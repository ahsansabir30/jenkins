pipeline{
        agent any
        stages{
            stage('setup'){
                steps{
                    sh "git fetch https://github.com/ahsansabir30/jenkins"
                    sh "cd jenkins-prac && cd devops-project"
                }
            }
            stage('deployment'){
                steps{
                    sh "docker-compose up -d"
                }
            }
        }
}