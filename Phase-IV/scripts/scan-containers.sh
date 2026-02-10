#!/bin/bash
# Container Vulnerability Scanning Script
# This script scans Docker images for vulnerabilities using Trivy

set -e

echo "=== Container Vulnerability Scanning ==="
echo ""

# Check if Trivy is installed
if ! command -v trivy &> /dev/null; then
    echo "❌ Trivy is not installed. Installing..."
    echo ""
    echo "To install Trivy on Ubuntu/Debian:"
    echo "  wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -"
    echo "  echo 'deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main' | sudo tee -a /etc/apt/sources.list.d/trivy.list"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install trivy"
    echo ""
    echo "Or install via binary:"
    echo "  curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin"
    exit 1
fi

echo "✓ Trivy is installed"
echo ""

# Scan backend image
echo "Scanning backend image: todo-backend:latest"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
trivy image --severity HIGH,CRITICAL --exit-code 1 todo-backend:latest

if [ $? -eq 0 ]; then
    echo "✓ Backend image: No HIGH/CRITICAL vulnerabilities found"
else
    echo "❌ Backend image: HIGH/CRITICAL vulnerabilities detected"
    echo "   Please review and fix vulnerabilities before deploying"
fi

echo ""

# Scan frontend image
echo "Scanning frontend image: todo-frontend:latest"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
trivy image --severity HIGH,CRITICAL --exit-code 1 todo-frontend:latest

if [ $? -eq 0 ]; then
    echo "✓ Frontend image: No HIGH/CRITICAL vulnerabilities found"
else
    echo "❌ Frontend image: HIGH/CRITICAL vulnerabilities detected"
    echo "   Please review and fix vulnerabilities before deploying"
fi

echo ""
echo "=== Scan Complete ==="
echo ""
echo "For detailed reports, run:"
echo "  trivy image --format json --output backend-scan.json todo-backend:latest"
echo "  trivy image --format json --output frontend-scan.json todo-frontend:latest"
