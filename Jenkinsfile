pipeline {
    agent any

    environment {
        // Keeps your functional web credential token injection
        SONAR_TOKEN = credentials('sonar-token') 
        
        // CRITICAL: Dynamically pulls the installation directory you configured in the UI
        SONAR_SCANNER_HOME = tool 'SonarScanner' 
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
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {  
                    // CRITICAL FIX: Directs execution via the absolute tool path variable
                    sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner -Dsonar.token=${SONAR_TOKEN}"
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
