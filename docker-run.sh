docker image build -t api_ai_chatbot:tag . #5000
# docker build -t api_ai_chatbot:tag -f Dockerfile . #1337

# EXPOSE 1337 5000

# docker run -p 5000:1337 -p 1337:1337
# docker run -d -p 1337:1337 api_ai_chatbot:tag #1337

# docker run --publish 1337:1337 api_ai_chatbot:tag