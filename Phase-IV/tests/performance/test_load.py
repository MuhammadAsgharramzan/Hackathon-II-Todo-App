#!/usr/bin/env python3
"""
Performance Load Testing for Todo App
Tests response times, throughput, and resource usage under load
"""

import concurrent.futures
import json
import sys
import time
import urllib.request
import urllib.error
from typing import List, Dict, Tuple
from statistics import mean, median, stdev
import subprocess


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_header(text: str):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(text)
    print(f"{'='*60}{Colors.RESET}\n")


def print_pass(message: str):
    print(f"  {Colors.GREEN}✓ {message}{Colors.RESET}")


def print_fail(message: str):
    print(f"  {Colors.RED}✗ {message}{Colors.RESET}")


def print_info(message: str):
    print(f"  {Colors.YELLOW}ℹ {message}{Colors.RESET}")


def make_request(url: str, timeout: int = 5) -> Tuple[bool, float, int]:
    """Make HTTP request and return (success, response_time, status_code)"""
    start = time.time()
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed = time.time() - start
            return True, elapsed, response.status
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start
        return False, elapsed, e.code
    except Exception:
        elapsed = time.time() - start
        return False, elapsed, 0


def run_concurrent_requests(url: str, num_requests: int, num_workers: int) -> List[Tuple[bool, float, int]]:
    """Run concurrent requests and return results"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(make_request, url) for _ in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results


def calculate_percentile(values: List[float], percentile: int) -> float:
    """Calculate percentile from sorted values"""
    sorted_values = sorted(values)
    index = int(len(sorted_values) * percentile / 100)
    return sorted_values[min(index, len(sorted_values) - 1)]


def get_container_stats() -> Dict[str, Dict]:
    """Get CPU and memory stats for containers"""
    try:
        result = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )

        stats = {}
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                name = data.get("Name", "")
                if "todo-" in name:
                    cpu_str = data.get("CPUPerc", "0%").rstrip('%')
                    mem_str = data.get("MemPerc", "0%").rstrip('%')
                    stats[name] = {
                        "cpu": float(cpu_str),
                        "memory": float(mem_str)
                    }
        return stats
    except Exception as e:
        print_info(f"Could not get container stats: {e}")
        return {}


def test_response_times():
    """Test response times under normal load"""
    print_header("Test 1: Response Time Analysis")

    endpoints = [
        ("http://localhost:8000/health", "Backend Health"),
        ("http://localhost:8000/ready", "Backend Readiness"),
        ("http://localhost:3000/api/health", "Frontend Health"),
    ]

    num_requests = 100
    results_by_endpoint = {}

    for url, name in endpoints:
        print(f"\n{Colors.BLUE}Testing: {name}{Colors.RESET}")
        print_info(f"Running {num_requests} requests...")

        results = run_concurrent_requests(url, num_requests, num_workers=10)

        # Extract response times from successful requests
        response_times = [rt for success, rt, _ in results if success]
        success_count = len(response_times)

        if response_times:
            avg_time = mean(response_times) * 1000  # Convert to ms
            median_time = median(response_times) * 1000
            p95_time = calculate_percentile(response_times, 95) * 1000
            p99_time = calculate_percentile(response_times, 99) * 1000

            print_info(f"Success rate: {success_count}/{num_requests} ({success_count/num_requests*100:.1f}%)")
            print_info(f"Average: {avg_time:.2f}ms")
            print_info(f"Median: {median_time:.2f}ms")
            print_info(f"P95: {p95_time:.2f}ms")
            print_info(f"P99: {p99_time:.2f}ms")

            # Check against NFR-1 requirement (p95 < 500ms)
            if p95_time < 500:
                print_pass(f"P95 response time meets requirement (<500ms)")
            else:
                print_fail(f"P95 response time exceeds requirement: {p95_time:.2f}ms")

            results_by_endpoint[name] = {
                "success_rate": success_count/num_requests,
                "avg": avg_time,
                "p95": p95_time,
                "p99": p99_time
            }
        else:
            print_fail("All requests failed")
            results_by_endpoint[name] = None

    return results_by_endpoint


def test_concurrent_users():
    """Test system under concurrent user load"""
    print_header("Test 2: Concurrent User Load")

    url = "http://localhost:8000/health"
    concurrent_users = [10, 25, 50, 100]
    requests_per_user = 10

    results = []

    for num_users in concurrent_users:
        print(f"\n{Colors.BLUE}Testing with {num_users} concurrent users{Colors.RESET}")
        total_requests = num_users * requests_per_user

        start_time = time.time()
        request_results = run_concurrent_requests(url, total_requests, num_workers=num_users)
        total_time = time.time() - start_time

        success_count = sum(1 for success, _, _ in request_results if success)
        response_times = [rt for success, rt, _ in request_results if success]

        if response_times:
            throughput = total_requests / total_time
            avg_time = mean(response_times) * 1000
            p95_time = calculate_percentile(response_times, 95) * 1000

            print_info(f"Total time: {total_time:.2f}s")
            print_info(f"Throughput: {throughput:.2f} req/s")
            print_info(f"Success rate: {success_count}/{total_requests} ({success_count/total_requests*100:.1f}%)")
            print_info(f"Average response: {avg_time:.2f}ms")
            print_info(f"P95 response: {p95_time:.2f}ms")

            if success_count == total_requests and p95_time < 500:
                print_pass(f"System handles {num_users} concurrent users successfully")
            else:
                print_fail(f"System struggled with {num_users} concurrent users")

            results.append({
                "users": num_users,
                "throughput": throughput,
                "p95": p95_time,
                "success_rate": success_count/total_requests
            })

    return results


def test_resource_usage():
    """Test CPU and memory usage under load"""
    print_header("Test 3: Resource Usage Under Load")

    print_info("Measuring baseline resource usage...")
    baseline_stats = get_container_stats()

    if baseline_stats:
        print("\nBaseline:")
        for container, stats in baseline_stats.items():
            print(f"  {container}: CPU={stats['cpu']:.1f}%, Memory={stats['memory']:.1f}%")

    print_info("\nGenerating load...")
    url = "http://localhost:8000/health"

    # Run load test
    run_concurrent_requests(url, 500, num_workers=50)

    time.sleep(2)  # Let metrics stabilize

    print_info("Measuring resource usage under load...")
    load_stats = get_container_stats()

    if load_stats:
        print("\nUnder Load:")
        all_within_limits = True
        for container, stats in load_stats.items():
            print(f"  {container}: CPU={stats['cpu']:.1f}%, Memory={stats['memory']:.1f}%")

            # Check against NFR-1 requirement (< 80%)
            if stats['cpu'] < 80 and stats['memory'] < 80:
                print_pass(f"{container} within resource limits")
            else:
                print_fail(f"{container} exceeds resource limits")
                all_within_limits = False

        return all_within_limits
    else:
        print_info("Could not measure resource usage")
        return None


def test_sustained_load():
    """Test system under sustained load"""
    print_header("Test 4: Sustained Load Test")

    url = "http://localhost:8000/health"
    duration = 30  # seconds
    requests_per_second = 10

    print_info(f"Running sustained load for {duration} seconds...")
    print_info(f"Target: {requests_per_second} req/s")

    start_time = time.time()
    all_results = []

    while time.time() - start_time < duration:
        batch_start = time.time()
        results = run_concurrent_requests(url, requests_per_second, num_workers=10)
        all_results.extend(results)

        # Sleep to maintain target rate
        elapsed = time.time() - batch_start
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)

    total_time = time.time() - start_time
    success_count = sum(1 for success, _, _ in all_results if success)
    response_times = [rt for success, rt, _ in all_results if success]

    if response_times:
        actual_throughput = len(all_results) / total_time
        avg_time = mean(response_times) * 1000
        p95_time = calculate_percentile(response_times, 95) * 1000

        print_info(f"Duration: {total_time:.2f}s")
        print_info(f"Total requests: {len(all_results)}")
        print_info(f"Actual throughput: {actual_throughput:.2f} req/s")
        print_info(f"Success rate: {success_count}/{len(all_results)} ({success_count/len(all_results)*100:.1f}%)")
        print_info(f"Average response: {avg_time:.2f}ms")
        print_info(f"P95 response: {p95_time:.2f}ms")

        if success_count/len(all_results) > 0.99 and p95_time < 500:
            print_pass("System maintains performance under sustained load")
            return True
        else:
            print_fail("System degrades under sustained load")
            return False

    return False


def main():
    print_header("Todo App - Performance Load Testing")

    print_info("Warming up services...")
    make_request("http://localhost:8000/health")
    make_request("http://localhost:3000/api/health")
    time.sleep(2)

    # Run all tests
    test_results = {}

    test_results["response_times"] = test_response_times()
    test_results["concurrent_users"] = test_concurrent_users()
    test_results["resource_usage"] = test_resource_usage()
    test_results["sustained_load"] = test_sustained_load()

    # Final summary
    print_header("Performance Test Summary")

    print(f"\n{Colors.BLUE}NFR-1 Requirements:{Colors.RESET}")
    print("  • P95 response time < 500ms")
    print("  • Support 100 concurrent users")
    print("  • CPU/Memory usage < 80% under load")

    print(f"\n{Colors.BLUE}Results:{Colors.RESET}")

    # Check response time requirement
    if test_results["response_times"]:
        all_meet_requirement = all(
            data and data["p95"] < 500
            for data in test_results["response_times"].values()
            if data
        )
        if all_meet_requirement:
            print_pass("Response time requirement met")
        else:
            print_fail("Response time requirement not met")

    # Check concurrent users
    if test_results["concurrent_users"]:
        user_100_result = next((r for r in test_results["concurrent_users"] if r["users"] == 100), None)
        if user_100_result and user_100_result["success_rate"] > 0.99:
            print_pass("Concurrent user requirement met (100 users)")
        else:
            print_fail("Concurrent user requirement not met")

    # Check resource usage
    if test_results["resource_usage"]:
        print_pass("Resource usage requirement met")
    elif test_results["resource_usage"] is False:
        print_fail("Resource usage requirement not met")
    else:
        print_info("Resource usage could not be measured")

    # Check sustained load
    if test_results["sustained_load"]:
        print_pass("Sustained load test passed")
    else:
        print_fail("Sustained load test failed")

    print(f"\n{Colors.GREEN}Performance testing complete!{Colors.RESET}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
