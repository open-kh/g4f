# docker run -d -p 5000 api_ai_chatbot:tag
# docker rmi -f $(docker ps -a -q) # remove image

docker stop $(docker ps -a -q) #stop container
docker rm -f $(docker ps -a -q) # remove container

GPT="gpt4"
docker image build -t gpt4:tag . #5000
docker image build -t gpt4img:tag -f Dockerfile1 . #1337
# docker image build -t ${GPT}img:tag -f Dockerfile1 . #1337
# docker image build -t ${GPT}:tag . #5000

# docker system prune -a # remove all container and image

COUNT=6
PORT=1337
for i in $(seq 1 $COUNT)
do
    docker run -d -p ${PORT}:1337 gpt4:tag
    PORT=$((PORT+1))
done

docker run -d -p 1333:1333 gpt4img:tag
# docker run -d -p 1342:1333 ${GPT}:tag

# docker ps -al
