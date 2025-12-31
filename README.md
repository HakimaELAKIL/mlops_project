Katib NAS – Atelier

This project demonstrates a full MLOps workflow for Neural Architecture Search (NAS) using Kubeflow Katib, Docker, Kubernetes (MicroK8s), Early Stopping, and FastAPI inference.

Project Structure
katib-nas-atelier/
│
├── train_continuous_nas.py     # Core training logic with Early Stopping
├── Dockerfile                 # Training environment
├── continuous_nas.yaml        # Katib Experiment (search space)
├── tmp-pvc-pod.yaml           # Helper pod to extract models
├── main.py                    # FastAPI inference service
└── model/                     # Local mount point for PVC artifacts

Prerequisites

Docker

MicroK8s

Kubeflow Katib installed

Python 3.9+

Step 1 – Build the Docker Image
docker build -t katib-nas:latest .

Step 2 – Import Image into MicroK8s
docker save katib-nas:latest | microk8s ctr image import -


Verify:

microk8s ctr image list | grep katib-nas

Step 3 – Create Persistent Volume Claim (if not exists)
microk8s kubectl apply -f tmp-pvc-pod.yaml


Check PVC:

microk8s kubectl get pvc

Step 4 – Run Katib NAS Experiment
microk8s kubectl apply -f continuous_nas.yaml


Check experiment:

microk8s kubectl get experiment


Check trials:

microk8s kubectl get trials

Step 5 – Monitor Training Pods
microk8s kubectl get pods


Logs:

microk8s kubectl logs <training-pod-name>

Step 6 – Extract Trained Models from PVC

Deploy helper pod:

microk8s kubectl apply -f tmp-pvc-pod.yaml


Access pod:

microk8s kubectl exec -it tmp-pvc-pod -- /bin/sh


Copy models:

cp -r /mnt/pvc/* /model/

Step 7 – Run FastAPI Inference Service

Install dependencies:

pip install fastapi uvicorn


Run API:

uvicorn main:app --host 0.0.0.0 --port 8000


Test:

curl http://localhost:8000/docs

Step 8 – Clean Up (Optional)
microk8s kubectl delete -f continuous_nas.yaml
microk8s kubectl delete pod tmp-pvc-pod

Workflow Summary
train_continuous_nas.py
        ↓
Docker Image
        ↓
MicroK8s Registry
        ↓
Katib Experiment (NAS + Early Stopping)
        ↓
PVC (Models & Metrics)
        ↓
FastAPI Inference

Technologies

Python

Docker

Kubernetes (MicroK8s)

Kubeflow Katib

Neural Architecture Search

Early Stopping

FastAPI
