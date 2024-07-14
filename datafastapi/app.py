import warnings

import pandas as pd
import uvicorn
from fastapi import FastAPI
from loguru import logger
from pymongo import MongoClient

# Configurar logging
logger.add(
    "datafastapi/logs/app.log", rotation="500 MB"
)  # Salvar logs em arquivo com rotação a cada 500 MB
warnings.filterwarnings("always")  # Exibir todos os warnings

# Importações do seu projeto
from src.contrato import NovasMetricasClienteBase

app = FastAPI()

# Conectar ao MongoDB
try:
    logger.info("Tentando conectar ao MongoDB...")
    client = MongoClient("mongodb://localhost:27017/")
    logger.info("Conexão com MongoDB estabelecida com sucesso.")
except Exception as e:
    logger.error(f"Erro ao conectar ao MongoDB: {e}")
    raise

# Caminho do arquivo CSV com os dados transformados
csv_path = "data/novas_metricas_clientes_transformadas.csv"


# Função para carregar os dados transformados no MongoDB
def carregar_dados():
    logger.info("Iniciando o carregamento dos dados transformados no MongoDB.")
    db = client["ecommerce"]
    collection = db["metricas_clientes"]

    try:
        logger.info("Limpando a coleção antes de carregar novos dados.")
        collection.delete_many(
            {}
        )  # Limpar coleção antes de carregar novos dados

        logger.info(
            f"Lendo os dados transformados do arquivo CSV: {csv_path}."
        )
        dados_transformados = pd.read_csv(csv_path)

        # Verificando se o DataFrame foi lido corretamente
        if dados_transformados.empty:
            logger.warning("O DataFrame lido do CSV está vazio.")

        # Transformar o DataFrame em uma lista de dicionários para inserção no MongoDB
        logger.info("Transformando o DataFrame em uma lista de dicionários.")
        dados = dados_transformados.to_dict(orient="records")

        # Inserir os dados no MongoDB
        logger.info("Inserindo os dados no MongoDB.")
        collection.insert_many(dados)
        logger.info("Dados carregados com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        raise


@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Evento de startup iniciado.")
        carregar_dados()
        logger.info("Evento de startup concluído.")
    except Exception as e:
        logger.error(f"Erro durante o evento de startup: {e}")
        raise


if __name__ == "__main__":
    try:
        logger.info("Iniciando o servidor FastAPI.")
        uvicorn.run(app, host="0.0.0.0", port=8002)
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor FastAPI: {e}")
        raise
