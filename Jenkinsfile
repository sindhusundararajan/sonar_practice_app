pipeline {
    agent any

    environment {
        // Keeps your functional web credential token injection
        SONAR_TOKEN = credentials('sonar-token') 
        
        // CRITICAL: Dynamically pulls the installation directory configured in the UI
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
                    // Directs execution via the absolute tool path variable
                    sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner -Dsonar.token=${SONAR_TOKEN}"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        echo "Waiting for SonarQube task to finish processing..."
                        
                        def status = ""
                        // Loop and check the SonarQube API until the analysis state is finalized
                        while (status != "SUCCESS" && status != "FAILED" && status != "CANCELED") {
                            // Give SonarQube 10 seconds between checks to process background metrics
                            sleep 10
                            
                            // FIXED: Complete URL routing through host.docker.internal:9000
                            def response = sh(
                                script: "curl -s -u ${SONAR_TOKEN}: http://docker.internal",
                                returnStdout: true
                            ).trim()
                            
                            // Parse out the current execution status using standard text pattern matching
                            if (response.contains('"status":"SUCCESS"')) {
                                status = "SUCCESS"
                            } else if (response.contains('"status":"FAILED"')) {
                                status = "FAILED"
                            } else if (response.contains('"status":"PENDING"') || response.contains('"status":"IN_PROGRESS"')) {
                                status = "IN_PROGRESS"
                            } else {
                                status = "UNKNOWN"
                            }
                            echo "Current Analysis Status: ${status}"
                        }
                        
                        // FIXED: Complete URL routing through host.docker.internal:9000
                        def gateResponse = sh(
                            script: "curl -s -u ${SONAR_TOKEN}: http://docker.internal",
                            returnStdout: true
                        ).trim()
                        
                        echo "Quality Gate Raw Response: ${gateResponse}"
                        
                        if (gateResponse.contains('"status":"ERROR"')) {
                            error "Quality Gate Failed! Check your SonarQube Dashboard at http://localhost:9000"
                        } else {
                            echo "Quality Gate Passed Successfully!"
                        }
                    }
                }
            }
        }
    }
}
