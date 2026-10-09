// ACEest Fitness — Jenkins pipeline for Linux agents only (CSI ZG514 Assignment 1)
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness'
        // User-level pip installs on the Jenkins agent (no sudo required)
        PATH = "${env.HOME}/.local/bin:${env.PATH}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        // SCM checkout is already done by "Pipeline from SCM"; this stage keeps the log explicit.
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
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Tests in container') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} python3 -m pytest -v"
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
