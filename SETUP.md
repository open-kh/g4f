docker -v
sudo apt-get install docker
docker -v
docker --version
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
docker --version
sudo usermod -aG docker $USER

1. docker image build -t api_ai_chatbot:tag .
<!-- 2. docker build -t api_ai_chatbot:tag -f Dockerfile .   -->
   
3. docker run --publish 1337:1337 api_ai_chatbot:tag