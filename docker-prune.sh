docker stop $(docker ps -a -q) #stop container
docker rm -f $(docker ps -a -q) # remove container

docker system prune -a # remove all container and image
