# Importa Optional para definir tipos opcionais
from typing import Optional
# Importa a biblioteca pandas para manipulação de DataFrames
import pandas as pd
# Importa a biblioteca pandera para validação de DataFrames
import pandera as pa
# Importa Series do pandera para definir tipos de colunas
from pandera.typing import \
    Series


# Define um modelo de DataFrame usando pandera
class MetricasClientesBase(pa.DataFrameModel):
    # Define os tipos e restrições das colunas do DataFrame
    # Coluna para a classificação dos clientes
    Classificacao_Clientes: Series[str]
    Nome_Clientes: Series[str]  # Coluna para o nome dos clientes
    Idade: Series[int]  # Coluna para a idade dos clientes
    Pesquisa: Series[int]  # Coluna para os dados de pesquisa
    Satisfação: Series[str]  # Coluna para a satisfação dos clientes
    Marca: Series[str]  # Coluna para a marca do produto
    Categoria: Series[str]  # Coluna para a categoria do produto
    Data_Vendas: Series[pa.DateTime]  # Coluna para a data das vendas
    # Coluna para o custo unitário, com valor mínimo de 0
    Custo_Unitario: Series[float] = pa.Field(ge=0)
    # Coluna para o preço unitário, com valor mínimo de 0
    Preco_Unitario: Series[float] = pa.Field(ge=0)
    # Coluna para a quantidade vendida, com valor maior que 0
    Qtd_Vendida: Series[int] = pa.Field(gt=0)
    Coluna_Adicional: Optional[str]  # Coluna adicional que pode ser opcional

    # Configurações adicionais para o modelo
    class Config:
        strict = True  # Exige que o DataFrame tenha exatamente as colunas definidas
        coerce = True  # Converte tipos de dados automaticamente

    # Define uma verificação para a coluna "Satisfação"
    @pa.check(
        "Satisfação",  # Nome da coluna a ser verificada
        name="Checagem de Pesquisa de Satisfação Clientes",  # Nome da verificação
        # Mensagem de erro se a verificação falhar
        error="Checagem de Pesquisa de Satisfação Clientes é Inválido"
    )
    def check_satisfacao(cls, satisfacao: Series[str]) -> Series[bool]:
        # Verifica se os valores da coluna "Satisfação" estão entre os valores especificados
        return satisfacao.isin(["Ruim", "Bom", "Excelente"])

# Define um novo modelo que herda de MetricasClientesBase e adiciona novas colunas


class NovasMetricasClienteBase(MetricasClientesBase):
    # Define novas colunas adicionais com descrições e restrições
    Custo_Total_Unitario: Series[float] = pa.Field(
        ge=0, description="Custo total unitário do produto")
    Preco_Total_Unitario: Series[float] = pa.Field(
        ge=0, description="Preço total unitário do produto")
    Sem_ICMS_Custo: Series[float] = pa.Field(
        ge=0, description="Custo sem ICMS")
    Sem_ICMS_Preco: Series[float] = pa.Field(
        ge=0, description="Preço sem ICMS")
    Dif_ICMS_Custo: Series[float] = pa.Field(
        ge=0, description="Diferença de ICMS no custo")
    Dif_ICMS_Preco: Series[float] = pa.Field(
        ge=0, description="Diferença de ICMS no preço")

    # Configurações adicionais para o modelo
    class Config:
        strict = True  # Exige que o DataFrame tenha exatamente as colunas definidas
        coerce = True  # Converte tipos de dados automaticamente

    @staticmethod
    def analisar_insatisfacao(df2: pd.DataFrame) -> pd.DataFrame:
        # Adiciona uma coluna "Motivo_Insatisfacao" com base no aumento de custo ou preço
        df2['Motivo_Insatisfacao'] = df2.apply(
            lambda row: 'Aumento de Preço' if row['Preco_Unitario'] > row['Custo_Unitario'] else 'Outro', axis=1
        )
        return df2

    @staticmethod
    def analisar_aumento_preco(df2: pd.DataFrame) -> pd.DataFrame:
        # Calcula a diferença percentual do preço antes e depois do ICMS
        df2['Percentual_Aumento_Preco'] = (
            (df2['Preco_Unitario'] - df2['Sem_ICMS_Preco']) /
            df2['Sem_ICMS_Preco'] * 100
        )
        return df2
