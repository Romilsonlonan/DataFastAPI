from loguru import logger  # Importa o logger do loguru para logging avançado
import pandas as pd
import pandera as pa  # Importa o pandera para validação de DataFrames
from typing import Optional  # Importa Optional para tipos opcionais
import pandera.typing as Series  # Importa o pandas para manipulação de DataFrames

# Define um modelo de DataFrame usando pandera
class MetricasFinanceirasBase(pa.DataFrameModel):
    # Define os tipos e restrições das colunas do DataFrame
    Classificacao_Clientes: Series[str]  
    Nome_Clientes: Series[str]  
    Idade: Series[int]
    Pesquisa: Series[int] 
    Satisfação: Series[str] 
    Marca: Series[str] 
    Categoria: Series[str] 
    Data_Vendas: Series[pa.DateTime]  
    Custo_Unitario: Series[float] = pa.Field(ge=0) 
    Preco_Unitario: Series[float] = pa.Field(ge=0) 
    Qtd_Vendida: Series[int] = pa.Field(gt=0)  
    Coluna_Adicional: Optional[str] 

    
    # Configurações adicionais para o modelo
    class Config:
        strict = True  # Exige que o DataFrame tenha exatamente as colunas definidas
        coerce = True  # Converte tipos de dados automaticamente

    # Define uma verificação para a coluna Classificacao_Clientes
    @pa.check(
        "Classificacao_Clientes",
        name="Checagem de código Classificacao de Clientes",
        error="Checagem de Código de Classificação de Clientes é Inválido"
    )
    def check_codigo_setor(cls, codigo: pd.Series) -> pd.Series:
        # Verifica se a coluna começa com os códigos especificados
        return codigo.str.startswith(('Clientes_Ouro>=1001.00', 'Clientes_Prata<=1000.00'))