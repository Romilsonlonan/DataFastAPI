# Importa a biblioteca os para interagir com o sistema operacional.
import os  
# Importa a biblioteca warnings para emitir avisos.
import warnings  
# Importa a biblioteca pandas, que é usada para manipulação e análise de dados.
import pandas as pd
# Importa a função load_dotenv para carregar variáveis de ambiente de um arquivo .env.
from dotenv import load_dotenv
# Importa a biblioteca loguru para registro de logs.  
from loguru import logger
# Importa a função create_engine para conectar ao banco de dados PostgreSQL.  
from sqlalchemy import create_engine  
# Importa a função extrai_dados do módulo extrair.
from src.etl.extrair import extrai_dados
# Importa a função transforma_dados do módulo transformar.  
from src.etl.transformar import transforma_dados  

# Configuração do logger para registrar logs em um arquivo com rotação de 10 MB.
logger.add("logs/application.log", rotation="10 MB", level="INFO")


# Função para carregar dados no PostgreSQL.
def carrega_dados(df2: pd.DataFrame) -> None:
    # Carrega as variáveis de ambiente do arquivo .env.
    load_dotenv(".post.env")

    # Obtém as variáveis de ambiente necessárias para a conexão com o PostgreSQL.
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    # Cria a URL de conexão com o PostgreSQL.
    POSTGRES_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Cria o engine do SQLAlchemy para se conectar ao PostgreSQL.
    engine = create_engine(POSTGRES_DATABASE_URL)

    # Define o nome da tabela onde os dados serão carregados.
    nome_da_tabela = "metricas_clientes"
    try:
        # Carrega os dados no PostgreSQL, substituindo a tabela se ela já existir.
        df2.to_sql(nome_da_tabela, engine, if_exists="replace", index=False)
        logger.info(
            f"Dados carregados com sucesso na tabela {nome_da_tabela}."
        )
    except Exception as e:
        # Registra um erro e emite um aviso se ocorrer uma exceção ao carregar os dados.
        logger.error(f"Erro ao carregar dados no PostgreSQL: {e}")
        warnings.warn(f"Erro ao carregar dados no PostgreSQL: {e}")


# Bloco principal de execução do script.
if __name__ == "__main__":
    try:
        # Inicia o processo de extração de dados.
        logger.info("Iniciando o processo de extração de dados.")
        dir_arquivo = "data/novas_metricas_clientes_transformadas.csv"
        df2 = extrai_dados(dir_arquivo)

        # Inicia o processo de transformação de dados.
        logger.info("Iniciando o processo de transformação de dados.")
        df_transformado = transforma_dados(df2)

        # Inicia o processo de carga de dados no PostgreSQL.
        logger.info("Iniciando o processo de carga de dados no PostgreSQL.")
        carrega_dados(df_transformado)

    except Exception as e:
        # Registra um erro se ocorrer uma exceção.
        logger.error(f"Erro no processo: {e}")
    else:
        # Log de conclusão do processo sem exceções.
        logger.info("Processo concluído com sucesso.")