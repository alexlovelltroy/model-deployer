# Model-Deployer
Flask API for scikit learn
A simple Flask application that can serve predictions from a scikit-learn model. Reads a pickled sklearn model into memory from a Google Cloud Storage bucket.

When the Flask app is started it returns predictions through the /predict endpoint. You can also use the /train endpoint to train/retrain the model. Any sklearn model can be used for prediction.

Use /shutdown endpoint to shutdown the server
other API endpoints for GCS storage.

## Requirements
- GKE Cluster -Google Kubernetes Engine
- GCB -Google Cloud Builder
  - Used as a build trigger to build container images when a commit is made and push the builds to Google Container Registery.

## Pre-Requirements
- Add a Kubernetes secret for your GCP service account principle using the following command ``` kubectl create secret generic credentials --from-file ./service_account.json```
- Configure Cloud builder to trigger when a commit is made on the git repo.
- Have the required models stored inside a GCS bucket.
- Edit cloudbuild.yaml with appropriate Kubernetes cluster name and region. cloudbuild.yaml file is used as a pipeline job for container builder, Kubernetes deployment, etc...This is similar to Jenkins pipeline job.

## Flow of WORK
- User has different models stored on Google Cloud Storage.
- All the intermediate steps between a Git commit to deploying the application on a Kubernetes cluster is automated.
- User can use this application to pull the model from GCS and deploy it to a Kubernetes cluster.
- Once the application it deployed, get the external static IP of the cluster and train/predict on the models.

## Steps
- Edit the model.yaml with bucket name and model(file) name.
- Push git commit and wait for 3 mins for the build to complete and it deploys the flask application to Kubernetes cluster.
- use ```kubectl get services ``` to get the external LoadBalancer IP of our Demo application.
- try different endpoints ```http://<external-ip>/shutdown``` ```http://<external-ip>/train``` ```http://<external-ip>/predict```

## To redeploy a newer model on Kubernetes Cluster
- This assumes that the GCS bucket contains the model you would like to deploy.
- Edit the model.yaml file with the bucket name and model file name. The flask application downloads the model and loads it for training and prediction once the new pod is active.
-  Push the git commit and wait for 3-5 mins for the Google Cloud builder to run the pipeline as described in cloudbuild.yaml file.
- Once the new container image is pushed and the pod is deployed. use ```kubectl get services ``` to get the external LoadBalancer IP of our Demo application.

## Future WORK
- Automated rollbacks of Kubernetes deployment.
- Disable older pods( Flask app with previous models). This should act as a failover.
