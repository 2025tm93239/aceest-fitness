// ACEest Fitness — Jenkins pipeline for Linux agents only (CSI ZG514 Assignment 1)
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness'
        PATH = "${env.HOME}/.local/bin:${env.PATH}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''#!/bin/bash
                set -euo pipefail
                export PATH="${HOME}/.local/bin:${PATH}"

                echo "Python: $(python3 --version)"

                if ! python3 -m pip --version >/dev/null 2>&1; then
                  echo "Bootstrapping pip on Linux agent..."
                  python3 -m ensurepip --upgrade 2>/dev/null || true
                fi
                if ! python3 -m pip --version >/dev/null 2>&1; then
                  curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                  python3 get-pip.py --user
                  export PATH="${HOME}/.local/bin:${PATH}"
                fi

                python3 -m pip install --upgrade pip --user
                python3 -m pip install -r requirements.txt --user
                python3 -m pip --version
                python3 -m pytest --version
                '''
            }
        }

        stage('Build (compile / syntax)') {
            steps {
                sh '''#!/bin/bash
                set -euo pipefail
                export PATH="${HOME}/.local/bin:${PATH}"
                python3 -m compileall -q app.py aceest tests
                echo "compileall OK"
                '''
            }
        }

        stage('Quality gate — unit tests') {
            steps {
                sh '''#!/bin/bash
                set -euo pipefail
                export PATH="${HOME}/.local/bin:${PATH}"
                python3 -m pytest -v
                '''
            }
        }

        stage('Docker build') {
            steps {
                sh """#!/bin/bash
                set -euo pipefail

                echo "Jenkins process user: \$(whoami)"
                echo "Groups: \$(id)"
                ls -la /var/run/docker.sock 2>/dev/null || echo "No docker.sock at /var/run/docker.sock"

                DOCKER_CMD=docker
                if docker info >/dev/null 2>&1; then
                  echo "Using: docker (direct)"
                elif command -v sudo >/dev/null 2>&1 && sudo -n docker info >/dev/null 2>&1; then
                  DOCKER_CMD="sudo docker"
                  echo "Using: sudo docker (passwordless sudo)"
                else
                  echo "============================================================"
                  echo "Docker is not usable by this Jenkins user."
                  echo ""
                  echo "Fix A (preferred) — on the Jenkins server as sudo:"
                  echo "  sudo systemctl enable --now docker"
                  echo "  sudo usermod -aG docker jenkins"
                  echo "  sudo systemctl restart jenkins"
                  echo "  sudo -u jenkins docker ps"
                  echo ""
                  echo "Fix B — allow passwordless sudo for docker only:"
                  echo "  sudo visudo"
                  echo "  jenkins ALL=(ALL) NOPASSWD: /usr/bin/docker"
                  echo ""
                  echo "Fix C — lab workaround (insecure; dev VMs only):"
                  echo "  sudo chmod 666 /var/run/docker.sock"
                  echo "============================================================"
                  exit 1
                fi

                echo "\${DOCKER_CMD}" > .jenkins_docker_cmd
                \${DOCKER_CMD} build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                """
            }
        }

        stage('Tests in container') {
            steps {
                sh """#!/bin/bash
                set -euo pipefail
                DOCKER_CMD=\$(cat .jenkins_docker_cmd)
                \${DOCKER_CMD} run --rm ${IMAGE_NAME}:${BUILD_NUMBER} python3 -m pytest -v
                """
            }
        }
    }

    post {
        success {
            echo 'BUILD passed on Linux agent.'
        }
        failure {
            echo 'BUILD failed — see stage log above.'
        }
        always {
            deleteDir()
        }
    }
}
