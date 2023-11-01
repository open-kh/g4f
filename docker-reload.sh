# docker run -d -p 5000 api_ai_chatbot:tag
# docker rmi -f $(docker ps -a -q) # remove image

docker restart $(docker ps -a -q) #stop container
# docker rm -f $(docker ps -a -q) # remove container
# docker ps -al
