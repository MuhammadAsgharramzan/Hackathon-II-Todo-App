#!/usr/bin/env python3
"""
Simple Integration Tests for Todo App Deployment
No external dependencies required - uses only standard library
"""

import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
from typing import Dict, Tuple


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test(name: str):
    print(f"\n{Colors.BLUE}▶ {name}{Colors.RESET}")


def print_pass(message: str):
    print(f"  {Colors.GREEN}✓ {message}{Colors.RESET}")


def print_fail(message: str):
    print(f"  {Colors.RED}✗ {message}{Colors.RESET}")


def print_info(message: str):
    print(f"  {Colors.YELLOW}ℹ {message}{Colors.RESET}")


def http_get(url: str, timeout: int = 10) -> Tuple[int, Dict]:
    """Make HTTP GET request and return status code and JSON data"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            return response.status, data
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        print_fail(f"Request failed: {e}")
        return 0, {}


def test_docker_compose_running() -> bool:
    """Test that Docker Compose services are running"""
    print_test("Test: Docker Compose Services Running")

    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
            cwd="/mnt/h/GIAIC/Todo-app-hackathon-II/Phase-IV"
        )

        containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]

        required_services = {"backend", "frontend", "postgres"}
        running_services = {c["Service"] for c in containers if c["State"] == "running"}

        if required_services.issubset(running_services):
            print_pass(f"All required services running: {', '.join(running_services)}")
            return True
        else:
            missing = required_services - running_services
            print_fail(f"Missing services: {', '.join(missing)}")
            return False

    except Exception as e:
        print_fail(f"Failed to check Docker Compose status: {e}")
        return False


def test_backend_health() -> bool:
    """Test backend health endpoint"""
    print_test("Test: Backend Health Endpoint")

    status, data = http_get("http://localhost:8000/health")

    if status == 200 and data.get("status") == "healthy":
        print_pass("Backend health check passed")
        return True
    else:
        print_fail(f"Backend health check failed (status: {status}, data: {data})")
        return False


def test_backend_readiness() -> bool:
    """Test backend readiness endpoint (includes DB connectivity)"""
    print_test("Test: Backend Readiness Endpoint")

    status, data = http_get("http://localhost:8000/ready")

    if status == 200:
        if data.get("status") == "ready" and data.get("database") == "connected":
            print_pass("Backend is ready and database is connected")
            return True
        else:
            print_fail(f"Backend not ready: {data}")
            return False
    else:
        print_fail(f"Readiness check failed with status {status}")
        return False


def test_frontend_health() -> bool:
    """Test frontend health endpoint"""
    print_test("Test: Frontend Health Endpoint")

    status, data = http_get("http://localhost:3000/api/health")

    if status == 200 and data.get("status") == "healthy":
        print_pass(f"Frontend health check passed (timestamp: {data.get('timestamp')})")
        return True
    else:
        print_fail(f"Frontend health check failed (status: {status})")
        return False


def test_frontend_loads() -> bool:
    """Test that frontend homepage loads"""
    print_test("Test: Frontend Homepage Loads")

    try:
        req = urllib.request.Request("http://localhost:3000")
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode()
            if response.status == 200 and len(content) > 0:
                print_pass(f"Frontend loaded successfully ({len(content)} bytes)")
                return True
            else:
                print_fail("Frontend returned empty response")
                return False
    except Exception as e:
        print_fail(f"Failed to load frontend: {e}")
        return False


def test_backend_api_docs() -> bool:
    """Test that backend API docs are accessible"""
    print_test("Test: Backend API Documentation")

    try:
        req = urllib.request.Request("http://localhost:8000/docs")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print_pass("Backend API docs accessible")
                return True
            else:
                print_fail(f"API docs returned status {response.status}")
                return False
    except Exception as e:
        print_fail(f"Failed to access API docs: {e}")
        return False


def test_response_times() -> bool:
    """Test that services respond within acceptable time"""
    print_test("Test: Response Times")

    endpoints = [
        ("http://localhost:8000/health", "Backend health"),
        ("http://localhost:8000/ready", "Backend readiness"),
        ("http://localhost:3000/api/health", "Frontend health"),
    ]

    all_passed = True
    for url, name in endpoints:
        start = time.time()
        status, _ = http_get(url, timeout=5)
        elapsed = time.time() - start

        if status == 200 and elapsed < 2.0:
            print_pass(f"{name}: {elapsed:.3f}s")
        else:
            print_fail(f"{name}: {elapsed:.3f}s (too slow or failed)")
            all_passed = False

    return all_passed


def test_container_health_status() -> bool:
    """Test container health status from Docker"""
    print_test("Test: Container Health Status")

    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
            cwd="/mnt/h/GIAIC/Todo-app-hackathon-II/Phase-IV"
        )

        containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]

        all_healthy = True
        for container in containers:
            service = container["Service"]
            health = container.get("Health", "N/A")

            if health == "healthy":
                print_pass(f"{service}: {health}")
            else:
                print_info(f"{service}: {health}")
                if service in ["backend", "postgres"]:
                    all_healthy = False

        return all_healthy

    except Exception as e:
        print_fail(f"Failed to check container health: {e}")
        return False


def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Todo App - Integration Test Suite")
    print(f"{'='*60}{Colors.RESET}\n")

    print_info("Waiting for services to be ready...")
    time.sleep(2)

    tests = [
        ("Docker Compose Services", test_docker_compose_running),
        ("Backend Health", test_backend_health),
        ("Backend Readiness", test_backend_readiness),
        ("Frontend Health", test_frontend_health),
        ("Frontend Homepage", test_frontend_loads),
        ("Backend API Docs", test_backend_api_docs),
        ("Response Times", test_response_times),
        ("Container Health", test_container_health_status),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print_fail(f"Test crashed: {e}")
            results.append((name, False))

    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Test Summary")
    print(f"{'='*60}{Colors.RESET}\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"  {status}  {name}")

    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.RESET}")

    if passed == total:
        print(f"{Colors.GREEN}✓ All integration tests passed!{Colors.RESET}\n")
        return 0
    else:
        print(f"{Colors.RED}✗ Some tests failed{Colors.RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
