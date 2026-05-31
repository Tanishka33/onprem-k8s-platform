pipeline {
    agent {
        label 'ec2-agent'
    }

    stages {

        stage('Repository Verification') {
            steps {
                echo 'Repository Cloned Successfully'

                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Backend Verification') {
            steps {
                sh '''
                cd backend
                python3 --version
                ls -la
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline Finished'
        }
    }
}
