# Katib NAS Atelier

An end-to-end **MLOps workflow** demonstrating **Neural Architecture Search (NAS)** using  
**Kubeflow Katib**, **Docker**, **Kubernetes (MicroK8s)**, and **FastAPI**.

This project shows how machine learning experimentation can be automated, scalable, reproducible, and deployment-ready using cloud-native technologies.

---

## Motivation

Traditional machine learning workflows are often:
- Manual and time-consuming
- Hard to scale across multiple experiments
- Difficult to reproduce
- Limited to experimentation without deployment

Hyperparameter tuning and architecture search usually become bottlenecks due to infrastructure complexity.

This project addresses these challenges by combining automated NAS, containerization, Kubernetes-native execution, persistent storage, and model serving.

---

## Project Structure

katib-nas-atelier/
├── train_continuous_nas.py # Continuous NAS training with Early Stopping
├── Dockerfile # Training container environment
├── continuous_nas.yaml # Katib experiment definition
├── tmp-pvc-pod.yaml # Temporary pod for PVC access
├── main.py # FastAPI inference service
└── model/ # Local mount point for trained artifacts

yaml
Copier le code

---

## Objectives

- Automate Neural Architecture Search
- Efficiently explore model configurations under resource constraints
- Enable reproducible ML experiments
- Persist and compare trial results
- Deploy the best-performing model as an API

---

## Neural Architecture Search (NAS)

Neural Architecture Search automatically explores different neural network architectures instead of relying on manual design.

In this project:
- Each Katib Trial represents a unique architecture or hyperparameter configuration
- Trials are scheduled progressively based on available cluster resources
- Not all trials run simultaneously
- Early stopping terminates poorly performing trials to save compute resources

---

## System Architecture

┌─────────────────────────┐
│ train_continuous_nas.py │
└─────────────┬───────────┘
↓
┌─────────────────────────┐
│ Docker Image │
└─────────────┬───────────┘
↓
┌─────────────────────────┐
│ MicroK8s Cluster │
│ (Single-node Kubernetes)│
└─────────────┬───────────┘
↓
┌─────────────────────────┐
│ Kubeflow Katib │
│ (NAS + HPO Engine) │
└─────────────┬───────────┘
↓
┌─────────────────────────┐
│ Persistent Volume Claim │
│ (Models & Metrics) │
└─────────────┬───────────┘
↓
┌─────────────────────────┐
│ FastAPI Inference API │
└─────────────────────────┘

yaml
Copier le code

---

## Components

### Training Logic
**File:** `train_continuous_nas.py`

- Receives hyperparameters from Katib
- Performs continuous training
- Applies early stopping
- Logs metrics and saves models to a PVC

---

### Containerization
**File:** `Dockerfile`

- Defines a consistent execution environment
- Ensures reproducibility
- Used by Katib training pods

---

### Katib Experiment
**File:** `continuous_nas.yaml`

Defines:
- Search space (architectures and hyperparameters)
- Optimization algorithm
- Objective metric
- Trial scheduling behavior

---

### Persistent Storage

- Uses Kubernetes Persistent Volume Claims
- Stores trained models and metrics
- Enables experiment comparison and auditability

---

### Model Extraction
**File:** `tmp-pvc-pod.yaml`

- Launches a temporary helper pod
- Mounts the PVC
- Allows inspection and extraction of artifacts

---

### Inference Service
**File:** `main.py`

- FastAPI-based REST service
- Loads the selected best model
- Exposes prediction endpoints
- Provides Swagger UI for testing

---

## Workflow

Experiment Definition
↓
Dockerized Training
↓
Katib NAS Trials
↓
Early Stopping
↓
Persistent Storage
↓
Best Model Selection
↓
FastAPI Deployment

yaml
Copier le code

---

## Reproducibility & Experiment Tracking

This workflow ensures reproducibility through:
- Docker-based containerization
- Declarative experiment configuration (YAML)
- Versioned training code
- Persistent metrics and model artifacts
- Identical re-execution under the same configuration

Each Katib experiment can be replayed, compared, and audited.

---

## Resource Constraints & Scalability

- Designed for a single-node MicroK8s cluster
- Trial concurrency depends on available CPU and memory
- Early stopping reduces unnecessary computation
- Easily scalable to multi-node Kubernetes clusters

---

## How to Run

### Build and Import Docker Image

```bash
docker build -t katib-nas:latest .
docker save katib-nas:latest | microk8s ctr image import -
Run Katib Experiment
```
```bash
microk8s kubectl apply -f continuous_nas.yaml
```
Monitor execution:

```bash
microk8s kubectl get experiments
microk8s kubectl get trials
microk8s kubectl get pods
Extract Trained Models
```

```bash
microk8s kubectl apply -f tmp-pvc-pod.yaml
microk8s kubectl exec -it tmp-pvc-pod -- sh
Start Inference Service
```
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access the API documentation:

```bash
http://localhost:8000/docs
```

Technology Stack
Python

Docker

Kubernetes (MicroK8s)

Kubeflow Katib

FastAPI

Use Cases
Neural Architecture Search experiments

MLOps education and learning

Kubernetes-based ML pipelines

Academic and research projects

Workshops and demonstrations

License
This project is intended for educational and research purposes.

yaml


---

If you want **later**:
- a **shorter README**
- a **paper-style version**
- or a **diagram image (PNG/SVG)**

I can do that — but this version is now **final and complete** 
