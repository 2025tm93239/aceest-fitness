#!/bin/bash
# Run on the Jenkins Linux VM with sudo (one-time setup).
# Usage: sudo bash docs/jenkins-docker-fix.sh

set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root: sudo bash $0"
  exit 1
fi

echo "==> Start Docker"
systemctl enable --now docker

echo "==> Add jenkins user to docker group"
usermod -aG docker jenkins

echo "==> Restart Jenkins so the jenkins user picks up group docker"
systemctl restart jenkins

echo "==> Verify"
sleep 3
sudo -u jenkins docker ps
sudo -u jenkins docker run --rm hello-world

echo "Done. Trigger Build Now in Jenkins."
