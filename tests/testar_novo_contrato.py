import os  # Importa o módulo os para manipular caminhos de arquivos
import sys  # Importa o módulo sys para manipular o caminho do sistema

import pandas as pd  # Importa a biblioteca pandas para manipulação de DataFrames
import pandera as pa  # Importa a biblioteca pandera para validação de DataFrames; Importa novamente pandera (parece duplicado)
from loguru import logger  # Importa a biblioteca loguru para logging

from src.contrato import (
    NovasMetricasClienteBase,
)  # Importa a classe NovasMetricasClienteBase do módulo src.contrato
from src.etl.transformar import (
    transforma_dados,
)  # Importa a função transforma_dados do módulo src.etl.transformar

# Adiciona o diretório pai ao caminho do sistema para permitir importações
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

# Define o caminho do arquivo CSV que contém as novas métricas de clientes transformadas
novo_contrato = "data/novas_metricas_clientes_transformadas.csv"


def test_transformacao_dados():
    # Função para testar a transformação dos dados

    # Carregar o contrato inicial a partir do arquivo CSV
    df_contrato = pd.read_csv(novo_contrato)

    # Aplicar a função de transformação nos dados carregados
    df_transformado = transforma_dados(df_contrato)

    # Testar verificação de dados faltantes
    assert (
        not df_transformado.isnull().any().any()
    ), "Dados faltantes encontrados após transformação."

    # Testar verificação de colunas duplicadas
    assert (
        not df_transformado.columns.duplicated().any()
    ), "Colunas duplicadas encontradas após transformação."

    # Testar se as novas colunas calculadas existem no DataFrame transformado
    assert (
        "Custo_Total_Unitario" in df_transformado.columns
    ), "Coluna 'Custo_Total_Unitario' não encontrada."
    assert (
        "Preco_Total_Unitario" in df_transformado.columns
    ), "Coluna 'Preco_Total_Unitario' não encontrada."
    assert (
        "Sem_ICMS_Custo" in df_transformado.columns
    ), "Coluna 'Sem_ICMS_Custo' não encontrada."
    assert (
        "Sem_ICMS_Preco" in df_transformado.columns
    ), "Coluna 'Sem_ICMS_Preco' não encontrada."
    assert (
        "Dif_ICMS_Custo" in df_transformado.columns
    ), "Coluna 'Dif_ICMS_Custo' não encontrada."
    assert (
        "Dif_ICMS_Preco" in df_transformado.columns
    ), "Coluna 'Dif_ICMS_Preco' não encontrada."

    # Validar os dados transformados usando Pandera com o novo contrato
    try:
        NovasMetricasClienteBase.validate(df_transformado, lazy=True)
    except pa.errors.SchemaErrors as exc:
        # Caso ocorra um erro de validação, o teste falha e a mensagem de erro é exibida
        assert False, f"Erro de validação do schema: {exc}"

    # Imprimir mensagem indicando que os testes de transformação de dados passaram com sucesso
    print("Testes de transformação de dados passaram com sucesso.")
