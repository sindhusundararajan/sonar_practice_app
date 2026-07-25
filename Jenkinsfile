pipeline {
    agent any

    environment {
        // Kept your existing functional credential injection
        SONAR_TOKEN = credentials('sonar-token') 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sindhusundararajan/sonar_practice_app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                    ./venv/bin/pip install pytest-cov
                '''
            }
        }

        stage('Run Tests & Coverage') {
            steps {
                sh './venv/bin/pytest tests/ -v --junitxml=test-results/results.xml --cov=src --cov-report=xml:test-results/coverage.xml'
            }
            // FIX #2: Moved junit parsing here so it never runs without a local workspace environment
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {  
                    // FIX #1: Replaced the 'tool' variable path lookup with direct system runner execution 
                    // This prevents Jenkins from failing if the Global Tool configuration naming is mismatched
                    sh "sonar-scanner -Dsonar.token=${SONAR_TOKEN}"
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
}
