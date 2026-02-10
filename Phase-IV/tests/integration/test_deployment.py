"""
Integration Tests for Todo App Deployment
Tests deployment health, connectivity, and service integration
Works with both Docker Compose and Kubernetes deployments
"""

import pytest
import requests
import subprocess
import time
import os
from typing import Dict, List


class TestDeploymentHealth:
    """Test suite for deployment health and connectivity"""

    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    TIMEOUT = 60  # seconds

    @pytest.fixture(scope="class")
    def deployment_type(self) -> str:
        """Detect deployment type (docker-compose or kubernetes)"""
        try:
            subprocess.run(["docker-compose", "ps"],
                         capture_output=True, check=True)
            return "docker-compose"
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(["kubectl", "get", "pods"],
                             capture_output=True, check=True)
                return "kubernetes"
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("No deployment detected")

    def test_all_services_running(self, deployment_type):
        """Test that all required services are running"""
        if deployment_type == "docker-compose":
            result = subprocess.run(
                ["docker-compose", "ps", "--format", "json"],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse container status
            import json
            containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]

            required_services = {"backend", "frontend", "postgres"}
            running_services = {c["Service"] for c in containers if c["State"] == "running"}

            assert required_services.issubset(running_services), \
                f"Missing services: {required_services - running_services}"

        elif deployment_type == "kubernetes":
            result = subprocess.run(
                ["kubectl", "get", "pods", "-o", "json"],
                capture_output=True,
                text=True,
                check=True
            )

            import json
            pods_data = json.loads(result.stdout)

            running_pods = [
                pod["metadata"]["name"]
                for pod in pods_data["items"]
                if pod["status"]["phase"] == "Running"
            ]

            assert len(running_pods) >= 3, \
                f"Expected at least 3 pods running, found {len(running_pods)}"

    def test_backend_health_endpoint(self):
        """Test backend liveness probe endpoint"""
        response = requests.get(f"{self.BACKEND_URL}/health", timeout=10)

        assert response.status_code == 200, \
            f"Backend health check failed with status {response.status_code}"

        data = response.json()
        assert data.get("status") == "healthy", \
            f"Backend reports unhealthy status: {data}"

    def test_backend_readiness_endpoint(self):
        """Test backend readiness probe (includes DB connectivity)"""
        response = requests.get(f"{self.BACKEND_URL}/ready", timeout=10)

        assert response.status_code == 200, \
            f"Backend readiness check failed with status {response.status_code}"

        data = response.json()
        assert data.get("status") == "ready", \
            f"Backend not ready: {data}"
        assert data.get("database") == "connected", \
            f"Database not connected: {data}"

    def test_frontend_health_endpoint(self):
        """Test frontend health endpoint"""
        response = requests.get(f"{self.FRONTEND_URL}/api/health", timeout=10)

        assert response.status_code == 200, \
            f"Frontend health check failed with status {response.status_code}"

        data = response.json()
        assert data.get("status") == "healthy", \
            f"Frontend reports unhealthy status: {data}"
        assert "timestamp" in data, \
            "Frontend health response missing timestamp"

    def test_frontend_loads(self):
        """Test that frontend homepage loads"""
        response = requests.get(self.FRONTEND_URL, timeout=10)

        assert response.status_code == 200, \
            f"Frontend homepage failed to load with status {response.status_code}"

        # Check for Next.js content
        assert len(response.text) > 0, "Frontend returned empty response"

    def test_backend_api_accessible(self):
        """Test that backend API is accessible"""
        # Test the docs endpoint
        response = requests.get(f"{self.BACKEND_URL}/docs", timeout=10)

        assert response.status_code == 200, \
            f"Backend API docs not accessible: {response.status_code}"

    def test_database_connectivity_from_backend(self):
        """Test database connectivity through backend readiness check"""
        # This is already tested in test_backend_readiness_endpoint
        # but we'll add a more comprehensive check

        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{self.BACKEND_URL}/ready", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("database") == "connected":
                        return  # Success
            except requests.RequestException:
                pass

            if attempt < max_retries - 1:
                time.sleep(2)

        pytest.fail("Database connectivity check failed after multiple retries")

    def test_services_respond_within_timeout(self):
        """Test that all services respond within acceptable timeout"""
        services = [
            (f"{self.BACKEND_URL}/health", "Backend health"),
            (f"{self.BACKEND_URL}/ready", "Backend readiness"),
            (f"{self.FRONTEND_URL}/api/health", "Frontend health"),
        ]

        for url, name in services:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            elapsed = time.time() - start_time

            assert response.status_code == 200, \
                f"{name} endpoint failed"
            assert elapsed < 2.0, \
                f"{name} took too long to respond: {elapsed:.2f}s"


class TestServiceIntegration:
    """Test suite for service-to-service integration"""

    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

    def test_backend_cors_configuration(self):
        """Test that backend CORS is configured for frontend"""
        # Make a request with Origin header
        headers = {"Origin": self.FRONTEND_URL}
        response = requests.get(
            f"{self.BACKEND_URL}/health",
            headers=headers,
            timeout=10
        )

        assert response.status_code == 200
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers or \
               "Access-Control-Allow-Origin" in response.headers, \
               "CORS headers not configured"

    def test_environment_variables_loaded(self, deployment_type):
        """Test that environment variables are properly loaded"""
        if deployment_type == "docker-compose":
            # Check backend container env vars
            result = subprocess.run(
                ["docker", "exec", "todo-backend", "env"],
                capture_output=True,
                text=True,
                check=True
            )

            env_vars = result.stdout
            assert "DATABASE_URL" in env_vars, "DATABASE_URL not set"
            assert "JWT_SECRET_KEY" in env_vars, "JWT_SECRET_KEY not set"
            assert "GEMINI_API_KEY" in env_vars, "GEMINI_API_KEY not set"


class TestDeploymentResilience:
    """Test suite for deployment resilience and recovery"""

    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

    def test_health_checks_recover_after_delay(self):
        """Test that health checks eventually succeed even with delays"""
        max_attempts = 10
        success = False

        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    f"{self.BACKEND_URL}/health",
                    timeout=5
                )
                if response.status_code == 200:
                    success = True
                    break
            except requests.RequestException:
                pass

            time.sleep(3)

        assert success, \
            f"Health check did not recover after {max_attempts} attempts"


@pytest.fixture(scope="session", autouse=True)
def wait_for_deployment():
    """Wait for deployment to be ready before running tests"""
    print("\nWaiting for deployment to be ready...")

    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    max_wait = 120  # 2 minutes
    start_time = time.time()

    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{backend_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Deployment is ready")
                return
        except requests.RequestException:
            pass

        time.sleep(5)

    pytest.fail("Deployment did not become ready within timeout")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
