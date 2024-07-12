# Use uma imagem base oficial do Python
FROM python:3.12

# Instale o Poetry
RUN pip install poetry

# Instale o Poetry
RUN pip install pipx


# Instale o Poetry
RUN pipx install uvicorn

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY poetry.lock pyproject.toml ./
COPY requirements.txt .

# Instale as dependências do projeto
RUN poetry install --no-dev


# Copie todo o código do projeto para o contêiner
COPY . .

# Executar a aplicação em outras portas:
#RUN uvicorn datafastapi.app:app --reload --port 8001


# Exponha a porta na qual a aplicação irá rodar (se necessário)
EXPOSE 8001


