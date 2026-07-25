pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonar-token') // set this up in Jenkins Credentials first
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sindhusundararajan/sonar_practice_app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh './venv/bin/pytest tests/ -v --junitxml=test-results/results.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {  // 'SonarQube' must match the server name configured in Manage Jenkins
                    //sh 'sonar-scanner -Dsonar.login=${SONAR_TOKEN}'
                    sh "sonar-scanner \
                        -Dsonar.projectKey=sonar_practice_app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            error "Quality gate failed: ${qg.status}"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            junit 'test-results/*.xml'
        }
    }
}