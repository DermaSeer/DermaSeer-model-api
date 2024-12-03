# Dermaseer Model Machine Learning API

DermaSeer ML API is a machine learning service for dermatological analysis and prediction. This API provides endpoints for skin condition prediction using machine learning models.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/dermaseer-ml-api.git
cd dermaseer-ml-api
```

2. Install dependencies (for local development):

```bash
pip install -r requirements.txt
```

### Firebase Setup

1. Firebase Admin Configuration:
   - Go to Firebase Console > Project Settings > Service Accounts
   - Generate a new private key
   - Save the key as `firebaseAdmin.json` in the project root

## Running the Application

### Local Development

Run the application:

```bash
python app.py
```

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t dermaseer-ml-api:1.0.0 .
```

2. Run the container:

```bash
docker run -d -p 5000:5000 --name model-ml-api dermaseer-ml-api:1.0.0
```

### Cloud Run Deployment

1. Clone Repository to Cloud Shell

2. Create Artifact Registry Repository

   ```bash
    gcloud artifacts repositories create dermaseer \
    --repository-format=docker \
    --location=asia-southeast2
   ```

3. Set Up Environment Variables

   ```bash
   # Set your project ID
   export GOOGLE_CLOUD_PROJECT=your-project-id

   # Set your region
   export REGION=asia-southeast2

   # Set your service name
   export SERVICE_NAME=dermaseer-ml-api

   # Setu your Artifact Registry Repository
   export ARTIFACT_REPO=dermaseer
   ```

4. Build and Push Docker Image

   ```bash
   gcloud builds submit --tag asia-southeast2-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${ARTIFACT_REPO}/dermaseer-ml-api:1.0.0
   ```

5. Deploy to Cloud Run
   ```bash
   gcloud run deploy ${SERVICE_NAME} \
   --image asia-southeast2-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${ARTIFACT_REPO}/dermaseer-ml-api:1.0.0 \
   --platform managed \
   --region ${REGION} \
   --allow-unauthenticated \
   --memory 2Gi \
   --cpu 2 \
   --port 5000
   ```

## API Documentation

### Endpoints

#### Predict Image

- **URL**: `/api/predict`
- **Method**: `POST`
- **Authentication**: Bearer Token required
- **Request Body**:
  ```json
  {
    "img_url": "https://storage.googleapis.com/bucket-name/predict/example-image.jpeg"
  }
  ```
- **Success Response**:
  ```json
  {
    "data": {
      "predicted_acne_type": "Fulminans",
      "probabilities": {
        "Fulminans": 0.93,
        "Fungal": 0.01,
        "Nodules": 0.0,
        "Papula": 0.01,
        "Postula": 0.05
      }
    }
  }
  ```
