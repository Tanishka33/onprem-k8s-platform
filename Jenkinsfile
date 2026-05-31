pipeline {
    agent {
        label 'ec2-agent'
    }

    stages {
        stage('Repository Verification') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                cd backend
                python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                cd backend
                pytest tests -v
                '''
            }
        }
        
        stage('Build Backend Image') {
            steps {
                sh '''
                docker build \
                -t tanishkaborade/feedback-backend:${BUILD_NUMBER} \
                backend
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }
        
        stage('Push Backend Image') {
            steps {
                sh '''
                docker push tanishkaborade/feedback-backend:${BUILD_NUMBER}
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build \
                -t tanishkaborade/feedback-frontend:${BUILD_NUMBER} \
                frontend
                '''
            }
        }

        stage('Push Frontend Image') {
            steps {
                sh '''
                docker push tanishkaborade/feedback-frontend:${BUILD_NUMBER}
                '''
            }
        }

        stage('Verify Images') {
            steps {
                sh '''
                docker images | grep feedback
                '''
            }
        }
        stage('Verify Kubernetes Cluster') {
            steps {
                sh '''
                kubectl get nodes
                kubectl get ns
                '''
            }
        }
        stage('Deploy Backend') {
            steps {
                sh '''
                kubectl set image deployment/backend \
                backend=tanishkaborade/feedback-backend:${BUILD_NUMBER} \
                -n shared-apps
        
                kubectl rollout status deployment/backend \
                -n shared-apps
                '''
            }
        }
        stage('Deploy Frontend') {
            steps {
                sh '''
                kubectl set image deployment/frontend \
                frontend=tanishkaborade/feedback-frontend:${BUILD_NUMBER} \
                -n shared-apps
        
                kubectl rollout status deployment/frontend \
                -n shared-apps
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline Finished'
        }

        success {
            echo 'Backend and Frontend Docker Images Built and Pushed Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}
