# Phase IV – Constitution
## Cloud Native Todo Chatbot (Local Kubernetes Deployment)

### 1. Objective
Deploy the Phase III Todo Chatbot (Frontend + Backend + AI Chatbot)
on a local Kubernetes cluster using Minikube and Helm Charts.

### 2. Development Rules
- No manual coding is allowed
- All implementations must be generated via AI tools
- Agentic Dev Stack workflow must be followed strictly:
  Spec → Plan → Tasks → Implementation
- Every step must be reproducible and documented

### 3. Tooling Mandate
Mandatory tools for this phase:
- Docker Desktop (with Docker AI – Gordon if available)
- Minikube (local Kubernetes)
- Helm (package manager)
- kubectl-ai
- Kagent (optional but encouraged)

### 4. Containerization Policy
- Frontend and Backend must be containerized separately
- Docker images must be versioned
- Containers must be Kubernetes-ready

### 5. AI-Assisted DevOps Policy
- Docker operations should use Docker AI (Gordon)
- Kubernetes operations should use kubectl-ai and kagent
- Prompts and AI outputs must be saved for evaluation

### 6. Deployment Scope
- Local deployment only (Minikube)
- No cloud provider usage
- Helm Charts required for deployments

### 7. Success Criteria
- Frontend accessible via Minikube service
- Backend API reachable inside cluster
- Chatbot functionality operational
- Helm install/upgrade working successfully
