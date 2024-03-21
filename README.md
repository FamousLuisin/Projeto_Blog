# Projeto_Blog
projeto de um blog

# Criar pasta djangoapp
- Pasta djangoapp é onde fica o projeto
- Criar o requirements.txt para ser enviado ao dockers, e baixar as bibliotecas que são necessarias
- Criar arquivo .dockerignore para ignorar arquivos desnecessarios de irem para o docker
- Criar um .env para criar as variaveis de ambiente e serem usadas no settings do projeto
- Configurar as variaveis de ambiente no settings 
- Configurar arquivos staticos e de media no settings
- Configurar na url os arquivos de media, para usar quando o debug estiver como True
- Criar arquivo Dockerfile para a configuração do docker
- Dockerfile: arquivo de instruções usadas pelo Docker ao construir uma imagem Docker (Possui todos os passos para construir a imagem)
- O dockerfile cria/biuldar/construir uma imagem ao seu gosto
- Criar o arquivo docker-compose.yml (para biuldar o docker do django e do postgresql)