import pandas as pd
import pandera as pa
from loguru import logger
from src.etl.transformar import transforma_dados
from src.contrato import NovasMetricasClienteBase 


novo_contrato = "data/novas_metricas_clientes_transformadas.csv"

def test_transformacao_dados():
    # Carregar o contrato inicial
    df_contrato = pd.read_csv(novo_contrato)

    # Transformar os dados
    df_transformado = transforma_dados(df_contrato)

    # Testar verificação de dados faltantes
    assert not df_transformado.isnull().any().any(), "Dados faltantes encontrados após transformação."

    # Testar verificação de colunas duplicadas
    assert not df_transformado.columns.duplicated().any(), "Colunas duplicadas encontradas após transformação."

    # Testar cálculos de novas colunas
    assert 'Custo_Total_Unitario' in df_transformado.columns, "Coluna 'Custo_Total_Unitario' não encontrada."
    assert 'Preco_Total_Unitario' in df_transformado.columns, "Coluna 'Preco_Total_Unitario' não encontrada."
    assert 'Sem_ICMS_Custo' in df_transformado.columns, "Coluna 'Sem_ICMS_Custo' não encontrada."
    assert 'Sem_ICMS_Preco' in df_transformado.columns, "Coluna 'Sem_ICMS_Preco' não encontrada."
    assert 'Dif_ICMS_Custo' in df_transformado.columns, "Coluna 'Dif_ICMS_Custo' não encontrada."
    assert 'Dif_ICMS_Preco' in df_transformado.columns, "Coluna 'Dif_ICMS_Preco' não encontrada."

    # Validar os dados transformados usando Pandera com o novo contrato
    try:
        NovasMetricasClienteBase.validate(df_transformado, lazy=True)
    except pa.errors.SchemaErrors as exc:
        assert False, f"Erro de validação do schema: {exc}"

    print("Testes de transformação de dados passaram com sucesso.")
