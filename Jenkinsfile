pipeline {
    agent any

    environment {
        // Keeps your existing credential injection
        SONAR_TOKEN = credentials('sonar-token') 
        // Best Practice: Dynamically grab the scanner tool path from global configuration
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
                // Grouped sh commands into a multi-line string for faster execution
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
                // Added code coverage parameters so SonarQube can track code health
                sh './venv/bin/pytest tests/ -v --junitxml=test-results/results.xml --cov=src --cov-report=xml:test-results/coverage.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // 'SonarQube' must match the server name configured in Manage Jenkins
                withSonarQubeEnv('SonarQube') {  
                    // CRITICAL FIX: Changed to double quotes so ${SONAR_TOKEN} executes properly
                    // Crucial Fix: Used absolute tool path to prevent "command not found" errors
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

    post {
        always {
            junit 'test-results/*.xml'
        }
    }
}
