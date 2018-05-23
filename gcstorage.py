import pickle
# import errno
import os
import glob
from google.cloud import storage
from sklearn.externals import joblib


def get_model(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = (bucket.list_blobs())

    for blob in blobs:
        print(blob.name)
    return blobs


def load_model(bucket_name, source_model_name):
    if bucket_name:
        """Load model from Generic models GCS bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)  # Bucket name
        blob = bucket.blob(source_model_name)  # Source Model Name
        model = blob.download_to_filename(
            './models/{}'.format(source_model_name))
        print('Blob {} downloaded to {}.'.format(
            source_model_name, source_model_name))
        model_directory = './models'
    try:
        # Find the newest model file in the directory
        files = [x for x in os.listdir(model_directory) if x.endswith(".pkl")]
        list_of_files = glob.glob('./models/*')
        newest = max(list_of_files, key=os.path.getctime)
        print("Recently modified Docs", newest)
        model_file_name = '%s/%s' % (model_directory, newest[0])
        clf = joblib.load(model_file_name)
        return clf

    except Exception as e:
        clf = None
        raise FileNotFoundError(
            "No model found in {} with suffix '.pkl'{}.".format(model_directory, e))
    else:
        print('Sorry, that model bucket does not exist!')
        return 'Enter a valid modle name'


def upload_model(bucket_name, file_name, file_path):
    """Uploads a blob from the root directory."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)  # filename='./api.py'
    print('Blob {} uploaded.'.format(file_name))
    return blob.public_url


def delete_model(bucket_name, file_name, file_path):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print('Blob {} deleted.'.format(file_name))
    return 'Deleted Model'
