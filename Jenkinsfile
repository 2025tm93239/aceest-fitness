pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness'
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
                script {
                    if (isUnix()) {
                        sh 'python3 -m pip install --upgrade pip'
                        sh 'pip3 install -r requirements.txt'
                    } else {
                        bat 'python -m pip install --upgrade pip'
                        bat 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Build (compile / syntax)') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m compileall -q app.py aceest tests'
                    } else {
                        bat 'python -m compileall -q app.py aceest tests'
                    }
                }
            }
        }

        stage('Quality gate — unit tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'pytest -v'
                    } else {
                        bat 'pytest -v'
                    }
                }
            }
        }

        stage('Docker build') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    } else {
                        bat "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    }
                }
            }
        }

        stage('Tests in container') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} pytest -v"
                    } else {
                        bat "docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} pytest -v"
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'BUILD passed — code compiles, tests OK, Docker image built.'
        }
        failure {
            echo 'BUILD failed — fix errors before merging to main.'
        }
        always {
            deleteDir()
        }
    }
}
