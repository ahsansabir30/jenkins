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
                    sh "cd /home/ahsan/jenkins-prac && python3 -m venv venv && . .venv/bin/activate && pip3 install -r requirements.txt && python3 -m pytest --cov=application"
                }
            }
            stage('deployment'){
                steps{
                    sh "docker-compose up -d"
                }
            }
        }
}