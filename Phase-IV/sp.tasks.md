# Tasks: Cloud Native Todo Chatbot (Phase IV)

## 0. Preparation
- [ ] **Task 0.1**: Verify Prerequisites (Docker, Minikube, Helm, kubectl).
- [ ] **Task 0.2**: Ensure Phase II/III code is ready for containerization.

## 1. Containerization (AI-Driven)
- [ ] **Task 1.1**: Generate `Dockerfile` for Backend.
    - *Input*: `Phase-II/backend` code.
    - *Constraint*: Use Python 3.12+, Multi-stage build (builder/runner) for optimization.
    - *Agent*: "Gordon" (Simulated by Claude/Gemini).
- [ ] **Task 1.2**: Generate `Dockerfile` for Frontend.
    - *Input*: `Phase-II/frontend` code.
    - *Constraint*: Node.js 18+, Multi-stage build (deps/builder/runner).
    - *Agent*: "Gordon" (Simulated by Claude/Gemini).
- [ ] **Task 1.3**: Build and Verify Docker Images locally.
    - *Action*: `docker build -t todo-backend:latest ./Phase-II/backend`
    - *Action*: `docker build -t todo-frontend:latest ./Phase-II/frontend`
    - *Action*: `minikube image load ...`

## 2. Orchestration Manifests (AI-Driven)
- [ ] **Task 2.1**: Generate Backend K8s Manifests.
    - *Output*: `k8s/backend-deployment.yaml`, `k8s/backend-service.yaml`.
    - *Constraint*: Replicas=1, Env vars for DB and JWT, Service=ClusterIP.
- [ ] **Task 2.2**: Generate Frontend K8s Manifests.
    - *Output*: `k8s/frontend-deployment.yaml`, `k8s/frontend-service.yaml`.
    - *Constraint*: Env var `NEXT_PUBLIC_API_BASE_URL`, Service=LoadBalancer or NodePort (for Minikube access).
- [ ] **Task 2.3**: Generate Database Manifests.
    - *Output*: `k8s/postgres-deployment.yaml`, `k8s/postgres-service.yaml`, `k8s/pvc.yaml`.
    - *Note*: Use simple Deployment for Postgres for now.

## 3. Configuration & Secrets
- [ ] **Task 3.1**: Generate `k8s/configmap.yaml` (Non-sensitive env vars).
- [ ] **Task 3.2**: Generate `k8s/secrets.yaml` (Sensitive: DB password, JWT secret).

## 4. Helm Chart Creation
- [ ] **Task 4.1**: Create Helm Chart Structure (`charts/todo-app`).
- [ ] **Task 4.2**: Templatize Manifests into Helm format.
- [ ] **Task 4.3**: Define `values.yaml` with defaults.

## 5. Deployment & Verification
- [ ] **Task 5.1**: Deploy Chart to Minikube (`helm install`).
- [ ] **Task 5.2**: Verify Pod status.
- [ ] **Task 5.3**: Expose Services and Verify Access.
- [ ] **Task 5.4**: End-to-End Test (Chatbot Task Creation).