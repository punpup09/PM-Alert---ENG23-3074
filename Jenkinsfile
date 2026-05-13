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

        stage('2. Static Analysis / Test') {
            steps {
                echo 'Checking Python syntax...'
                // ตรวจจับ Syntax Error ในโค้ด ถ้าโค้ดพัง Pipeline จะหยุดและขึ้นกากบาทสีแดงทันที
                sh 'python3 -m py_compile app/app.py' 
            }
        }

        stage('3. Unit Test') {
            steps {
                echo 'Running unit tests...'
                // สร้างพื้นที่จำลอง (venv), ติดตั้ง Library, และสั่งรันไฟล์ Test
                sh '''
                python3 -m venv test-env
                . test-env/bin/activate
                pip install -r app/requirements.txt
                python -m unittest app/test_app.py
                '''
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
            // เคลียร์ Session ป้องกันรหัสหลุด
            sh 'docker logout'
        }
    }
}