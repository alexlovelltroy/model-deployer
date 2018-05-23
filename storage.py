from google.cloud import storage


def get_model(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = (bucket.list_blobs())

    for blob in blobs:
        print(blob.name)
    return blobs


def load_model(bucket_name, file_name):
    """Downloads a existing file inside a bucket and saves it root dir."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)
    print('Blob {} Downloaded.'.format(file_name))
    return 'New model loaded to Flask Application'


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
