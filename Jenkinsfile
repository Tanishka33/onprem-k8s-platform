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
