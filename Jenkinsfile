pipeline{
        agent any
        stages{
            stage('setup'){
                steps{
                    sh "git fetch https://github.com/ahsansabir30/jenkins"
                    sh "cd /home/ahsan/jenkins-prac && cd devops-project"
                }
            }
            stage('test'){
                steps{
                    sh "sudo apt install python3 python3-pip python3-venv"
                    sh "python3 -m venv venv"
                    sh "source venv/bin/activate"
                    sh "pip3 install -r requirements.txt"
                    sh "python3 -m pytest --cov=application --cov-report=html"
                }
            }
            stage('deployment'){
                steps{
                    sh "docker-compose up -d"
                }
            }
        }
}