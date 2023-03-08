```
Installation:
-------------

apt-get update
curl -fsSL test.docker.com -o get-docker.sh && sh get-docker.sh
docker version

Run jenkins on docker:
----------------------

docker run -p 8080:8080 -p 50000:50000 -d -v
jenkins_home:/var/jenkins_home jenkins/jenkins:lts

```
