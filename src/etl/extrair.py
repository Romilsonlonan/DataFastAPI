import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
import pandera as pa  # Importa a biblioteca pandera para validação de DataFrames
from loguru import logger  # Importa o loguru para logging
from src.contrato import MetricasFinanceirasBase  # Importa o modelo de validação do contrato

# Definindo o caminho do arquivo
dir_arquivo = "data/base_clientes.csv"  # Define o caminho do arquivo CSV que contém os dados

def extrai_dados(dir_arquivo: str) -> pd.DataFrame:
    try:
        # Carrega os dados originais
        df = pd.read_csv(dir_arquivo, delimiter=",", header=0)  # Lê o arquivo CSV em um DataFrame
        logger.info("Dados originais carregados.")  # Loga uma mensagem informando que os dados foram carregados
        logger.debug(f"Primeiras 20 linhas dos dados carregados: \n{df.head(20)}")  # Loga as primeiras 20 linhas do DataFrame
    except Exception as e:
        logger.error(f"Erro ao carregar os dados do arquivo {dir_arquivo}: {e}")
        return None

    # Seleciona as colunas conforme o contrato
    colunas_contrato = [
        "Classificacao_Clientes",
        "Nome_Clientes",
        "Idade",
        "Pesquisa",
        "Satisfação",
        "Marca",
        "Categoria",
        "Data_Vendas",
        "Custo_Unitario",
        "Preco_Unitario",
        "Qtd_Vendida",
    ]  # Lista das colunas que devem estar presentes conforme o contrato

    try:
        # Filtra o DataFrame para conter apenas as colunas do contrato
        df_contrato = df[colunas_contrato]  # Cria um novo DataFrame com apenas as colunas do contrato
        logger.info("Colunas selecionadas conforme o contrato.")
        logger.debug(f"Primeiras 2 linhas dos dados filtrados: \n{df_contrato.head(2)}")  # Loga as primeiras 2 linhas do DataFrame filtrado
    except KeyError as e:
        logger.error(f"Erro ao selecionar colunas do DataFrame: {e}")
        return None

    # Valida os dados do novo DataFrame
    try:
        df_contrato = MetricasFinanceirasBase.validate(df_contrato, lazy=True)  # Valida o DataFrame usando o modelo do contrato
        logger.info("Validação bem-sucedida dos dados selecionados.")  # Loga uma mensagem informando que a validação foi bem-sucedida
        logger.debug(f"Primeiras 2 linhas dos dados validados: \n{df_contrato.head(2)}")  # Loga as primeiras 2 linhas do DataFrame validado
        return df_contrato  # Retorna o DataFrame validado
    except pa.errors.SchemaErrors as exc:
        logger.error("Erro ao validar dados selecionados.")  # Loga uma mensagem de erro caso a validação falhe
        logger.error(exc.failure_cases)  # Loga os casos de falha na validação
        return None  # Retorna None em caso de falha na validação
    except Exception as e:
        logger.error(f"Erro inesperado durante a validação dos dados: {e}")
        return None

# Executa a função extrai_dados
if __name__ == "__main__":
    df1 = extrai_dados(dir_arquivo)  # Chama a função para extrair dados e atribui o resultado a df1
    # verificando se a variável df1 não é None antes de executar qualquer operação adicional com ela
    if df1 is not None: 
        try:
            df1.to_csv("data/base_metricas_clientes.csv", index=False)  # Salva o DataFrame validado em um novo arquivo CSV
            logger.info("Dados validados salvos em 'data/base_metricas_clientes.csv'.")
            logger.debug(f"Primeiras 10 linhas dos dados validados salvos: \n{df1.head(10)}")  # Loga as primeiras 10 linhas do DataFrame validado
        except Exception as e:
            logger.error(f"Erro ao salvar os dados validados: {e}")
    else:
        logger.warning("Os dados não foram validados corretamente e não serão salvos.")

