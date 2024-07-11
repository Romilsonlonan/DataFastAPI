import os  # Importa o módulo os para lidar com funcionalidades dependentes do sistema operacional
import sys  # Importa o módulo sys para acessar variáveis e funções específicas do interpretador Python
import pandas as pd  # Importa o pandas para manipulação e análise de dados
import pandera as pa  # Importa o pandera para validação de dados
import pytest  # Importa o pytest para execução de testes
from loguru import logger  # Importa o logger do loguru para logging avançado
import numpy as np  # Importa o numpy para operações matemáticas avançadas
import warnings  # Importa o módulo warnings para manipulação de avisos
import time  # Importa o módulo time para manipulação de tempo

# Adiciona o diretório pai ao path para que o Python possa encontrar os módulos dentro de src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importa a classe ou função necessária do seu módulo src.contrato
from src.contrato import MetricasClientesBase

from loguru import logger
logger.add(sys.stdout, format="{time} {level} {message}") 

# Configuração do warnings
warnings.simplefilter('always')  # Garante que todos os warnings sejam sempre mostrados

# Teste das classificações de clientes
def test_contrato_original():
    start_time = time.time()  # Obtém o tempo inicial de execução
    logger.info("--- %s seconds ---" % (time.time() - start_time))  # Loga o tempo de execução inicial
    
    satisfacoes = ["Ruim", "Excelente", "Bom"]  # Lista de diferentes níveis de satisfação
    
    # Loop sobre cada nível de satisfação
    for satisfacao in satisfacoes:
        # Cria um DataFrame de teste com dados simulados
        df_test = pd.DataFrame({
            "Classificacao_Clientes": ['Clientes_Ouro>=1001.00', 'Clientes_Prata<=1000.00', 'Clientes_Ouro>=1001.00'],
            "Nome_Clientes": ["Vicente Pinheiro", "Gerald Subram", "Isabella Murphy"],
            "Idade": ["44", "45", "21"],
            "Pesquisa": ["2", "9", "8"],
            "Satisfação": ["Ruim", "Excelente", "Bom"],
            "Marca": ["Litware", "Contoso", "Hashtag Toys"],
            "Categoria": ["Sistema de Som", "Acessórios para Câmeras", "Games"],
            "Data_Vendas": pd.to_datetime(['2017-06-01', '2017-06-01', '2017-06-01']),
            "Custo_Unitario": [367.43, 121.45, 14.28],
            "Preco_Unitario": [1109, 366.55, 28],
            "Qtd_Vendida": [1.0, 5.0, 1.0],
            "Coluna_Adicional": [0, 0, 0],
        })

        # Tenta validar o DataFrame utilizando o esquema definido em MetricasClientesBase
        try:
            MetricasClientesBase.validate(df_test)
            logger.info(f"Validação bem-sucedida para a satisfação cliente: {satisfacao}")  # Loga a validação bem-sucedida
        except pa.errors.SchemaError as e:
            logger.error(f"Erro na validação para a satisfação cliente: {satisfacao} - {e}")  # Loga o erro de validação
            logger.error(e.failure_cases)  # Loga os casos de falha de validação

# Executa os testes se este script for o programa principal
if __name__ == "__main__":
    pytest.main()  # Executa os testes utilizando o pytest

