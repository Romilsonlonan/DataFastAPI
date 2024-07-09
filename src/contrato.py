import time
from loguru import logger
import pandera as pa  # Importa o pandera para validação de DataFrames
from typing import Optional  # Importa Optional para tipos opcionais
from pandera.typing import Series  # Importa o pandas para manipulação de DataFrames

# Define um modelo de DataFrame usando pandera
class MetricasClientesBase(pa.DataFrameModel):
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

    # Define uma verificação para a coluna "Satisfação"
    @pa.check(
        "Satisfação",
        name = "Checagem de Pesquisa de Satisfação Clientes",
        error = "Checagem de Pesquisa de Satisfação Clientes é Inválido"
    )
    def check_satisfacao(cls, satisfacao: Series[str]) -> Series[bool]:
        # Verifica se os valores da coluna estão entre os valores especificados
        return satisfacao.isin(["Ruim", "Bom", "Excelente"])
    
    
# Define um novo modelo que herda de MetricasFinanceirasBase e adiciona novas colunas
class NovasMetricasClienteBase(MetricasClientesBase):
    Custo_Total_Unitario: Series[float] = pa.Field(ge=0)  
    Preco_Total_Unitario: Series[float] = pa.Field(ge=0)     
    Sem_ICMS_Custo: Series[float] = pa.Field(ge=0)  
    Sem_ICMS_Preco: Series[float] = pa.Field(ge=0)  
    Dif_ICMS_Custo: Series[float] = pa.Field(ge=0)  
    Dif_ICMS_Preco: Series[float] = pa.Field(ge=0)  
    
    # Configurações adicionais para o novo modelo
    class Config:
        strict = True  # Exige que o DataFrame tenha exatamente as colunas definidas
        coerce = True  # Converte tipos de dados automaticamente


if __name__ == "__main__":
    # Configuração do loguru para gravar logs em arquivo
    logger.add("logs/file_{time}.log")
    start_time = time.time()  # Marca o início da execução do script
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    
