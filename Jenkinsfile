/*
Jenkins hosted in Azure VM.
http://13.76.221.196:7777/job/flexigym_security_scan/
admin:flexigym123$
spin up sonarqube serve by : docker run -d --name sonarqube -p 9000:9000 -p 9092:9092 sonarqube
sonarqube dashboard --> http://13.76.221.196:9000/dashboard?id=spring-payment
*/


pipeline {
    agent any 
    stages {
        stage ("checkout") {
            steps {
            
                checkout([$class: 'GitSCM', 
                  branches: [[name: '*/master']], 
                  doGenerateSubmoduleConfigurations: false, 
                  extensions: [], submoduleCfg: [], 
                  userRemoteConfigs: [[credentialsId: 'git2', url: 'https://github.com/zariwal/flexigym.git']]])
           }
        }
        stage ("OWASP Dependency Check") {
            steps {
                dependencyCheck additionalArguments: '--scan "./frontend" --format XML', odcInstallation: 'OWASP-Dependency-Check'
                dependencyCheckPublisher pattern: ''
            }
        }
        stage('pyLint scan') { 
            steps {
                echo "analysis using pyLint"
                sh ("pylint --rcfile=./.pylintrc subscribe-service/service || true")
                sh ("pylint --rcfile=./.pylintrc FlexiGYM-Notification-API/myapp || true")
                sh ("pylint --rcfile=./.pylintrc FlexiGymAdvertiseAPI/myapp || true")
                sh ("pylint --rcfile=./.pylintrc jwt-authentication/project || true")
                recordIssues(tools: [pyLint()])
                //recordIssues(tools: [pyLint(pattern: 'results.xml')])
            }
        }
        stage ("bandit scan") {
            steps {
                echo "analysis using pyLint"
                sh ("bandit -f xml -o bandit_results.xml -r jwt-authentication || true")
                junit 'bandit_results.xml'
                sh ("bandit -f xml -o bandit_results.xml -r subscribe-service || true")
                junit 'bandit_results.xml'
                sh ("bandit -f xml -o bandit_results.xml -r FlexiGymAdvertiseAPI || true")
                junit 'bandit_results.xml'
                sh ("bandit -f xml -o bandit_results.xml -r FlexiGYM-Notification-API || true")
                junit 'bandit_results.xml'
                
                sh ("ls -lrta")


            }
        }
        stage ("sonar scan") {
            steps {
                //run sonar analysis
                sh ('cd FlexiGYM-payment-service/payment-service && mvn clean install && mvn sonar:sonar \
                   -Dsonar.projectKey=spring-payment \
                   -Dsonar.host.url=http://13.76.221.196:9000 \
                   -Dsonar.login=e3838aeb45b8cfb1dcc5df766b107a51705aeac3')

            }
        }
        /*
        stage ('Build App') { 
            steps {
                sh ("cd web-front && docker-compose down && docker-compose build --no-cache && docker-compose up -d")
                //echo "abc"
            }
        }
        */
        stage('ZAP Scan') { 
            steps {
                sh '''#!/usr/bin/env bash

						docker rm $(docker ps -a -f status=exited -q)
						# docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

						docker pull owasp/zap2docker-stable

						echo DEBUG - mkdir -p $PWD/out
						mkdir -p $PWD/out

						echo DEBUG - chmod 777 $PWD/out
						chmod 777 $PWD/out

						test -d ${PWD}/out \\
						  && docker run -v $(pwd)/out:/zap/wrk/:rw -t owasp/zap2docker-stable zap-api-scan.py -t \"https://flexigym.rohitzariwal.co.in/#/\" -f openapi -d -r zap_scan_report.html

						echo DEBUG - Finding all files in workspace
						find $PWD


						# sudo docker cp $(sudo docker ps -l -q):/home/zap/.ZAP_D/zap.log ${WORKSPACE}
						# the goal is to get the following to work, 
						# copying the zap_scan_report.html from the Docker container 
						# to the Jenkins workspace, as a start:
						# sudo docker cp \\ 
						#   $(docker ps -l -q):/home/zap/.ZAP_D/zap_scan_report.html \\
						#   ${WORKSPACE}/zap_scan_report.html

						if test -f ${PWD}/out/zap_scan_report.html; then
						  mv ${PWD}/out/zap_scan_report.html ${PWD}
						  rm -rf ${PWD}/out
						  echo DEBUG - Finding all files in workspace
						  find $PWD
						  exit 0
						else
						  echo "zap_scan_report.html not found!"
						  exit 1
						fi'''

				publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, includes: 'zap_scan_report.html', keepAll: false, reportDir: '', reportFiles: '', reportName: 'ZAP Scan Report', reportTitles: ''])
            }
        }
        
        stage('Deploy') { 
            steps {
                echo "deploy" 
            }
        }
    }
}
