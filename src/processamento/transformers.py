"""
Módulo de transformações com PySpark
Responsável por limpeza, enriquecimento e agregação
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, when, trim, lower, concat_ws, 
    to_date, year, month, dayofmonth,
    count, sum as spark_sum, avg, max as spark_max,
    row_number, broadcast
)
from pyspark.sql.window import Window
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SparkTransformer:
    """Transformações de dados com Spark"""
    
    def __init__(self, app_name: str = "DataTransformation"):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        logger.info(f"✅ SparkSession created: {app_name}")
    
    def read_parquet(self, path: str) -> DataFrame:
        """Lê dados Parquet"""
        logger.info(f"Reading from {path}")
        df = self.spark.read.parquet(path)
        logger.info(f"Schema: {df.schema}")
        return df
    
    def remove_duplicates(self, df: DataFrame, subset: Optional[List[str]] = None) -> DataFrame:
        """Remove duplicatas"""
        before = df.count()
        df_dedup = df.dropDuplicates(subset) if subset else df.dropDuplicates()
        after = df_dedup.count()
        
        logger.info(f"Removed {before - after} duplicates")
        return df_dedup
    
    def clean_strings(self, df: DataFrame, columns: Optional[List[str]] = None) -> DataFrame:
        """
        Limpa colunas string: trim, lowercase
        
        Args:
            df: DataFrame
            columns: Colunas a limpar (None = todas string)
        
        Returns:
            DataFrame limpo
        """
        if columns is None:
            columns = [field.name for field in df.schema.fields if field.dataType.typeName() == 'string']
        
        for col_name in columns:
            df = df.withColumn(col_name, trim(lower(col(col_name))))
        
        logger.info(f"Cleaned {len(columns)} string columns")
        return df
    
    def standardize_dates(self, df: DataFrame, date_columns: List[str], format: str = "yyyy-MM-dd") -> DataFrame:
        """Padroniza formato de datas"""
        for col_name in date_columns:
            df = df.withColumn(col_name, to_date(col(col_name), format))
        
        logger.info(f"Standardized {len(date_columns)} date columns")
        return df
    
    def add_date_parts(self, df: DataFrame, date_column: str) -> DataFrame:
        """Extrai year, month, day de uma coluna date"""
        df = df.withColumn("year", year(col(date_column)))
        df = df.withColumn("month", month(col(date_column)))
        df = df.withColumn("day", dayofmonth(col(date_column)))
        
        logger.info(f"Added date parts from {date_column}")
        return df
    
    def aggregate_by_group(self, df: DataFrame, group_by: List[str], 
                          agg_cols: dict) -> DataFrame:
        """
        Agregação genérica
        
        Args:
            df: DataFrame
            group_by: Colunas para agrupar
            agg_cols: Dict com agregações {'col_name': 'sum'|'avg'|'count'|'max'}
        
        Returns:
            DataFrame agregado
        """
        agg_expressions = {}
        
        for col_name, agg_func in agg_cols.items():
            if agg_func == 'sum':
                agg_expressions[col_name] = spark_sum(col_name).alias(f"{col_name}_total")
            elif agg_func == 'avg':
                agg_expressions[col_name] = avg(col_name).alias(f"{col_name}_avg")
            elif agg_func == 'count':
                agg_expressions[col_name] = count(col_name).alias(f"{col_name}_count")
            elif agg_func == 'max':
                agg_expressions[col_name] = spark_max(col_name).alias(f"{col_name}_max")
        
        df_agg = df.groupBy(*group_by).agg(*agg_expressions.values())
        logger.info(f"Aggregated by {group_by}")
        
        return df_agg
    
    def save_parquet(self, df: DataFrame, path: str, partition_by: Optional[List[str]] = None):
        """
        Salva em Parquet com compressão
        
        Args:
            df: DataFrame
            path: S3 ou local path
            partition_by: Colunas para particionar (otimiza queries)
        """
        logger.info(f"Writing {df.count()} rows to {path}")
        
        writer = df.write \
            .mode("overwrite") \
            .option("compression", "snappy")
        
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        
        writer.parquet(path)
        logger.info(f"✅ Saved to {path}")
    
    def get_data_quality_report(self, df: DataFrame) -> dict:
        """Gera relatório básico de qualidade"""
        total_rows = df.count()
        
        null_counts = {field.name: 0 for field in df.schema.fields}
        for field in df.schema.fields:
            null_counts[field.name] = df.filter(col(field.name).isNull()).count()
        
        return {
            'total_rows': total_rows,
            'null_counts': null_counts,
            'completeness': {
                k: round((total_rows - v) / total_rows * 100, 2)
                for k, v in null_counts.items()
            }
        }

# Exemplo de uso
def example_transformation():
    """Exemplo de pipeline de transformação completo"""
    transformer = SparkTransformer()
    
    # 1. Ler dados brutos
    df = transformer.read_parquet("s3://raw-data/transactions/")
    
    # 2. Limpar
    df = transformer.remove_duplicates(df, subset=['transaction_id'])
    df = transformer.clean_strings(df, columns=['user_name', 'category'])
    df = transformer.standardize_dates(df, date_columns=['transaction_date'])
    
    # 3. Enriquecer
    df = transformer.add_date_parts(df, 'transaction_date')
    
    # 4. Salvar em Silver
    transformer.save_parquet(
        df, 
        "s3://silver-data/transactions/",
        partition_by=['year', 'month']
    )
    
    # 5. Gerar relatório
    quality = transformer.get_data_quality_report(df)
    logger.info(f"Quality Report: {quality}")
    
    return df

if __name__ == '__main__':
    print("Module: Spark Transformations")
    print("Use: from src.processamento.transformers import SparkTransformer")
