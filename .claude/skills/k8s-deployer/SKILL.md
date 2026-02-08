---
name: "k8s-deployer"
description: "Deploy applications to Kubernetes (Minikube/Cloud) using Helm Charts and Manifests. Handles verification and Service exposure."
version: "1.0.0"
---

# Kubernetes Deployer Skill

## When to Use This Skill
- User wants to deploy an application to Kubernetes.
- User needs to verify or fix Kubernetes manifests (`yaml` files).
- User wants to create or install a Helm Chart.
- User needs to expose a service (NodePort, LoadBalancer, Port-Forward).
- User encounters deployment errors (CrashLoopBackOff, ImagePullBackOff).

## How This Skill Works

1.  **Context Check**: Verify `kubectl` is connected to the right cluster (`kubectl config current-context`). Ensure Minikube is running if local.
2.  **Manifest Verification**:
    *   Check `image:` tags in Deployments match built images.
    *   Verify `containerPort` matches application listen port.
    *   Check `env` variables or `ConfigMap` references.
    *   Validate YAML syntax.
3.  **Helm Charting**:
    *   Create structure: `helm create <chart-name>`.
    *   Templatize: Move hardcoded values from manifests to `values.yaml` and use `{{ .Values.key }}` in templates.
    *   Install/Upgrade: `helm upgrade --install <release-name> <chart-path> --values values.yaml`.
4.  **Deployment**: Apply manifests (`kubectl apply -f k8s/`) if not using Helm.
5.  **Verification**:
    *   Check Pods: `kubectl get pods`. Look for `Running` state.
    *   Debug: `kubectl describe pod <pod-name>` or `kubectl logs <pod-name>` if not running.
    *   Expose: Use `minikube service <service-name>` or `kubectl port-forward` to access.

## Output Format

Provide:
- **Cluster Status**: "Connected to [minikube/cluster-name]"
- **Deployment Actions**: "Applied [manifests]" or "Installed Helm release [name]"
- **Resource Status**: Table of Pods and Services with status.
- **Access URLs**: URLs to access the application.
- **Troubleshooting**: Analysis of any errors (e.g., "Pod failed due to config missing").

## Quality Criteria
- All Pods are in `Running` state (1/1).
- Services have valid ClusterIPs or ExternalIPs (if LoadBalancer).
- Application is reachable via the exposed URL.
- No `ImagePullBackOff` or `CrashLoopBackOff` errors.

## Example

**Input**: "Deploy the todo-backend to Minikube using Helm."

**Output**:
1.  **Context**: Minikube active.
2.  **Chart**: Found chart in `charts/todo-app`. Checked `values.yaml` for correct image tag `todo-backend:latest`.
3.  **Install**: Executed `helm upgrade --install todo-app charts/todo-app`.
4.  **Verify**: Pods are Running. Service exposed at `http://127.0.0.1:xxx`.
5.  **Result**: Deployment Successful.
