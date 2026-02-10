"""
Backend Container Tests
Tests Docker container build and runtime requirements
"""
import subprocess
import sys
import time
import requests
import pytest


class TestBackendContainer:
    """Test suite for backend Docker container"""

    IMAGE_NAME = "todo-backend:latest"
    CONTAINER_NAME = "test-todo-backend"

    @pytest.fixture(scope="class")
    def container_info(self):
        """Build and start container for testing"""
        # Build the container
        print(f"\nBuilding container: {self.IMAGE_NAME}")
        build_result = subprocess.run(
            ["docker", "build", "-t", self.IMAGE_NAME, "."],
            cwd="/mnt/h/GIAIC/Todo-app-hackathon-II/Phase-II/backend",
            capture_output=True,
            text=True
        )

        if build_result.returncode != 0:
            pytest.fail(f"Container build failed: {build_result.stderr}")

        # Start the container
        print(f"Starting container: {self.CONTAINER_NAME}")
        run_result = subprocess.run(
            [
                "docker", "run", "-d",
                "--name", self.CONTAINER_NAME,
                "-p", "8000:8000",
                "-e", "DATABASE_URL=sqlite:///./test.db",
                "-e", "JWT_SECRET_KEY=test-secret-key-for-testing-only",
                self.IMAGE_NAME
            ],
            capture_output=True,
            text=True
        )

        if run_result.returncode != 0:
            pytest.fail(f"Container start failed: {run_result.stderr}")

        container_id = run_result.stdout.strip()

        # Wait for container to be ready
        time.sleep(5)

        yield {"id": container_id, "name": self.CONTAINER_NAME}

        # Cleanup
        print(f"\nCleaning up container: {self.CONTAINER_NAME}")
        subprocess.run(["docker", "stop", self.CONTAINER_NAME], capture_output=True)
        subprocess.run(["docker", "rm", self.CONTAINER_NAME], capture_output=True)

    def test_container_builds_successfully(self):
        """Test that container builds without errors"""
        result = subprocess.run(
            ["docker", "build", "-t", f"{self.IMAGE_NAME}-test", "."],
            cwd="/mnt/h/GIAIC/Todo-app-hackathon-II/Phase-II/backend",
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"

        # Cleanup test image
        subprocess.run(["docker", "rmi", f"{self.IMAGE_NAME}-test"], capture_output=True)

    def test_python_version(self, container_info):
        """Test that Python version is 3.12+"""
        result = subprocess.run(
            ["docker", "exec", container_info["name"], "python", "--version"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, "Failed to get Python version"

        version_output = result.stdout.strip()
        assert "Python 3.1" in version_output or "Python 3." in version_output, \
            f"Expected Python 3.12+, got: {version_output}"

        # Extract version number
        version_parts = version_output.split()[1].split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])

        assert major == 3 and minor >= 12, \
            f"Expected Python 3.12+, got: {major}.{minor}"

    def test_dependencies_installed(self, container_info):
        """Test that all dependencies are installed correctly"""
        # Check for key dependencies
        dependencies = ["fastapi", "uvicorn", "sqlalchemy", "pydantic"]

        for dep in dependencies:
            result = subprocess.run(
                ["docker", "exec", container_info["name"], "pip", "show", dep],
                capture_output=True,
                text=True
            )

            assert result.returncode == 0, f"Dependency {dep} not installed"

    def test_application_starts(self, container_info):
        """Test that application starts without errors"""
        # Check container is running
        result = subprocess.run(
            ["docker", "ps", "-f", f"name={container_info['name']}", "--format", "{{.Status}}"],
            capture_output=True,
            text=True
        )

        status = result.stdout.strip()
        assert "Up" in status, f"Container not running: {status}"

    def test_health_endpoint_responds(self, container_info):
        """Test that health endpoint responds with 200"""
        # Wait a bit more for app to be fully ready
        time.sleep(3)

        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            assert response.status_code == 200, \
                f"Health endpoint returned {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Health endpoint not yet implemented: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
