```
Installation:
-------------

### Installing docker and docker-compose

# Docker:
curl -fsSL https://get.docker.com -o get-docker.sh

# Docker-compose:
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
cp $DOCKER_CONFIG/cli-plugins/docker-compose /usr/local/bin
docker compose version or docker-compose version

usermod -aG docker $USER 
su - $USER

or

sudo apt install docker.io docker-compose -y


Run jenkins on docker:
----------------------

docker run -p 8080:8080 -p 50000:50000 -d -v
jenkins_home:/var/jenkins_home jenkins/jenkins:lts

docker logs <containerid>
docker exec -it <containerid> bash

```
