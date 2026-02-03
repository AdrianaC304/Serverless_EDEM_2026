# ☁️ Extra Exercises: Cloud Functions & Cloud Run on GCP

![GCP](https://img.shields.io/badge/Platform-Google%20Cloud-blue?style=for-the-badge) 

This repository contains hands-on exercises for Cloud Functions and Cloud Run on Google Cloud Platform. The goal is to learn how to handle Cloud Storage events, manage IAM permissions, and develop production-ready serverless functions.

- Professors: 
    - [Javi Briones](https://github.com/jabrio)
    - [Adriana Campos](https://github.com/AdrianaC304)


Before starting the exercises, make sure you have everything set up:

```
gcloud config list
```

```
gcloud config set project <PROJECT_ID>
```

```
gcloud services enable cloudbuild.googleapis.com
```

```
gcloud services enable run.googleapis.com containerregistry.googleapis.com
```

Do not create a new repository if one already exists.

```
gcloud services enable artifactregistry.googleapis.com
```

```
gcloud artifacts repositories create <REPOSITORY_NAME> \
  --repository-format=docker \
  --location=<REGION>
```


## Exercise 1: Generate Random  Jokes

### 📌 Description

We will use a Cloud Function to generate random jokes.


```
cd ./GCP/01_Notebooks/01_ExercisesCloudRun/01_CloudFunctions
```

```
gcloud functions deploy <FUNCTION_NAME> \
  --gen2 \
  --runtime nodejs20 \
  --region <REGION> \
  --entry-point randomJoke \
  --trigger-http 
```

Now we are going to generate a token to test how to connect to it using authentication:

```
gcloud auth print-identity-token
```

```
TOKEN=$(gcloud auth print-identity-token)
```

```
curl -H "Authorization: Bearer $TOKEN" \
  <YOUR_CLOUD_FUNCTION_URL>
```

You can also allow traffic without authentication to view the joke. In the **security section**, change the option to Allow public access.

## Exercise 2: Copy Images Between Buckets

### 📌 Description

In this exercise, we will work entirely from the GCP **interface**. The goal is that when an image is uploaded to a bucket, a Cloud Function is triggered to copy the image from one bucket to another.

You need to create **two buckets** for this exercise. The first can be named imagenes-originales and the second imagenes-miniaturas. Both buckets should be regional and located in europe-west1.

You need to create a **Cloud Function**. 

- Name: copyimage
- Region: europe-west1
- Type:  Node.js 22
- Trigger:
  - **Type:** Cloud Storage  
  - **Event type:** `google.cloud.storage.object.v1.finalized`  
  - **Bucket :** `imagenes-originales`  
- Code:
  - Now you can copy the code `index.js` and put it in the interface, the entrypoint is copyImage. 
  - Copy the code in `package.json`.


This command is used to grant a specific account permission to invoke a Cloud Run service:

```
gcloud run services add-iam-policy-binding copyimage \
  --member="<YOUR_SERVICE_ACCOUNT>" \
  --role="roles/run.invoker" \
  --region europe-west1
```


## Exercise 3: Generate a Message

### 📌 Description

Cloud Run exposes a public HTTP endpoint if `--allow-unauthenticated` is set. Flask must listen on `0.0.0.0` and port `8080`.   It runs as a **serverless service** that scales automatically.

```
cd ./GCP/01_Notebooks/01_ExercisesCloudRun/03_CloudRun
```

Build the Docker Image

```
gcloud builds submit --tag <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>/<IMAGE_NAME>:latest .
```

Confirm the Image was Created

```
gcloud artifacts docker images list <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>
```

Deploy the Cloud Run Service

```
gcloud run deploy <SERVICE_NAME> \
  --image <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>/<IMAGE_NAME>:latest \
  --platform managed \
  --region <REGION> \
  --allow-unauthenticated
```

Now we are going to generate a token to test how to connect to it using authentication:

```
TOKEN=$(gcloud auth print-identity-token)
```

```
curl -H "Authorization: Bearer $TOKEN" \
     https://<SERVICE_URL>/
```

```
curl -H "Authorization: Bearer $TOKEN" \
     https://<SERVICE_URL>/health
```



## Exercise 4: Reading and Analyzing Users in BigQuery via Cloud Run

### 📌 Description

In this example, we will read data from a **BigQuery database** to see which users exist and what actions they perform.  

For this exercise, you have a file (`Clients.csv`) with random client information. Using the **GCP Console**, go to BigQuery, create a **new table**, and upload the `Clients.csv` file into it.

The Cloud Run API provides:

- A list of existing users  
- A list of existing episodes  
- The source of truth for the generator

```
cd ./GCP/01_Notebooks/01_ExercisesCloudRun/04_CloudRun
```

Build the Docker Image:

```
gcloud builds submit \
  --tag <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>/<IMAGE_NAME>:latest .
```

Deploy the Cloud Run Service:

```
gcloud run deploy <SERVICE_NAME> \
  --image <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>/<IMAGE_NAME>:latest \
  --platform managed \
  --allow-unauthenticated
```

**Service Account Permission Requirements**

The service account used for deployment must have the following permissions:

- **Storage:** `roles/storage.objectAdmin`
- **Cloud Build:** `roles/cloudbuild.builds.editor`
- **Artifact Registry:** `roles/artifactregistry.writer`
- **BigQuery:** 
  - `BigQuery Data Viewer`
  - `BigQuery Job User`


Access All Client Identifiers from the Terminal. Generate an identity token:

```
gcloud auth print-identity-token
```

```
TOKEN=$(gcloud auth print-identity-token)
```

Call the Cloud Run API to get the list of users:

```
curl -H "Authorization: Bearer $TOKEN" https://<SERVICE_URL>/users
```

***Optional:***

As an extra exercise within Exercise 4, you can implement the following architecture.   In this case, you need to **edit the `main.py` file** so that after reading from BigQuery, it inserts all user identifiers into a **Pub/Sub topic**. Additionally, you need to **modify the function deployment** to set up a **trigger** so that the Cloud Run service executes **every time a new client is inserted**.  

| Database (BigQuery) | >> | API (Cloud Run) | >> | Event Generator | >> | Pub/Sub |


# Real-World Projects

Cloud Functions and Cloud Run are widely used in real-world projects. Beyond the Spotify example we have been working on, below we present two real use cases of these services.

***Use case 1:***

<img src="Image/Usecase1.png" width="1500"/>

***Use case 2:***

<img src="Image/Usecase2.png" width="1500"/>
