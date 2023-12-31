GPT="gpt4"
docker image build -t ${GPT}img:tag -f Dockerfile1 . #1337
docker image build -t ${GPT}:tag . #5000

# docker run -d -p 5000 api_ai_chatbot:tag
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

COUNT=6
PORT=1337
for i in $(seq 1 $COUNT)
do
    docker run -d -p ${PORT}:1337 ${GPT}:tag
    PORT=$((PORT+1))
done
docker run -d -p 1333:1333 ${GPT}img:tag
# docker run -d -p 1342:1333 ${GPT}:tag

# docker ps -al