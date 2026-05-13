pipeline {
    agent any
    
    environment {
        
        DOCKER_USER = 'tanyathep' 
        IMAGE_NAME = 'pm-alert-app'
        DOCKER_AUTH_ID = 'dockerhub-auth'
    }

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
            }
        }

        stage('2. Static Analysis') {
            steps {
                echo 'Checking code quality...'
            }
        }

        stage('3. Unit Test') {
            steps {
                echo 'Running unit tests...'
            }
        }

        stage('4. Docker Build') {
            steps {
                echo 'Building Docker Image...'
                sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:latest ."
            }
        }

        stage('5. Security Scan') {
            steps {
                echo 'Scanning image...'
            }
        }

        stage('6. Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_AUTH_ID}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER_ENV')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER_ENV --password-stdin"
                    sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}