# Hospital Management Portal – DevOps Project
**Subject:** 24CS2018 – DevOps | **Semester:** VII CSE (2025–2026 Odd Semester)
**Faculty:** Dr. E. Bijolin Edwin

---

## Project Title
**Automated CI/CD Pipeline for a Hospital Management Portal using Docker, Kubernetes, and Azure**

## Project Overview
A Flask-based Hospital Management web application that displays patient records, doctor availability, and billing information. Deployed end-to-end using a complete DevOps pipeline: GitHub Actions for CI/CD, Docker for containerization, Terraform for Azure infrastructure provisioning, Ansible for configuration management, and Kubernetes (AKS) for orchestration.

---

## Tools & Technologies
| Tool | Purpose |
|---|---|
| Python Flask | Web application |
| Git / GitHub | Version control |
| GitHub Actions | CI/CD pipeline (Test → Build → Deploy) |
| Docker | Multi-stage containerization |
| Azure ACR | Private container registry |
| Terraform | Infrastructure as Code (IaC) |
| Ansible | Kubernetes deployment automation |
| Kubernetes AKS | Container orchestration + autoscaling |

---

## Project Structure
```
hospital-devops/
├── app/
│   └── app.py                    # Flask app – patients, doctors, search, health
├── templates/
│   ├── base.html                 # Shared layout with nav
│   ├── index.html                # Patient dashboard
│   ├── detail.html               # Patient detail + billing
│   └── doctors.html              # Doctors on duty
├── tests/
│   └── test_app.py               # 8 unit tests
├── k8s/
│   ├── deployment.yml            # Rolling update deployment
│   ├── service.yml               # LoadBalancer service
│   └── hpa.yml                   # Auto-scale 2–5 pods
├── terraform/
│   └── main.tf                   # Azure RG + ACR + AKS
├── ansible/
│   └── deploy-playbook.yml       # Applies K8s manifests
├── .github/workflows/
│   └── deploy.yml                # Full CI/CD pipeline
├── Dockerfile                    # Multi-stage secure build
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Phase 1 – Push to GitHub
```bash
git init
git add .
git commit -m "feat: hospital management portal DevOps project"
git remote add origin https://<token>@github.com/<username>/hospital-devops.git
git push -u origin main
```

### Phase 2 – Test Locally
```bash
pip install -r requirements.txt
pytest tests/ -v
python app/app.py   # Visit http://localhost:5000
```

### Phase 3 – Terraform (Azure Infrastructure)
```bash
cd terraform
terraform init
terraform apply     # Creates RG + ACR + AKS (~8 mins)
terraform output acr_name   # Note this for GitHub secret
```

### Phase 4 – Add GitHub Secrets
| Secret | Value |
|---|---|
| `AZURE_CREDENTIALS` | JSON from `az ad sp create-for-rbac` |
| `ACR_NAME` | Output of `terraform output acr_name` |
| `AZURE_RESOURCE_GROUP` | `hospitalportal-rg` |
| `AKS_CLUSTER_NAME` | `hospitalportal-aks` |

### Phase 5 – Trigger Pipeline
```bash
git commit --allow-empty -m "ci: trigger pipeline"
git push origin main
```

### Phase 6 – Verify on AKS
```bash
az aks get-credentials --resource-group hospitalportal-rg --name hospitalportal-aks
kubectl get pods -n hospital-portal
kubectl get svc  -n hospital-portal   # Copy EXTERNAL-IP → open in browser
```

### Cleanup After Evaluation
```bash
cd terraform && terraform destroy
```

---

## CI/CD Pipeline Flow
```
git push → Test (pytest) → Build Docker → Push to ACR → Ansible Deploy → AKS Live
```

## Features
- 🏥 Patient dashboard with Admitted / Critical / Discharged status
- 👨‍⚕️ Doctor availability by department
- 🔍 Search by name, ID, ward, or doctor
- 💰 Patient billing and daily rate calculation
- ❤️ Health check endpoint `/health` for Kubernetes probes
- 📈 Auto-scaling (2–5 pods) via HPA
