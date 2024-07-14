import pandas as pd  # Importa a biblioteca pandas para manipulação de DataFrames
import pandera as pa  # Importa a biblioteca pandera para validação de DataFrames
from loguru import logger  # Importa a biblioteca loguru para logging

from src.contrato import \
    NovasMetricasClienteBase  # Importa o modelo de contrato de métricas de clientes

df1 = "data/base_metricas_clientes.csv"  # Define o caminho do arquivo CSV com os dados base


# Define a função de transformação de dados com uma verificação de saída usando pandera
@pa.check_output(NovasMetricasClienteBase, lazy=True)
def transforma_dados(df1: pd.DataFrame) -> pd.DataFrame:
    logger.info(
        "Iniciando transformação dos dados."
    )  # Loga o início da transformação

    # Verificar colunas duplicadas
    logger.info(
        "Verificando colunas duplicadas."
    )  # Loga a verificação de colunas duplicadas
    df1 = df1.loc[
        :, ~df1.columns.duplicated()
    ]  # Remove colunas duplicadas do DataFrame

    # Criar novas colunas: Custo_Total_Unitario e Preco_Total_Unitario
    logger.info(
        "Criando novas colunas: Custo_Total_Unitario e Preco_Total_Unitario."
    )  # Loga a criação das novas colunas
    df1["Custo_Total_Unitario"] = (
        df1["Custo_Unitario"] * df1["Qtd_Vendida"]
    )  # Calcula o custo total unitário
    df1["Preco_Total_Unitario"] = (
        df1["Preco_Unitario"] * df1["Qtd_Vendida"]
    )  # Calcula o preço total unitário

    # Converte a coluna 'Data_Vendas' para o tipo datetime e trata valores nulos
    df1.loc[:, "Data_Vendas"] = pd.to_datetime(
        df1["Data_Vendas"], errors="coerce"
    )  # Converte a coluna para datetime
    df1.loc[:, "Data_Vendas"] = (
        df1["Data_Vendas"].ffill().bfill()
    )  # Preenche valores nulos com o valor anterior ou posterior

    icms_percentual = 0.18  # Percentual padrão do ICMS

    # Calcula os valores sem ICMS e arredonda para 2 casas decimais
    df1.loc[:, "Sem_ICMS_Custo"] = (
        df1["Custo_Total_Unitario"] / (1 + icms_percentual)
    ).round(
        2
    )  # Calcula custo sem ICMS
    df1.loc[:, "Sem_ICMS_Preco"] = (
        df1["Preco_Total_Unitario"] / (1 + icms_percentual)
    ).round(
        2
    )  # Calcula preço sem ICMS

    # Calcula o valor do ICMS e arredonda para 2 casas decimais
    df1.loc[:, "Dif_ICMS_Custo"] = (
        df1["Custo_Total_Unitario"] - df1["Sem_ICMS_Custo"]
    ).round(
        2
    )  # Calcula a diferença de ICMS no custo
    df1.loc[:, "Dif_ICMS_Preco"] = (
        df1["Preco_Total_Unitario"] - df1["Sem_ICMS_Preco"]
    ).round(
        2
    )  # Calcula a diferença de ICMS no preço

    # Converte a coluna 'Idade' para int e trata valores nulos
    df1["Idade"] = (
        df1["Idade"].fillna(0).astype(int)
    )  # Preenche valores nulos com 0 e converte para inteiro

    # Validar os dados transformados usando o modelo NovasMetricasClienteBase
    try:
        df1 = NovasMetricasClienteBase.validate(
            df1, lazy=True
        )  # Valida o DataFrame transformado
        logger.warning(
            "Validação bem-sucedida dos dados transformados."
        )  # Loga sucesso na validação

        # Agrupar dados por 'Nome_Clientes' e contar as categorias de 'Pesquisa'
        df_agrupado_clientes = (
            df1.groupby("Nome_Clientes")
            .agg({"Satisfação": "value_counts", "Qtd_Vendida": "sum"})
            .unstack()
            .fillna(0)
        )  # Agrupa e conta categorias de satisfação e soma quantidade vendida
        logger.warning(
            "Analisando a relação entre a satisfação do cliente e o volume de vendas"
        )  # Loga análise de satisfação
        print(
            df_agrupado_clientes.head(10)
        )  # Exibe as 10 primeiras linhas do DataFrame agrupado

    except pa.errors.SchemaErrors as exc:
        logger.error(
            "Erro ao validar dados transformados."
        )  # Loga erro na validação dos dados
        logger.error(exc.failure_cases)  # Loga os casos de falha na validação

    return df1  # Retorna o DataFrame transformado


# Executar a função transforma_dados
if __name__ == "__main__":
    # Carregar o contrato inicial
    df_contrato = pd.read_csv(
        df1
    )  # Carrega o DataFrame a partir do arquivo CSV

    # Transformar os dados
    df2 = transforma_dados(
        df_contrato
    )  # Chama a função de transformação de dados

    # Salvar o resultado transformado
    df2.to_csv(
        "data/novas_metricas_clientes_transformadas.csv", index=False
    )  # Salva o DataFrame transformado em um novo arquivo CSV

    logger.info(
        "Transformação concluída. Resultado salvo em data/novas_metricas_clientes_transformadas.csv."
    )  # Loga a conclusão da transformação

    print(
        df2.head(10)
    )  # Exibe as 10 primeiras linhas do DataFrame transformado
