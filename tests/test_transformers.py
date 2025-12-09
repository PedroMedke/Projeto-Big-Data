"""
Testes unitários para módulo de transformações
"""

import pytest
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from src.processamento.transformers import SparkTransformer

@pytest.fixture(scope="module")
def spark():
    """Fixture: cria SparkSession para testes"""
    spark_session = SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()
    yield spark_session
    spark_session.stop()

@pytest.fixture
def sample_df(spark):
    """Fixture: DataFrame de exemplo"""
    data = [
        ('TXN-001', 1, 'Alice Smith', 299.99, '2025-01-15', 'completed'),
        ('TXN-002', 2, 'BOB JONES', 150.00, '2025-01-15', 'completed'),
        ('TXN-001', 1, 'Alice Smith', 299.99, '2025-01-15', 'completed'),  # Duplicata
        ('TXN-003', 3, None, 500.00, '2025-01-16', 'pending'),  # Nulo em name
    ]
    
    schema = StructType([
        StructField('transaction_id', StringType()),
        StructField('user_id', IntegerType()),
        StructField('user_name', StringType()),
        StructField('amount', DoubleType()),
        StructField('date', StringType()),
        StructField('status', StringType()),
    ])
    
    return spark.createDataFrame(data, schema)

class TestSparkTransformer:
    """Testes para SparkTransformer"""
    
    def test_remove_duplicates(self, sample_df):
        """Testa remoção de duplicatas"""
        transformer = SparkTransformer()
        
        result = transformer.remove_duplicates(
            sample_df, 
            subset=['transaction_id', 'user_id']
        )
        
        assert result.count() == 3  # 4 -> 3 (remove 1 duplicata)
    
    def test_clean_strings(self, sample_df):
        """Testa limpeza de strings"""
        transformer = SparkTransformer()
        
        result = transformer.clean_strings(
            sample_df, 
            columns=['user_name', 'status']
        )
        
        # Verificar que 'BOB JONES' virou 'bob jones'
        names = result.select('user_name').collect()
        assert any('bob jones' in row.user_name for row in names if row.user_name)
    
    def test_add_date_parts(self, sample_df):
        """Testa extração de date parts"""
        from pyspark.sql.functions import to_date, col
        
        transformer = SparkTransformer()
        df_with_dates = sample_df.withColumn('date', to_date(col('date'), 'yyyy-MM-dd'))
        
        result = transformer.add_date_parts(df_with_dates, 'date')
        
        # Verificar que colunas year, month, day foram adicionadas
        assert 'year' in result.columns
        assert 'month' in result.columns
        assert 'day' in result.columns
    
    def test_get_data_quality_report(self, sample_df):
        """Testa relatório de qualidade"""
        transformer = SparkTransformer()
        
        report = transformer.get_data_quality_report(sample_df)
        
        assert 'total_rows' in report
        assert 'null_counts' in report
        assert 'completeness' in report
        assert report['total_rows'] == 4
        assert report['null_counts']['user_name'] == 1  # Uma linha tem None
        assert report['completeness']['user_name'] == 75.0  # 75% completo
    
    def test_aggregate_by_group(self, sample_df):
        """Testa agregação"""
        from pyspark.sql.functions import col
        
        transformer = SparkTransformer()
        
        result = transformer.aggregate_by_group(
            sample_df,
            group_by=['user_id'],
            agg_cols={'amount': 'sum'}
        )
        
        assert result.count() == 3  # 3 usuários
        # Verificar que coluna sum foi criada
        assert 'amount_total' in result.columns

class TestDataQuality:
    """Testes de qualidade de dados"""
    
    def test_null_handling(self, sample_df):
        """Testa manipulação de nulos"""
        from pyspark.sql.functions import col
        
        # Contar nulos
        null_count = sample_df.filter(col('user_name').isNull()).count()
        assert null_count == 1
    
    def test_duplicates_detection(self, sample_df):
        """Testa detecção de duplicatas"""
        from pyspark.sql.functions import row_number, col
        from pyspark.sql.window import Window
        
        window = Window.partitionBy('transaction_id', 'user_id').orderBy('transaction_id')
        df_with_row_num = sample_df.withColumn('row_num', row_number().over(window))
        
        duplicates = df_with_row_num.filter(col('row_num') > 1).count()
        assert duplicates == 1

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
