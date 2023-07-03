1. docker image build -t api_ai_chatbot:tag .
<!-- 2. docker build -t api_ai_chatbot:tag -f Dockerfile .   -->
   
3. docker run --publish 1337:1337 api_ai_chatbot:tag