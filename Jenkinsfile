pipeline {
    agent {
        node {
            label 'docker'
        }
    }
    stages {
        stage('Clone') {
            steps {
                git branch: 'develop', url: 'https://github.com/harbourheading/savsa.git'
            }
        }
        stage('Setup Environment') {
            steps {
                withCredentials([file(credentialsId: 'savsaenvfile', variable: 'ENV_FILE')]) {
                    script {
                        if (!fileExists('.env')) {
                            sh 'cp ${ENV_FILE} .env'
                        } else {
                            echo '.env file already exists. Skipping copy.'
                        }
                    }
                }
            }
        }
        stage('Build') {
            steps {
                sh 'docker compose up -d --no-color --wait'
                sh 'docker compose ps'
            }
        }
        stage('Test') {
            steps {
                sh 'docker exec backend pytest'
            }
        }
    }
    post {
        always {
            sh 'docker compose down'
            sh 'docker system prune --filter "label!=database" --volumes -f'
        }
    }
}