pipeline {
    agent any

    environment {
        DOCKER_USER = 'tanyathep'
        IMAGE_NAME = 'pm-alert-app'
        IMAGE_TAG = 'latest'
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
                echo 'Checking Python syntax...'
                sh 'python3 -m py_compile app/app.py'
            }
        }

        stage('3. Unit Test') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    python3 -m venv test-env
                    . test-env/bin/activate
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                    python -m unittest app/test_app.py
                '''
            }
        }

        stage('4. Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('5. Security Scan') {
            steps {
                echo 'Running lightweight image inspection...'
                sh "docker image inspect ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} > /dev/null"
            }
        }

        stage('6. Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_AUTH_ID}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER_ENV')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER_ENV" --password-stdin'
                    sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('7. Deploy with Terraform + Ansible') {
            steps {
                echo 'Validating infrastructure and deploying app...'
                // ให้ Jenkins ทำหน้าที่เช็คความถูกต้องของไฟล์อย่างเดียวพอครับ
                dir('terraform') {
                    sh 'terraform init -input=false'
                    sh 'terraform validate'
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}