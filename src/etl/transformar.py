import pandas as pd
from loguru import logger
import pandera as pa
from src.contrato import NovasMetricasClienteBase

novo_contrato = "data/base_metricas_clientes.csv"

@pa.check_output(NovasMetricasClienteBase, lazy=True)
def transforma_dados(novo_contrato: pd.DataFrame) -> pd.DataFrame:
    logger.info("Iniciando transformação dos dados.")

    # Verificar dados faltantes
    logger.info("Verificando dados faltantes.")
    df1 = novo_contrato.dropna()

    # Verificar colunas duplicadas
    logger.info("Verificando colunas duplicadas.")
    df1 = df1.loc[:, ~df1.columns.duplicated()]

    # Criar novas colunas: Custo_Total_Unitario e Preco_Total_Unitario
    logger.info("Criando novas colunas: Custo_Total_Unitario e Preco_Total_Unitario.")
    df1['Custo_Total_Unitario'] = df1['Custo_Unitario'] * df1['Qtd_Vendida']
    df1['Preco_Total_Unitario'] = df1['Preco_Unitario'] * df1['Qtd_Vendida']
    
    df1.loc[:, "Data_Vendas"] = pd.to_datetime(df1["Data_Vendas"], errors='coerce')
    df1.loc[:, 'Data_Vendas'] = df1['Data_Vendas'].ffill().bfill()
    
    icms_percentual = 0.18  # Percentual padrão do ICMS

    # Calcula os valores sem ICMS e arredonda para 2 casas decimais
    df1.loc[:, 'Sem_ICMS_Custo'] = (df1['Custo_Total_Unitario'] / (1 + icms_percentual)).round(2)
    df1.loc[:, 'Sem_ICMS_Preco'] = (df1['Preco_Total_Unitario'] / (1 + icms_percentual)).round(2)

    # Calcula o valor do ICMS
    df1.loc[:, 'Dif_ICMS_Custo'] = (df1['Custo_Total_Unitario'] - df1['Sem_ICMS_Custo']).round(2)
    df1.loc[:, 'Dif_ICMS_Preco'] = (df1['Preco_Total_Unitario'] - df1['Sem_ICMS_Preco']).round(2)

    # Converter a coluna Idade para int e tratar valores nulos
    df1['Idade'] = df1['Idade'].fillna(0).astype(int)

    # Validar os dados transformados
    try:
        df1 = NovasMetricasClienteBase.validate(df1, lazy=True)
        logger.info("Validação bem-sucedida dos dados transformados.")
    except pa.errors.SchemaErrors as exc:
        logger.error("Erro ao validar dados transformados.")
        logger.error(exc.failure_cases)

    return df1

# Executar a função transforma_dados
if __name__ == "__main__":
    # Carregar o contrato inicial
    df_contrato = pd.read_csv(novo_contrato)

    # Transformar os dados
    df2 = transforma_dados(df_contrato)

    # Salvar o resultado transformado
    df2.to_csv("data/novas_metricas_clientes_transformadas.csv", index=False)

    logger.info("Transformação concluída. Resultado salvo em data/novas_metricas_clientes_transformadas.csv.")

    print(df2.head(10))
