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

        stage('Verify Image') {
            steps {
                sh '''
                docker images | grep feedback-backend
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline Finished'
        }

        success {
            echo 'Backend Docker Image Built Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}
