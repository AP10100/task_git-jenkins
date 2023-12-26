pipeline {
    agent any

    stages {
        stage('Print Workspace Path') {
            steps {
                script {
                    def workspacePath = pwd()
                    echo "Current workspace path: ${workspacePath}"
                }
            }
        }

        // Add more stages as needed
    }

    post {
        always {
            echo 'Pipeline execution completed'
        }
    }
}
