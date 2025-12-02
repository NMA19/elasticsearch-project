"""
Complete Spark-Elasticsearch Integration with Sample Data
This script can be run standalone with PySpark
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

def create_spark_session():
    """Create Spark session with Elasticsearch connector"""
    return SparkSession.builder \
        .appName("Complete Spark-Elasticsearch Demo") \
        .master("local[*]") \
        .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
        .config("spark.es.nodes", "localhost") \
        .config("spark.es.port", "9200") \
        .config("spark.es.nodes.wan.only", "true") \
        .config("spark.es.index.auto.create", "true") \
        .getOrCreate()


def demo_write_to_elasticsearch(spark):
    """Demonstrate writing data from Spark to Elasticsearch"""
    print("\n" + "=" * 70)
    print("WRITING DATA FROM SPARK TO ELASTICSEARCH")
    print("=" * 70)
    
    # Create sample sales data
    sales_data = [
        ("S001", "2024-01-15", "Electronics", "Laptop", 1299.99, 5, "New York"),
        ("S002", "2024-01-16", "Electronics", "Phone", 999.99, 10, "Los Angeles"),
        ("S003", "2024-01-17", "Clothing", "Jacket", 89.99, 25, "Chicago"),
        ("S004", "2024-01-18", "Electronics", "Tablet", 599.99, 8, "Houston"),
        ("S005", "2024-01-19", "Clothing", "Shoes", 129.99, 15, "Phoenix"),
        ("S006", "2024-01-20", "Electronics", "Headphones", 299.99, 20, "Philadelphia"),
        ("S007", "2024-01-21", "Home", "Chair", 199.99, 12, "San Antonio"),
        ("S008", "2024-01-22", "Home", "Table", 349.99, 6, "San Diego"),
        ("S009", "2024-01-23", "Electronics", "Camera", 799.99, 4, "Dallas"),
        ("S010", "2024-01-24", "Clothing", "T-Shirt", 29.99, 50, "San Jose"),
    ]
    
    schema = StructType([
        StructField("sale_id", StringType(), False),
        StructField("sale_date", StringType(), False),
        StructField("category", StringType(), False),
        StructField("product", StringType(), False),
        StructField("price", DoubleType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("city", StringType(), False)
    ])
    
    sales_df = spark.createDataFrame(sales_data, schema)
    
    # Add calculated columns
    sales_df = sales_df \
        .withColumn("total_amount", col("price") * col("quantity")) \
        .withColumn("sale_timestamp", to_timestamp(col("sale_date")))
    
    print("\nSales Data:")
    sales_df.show(truncate=False)
    
    # Write to Elasticsearch
    sales_df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "spark_sales") \
        .option("es.mapping.id", "sale_id") \
        .mode("overwrite") \
        .save()
    
    print("✓ Data written to 'spark_sales' index")
    return sales_df


def demo_read_from_elasticsearch(spark):
    """Demonstrate reading data from Elasticsearch to Spark"""
    print("\n" + "=" * 70)
    print("READING DATA FROM ELASTICSEARCH TO SPARK")
    print("=" * 70)
    
    # Read from Elasticsearch
    sales_df = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "spark_sales") \
        .load()
    
    print("\nData from Elasticsearch:")
    sales_df.show(truncate=False)
    
    print("\nSchema:")
    sales_df.printSchema()
    
    return sales_df


def demo_spark_sql_analytics(spark, df):
    """Demonstrate SQL analytics on Elasticsearch data"""
    print("\n" + "=" * 70)
    print("SPARK SQL ANALYTICS ON ELASTICSEARCH DATA")
    print("=" * 70)
    
    # Register as temp view
    df.createOrReplaceTempView("sales")
    
    # Query 1: Sales by category
    print("\n1. Sales Summary by Category:")
    spark.sql("""
        SELECT 
            category,
            COUNT(*) as num_transactions,
            SUM(quantity) as total_units,
            ROUND(SUM(total_amount), 2) as total_revenue,
            ROUND(AVG(price), 2) as avg_price
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """).show()
    
    # Query 2: Top selling products
    print("\n2. Top 5 Products by Revenue:")
    spark.sql("""
        SELECT 
            product,
            category,
            quantity,
            ROUND(total_amount, 2) as revenue
        FROM sales
        ORDER BY total_amount DESC
        LIMIT 5
    """).show()
    
    # Query 3: Sales by city
    print("\n3. Sales by City:")
    spark.sql("""
        SELECT 
            city,
            COUNT(*) as transactions,
            ROUND(SUM(total_amount), 2) as total_revenue
        FROM sales
        GROUP BY city
        ORDER BY total_revenue DESC
    """).show()


def demo_dataframe_transformations(spark, df):
    """Demonstrate DataFrame transformations and writing back"""
    print("\n" + "=" * 70)
    print("DATAFRAME TRANSFORMATIONS")
    print("=" * 70)
    
    # Add analytics columns
    enriched_df = df \
        .withColumn("revenue_tier", 
            when(col("total_amount") >= 5000, "High")
            .when(col("total_amount") >= 1000, "Medium")
            .otherwise("Low")) \
        .withColumn("discount_eligible", col("quantity") >= 10) \
        .withColumn("profit_margin", col("total_amount") * 0.3)
    
    print("\nEnriched Data:")
    enriched_df.select("sale_id", "product", "total_amount", "revenue_tier", "discount_eligible").show()
    
    # Write enriched data back to Elasticsearch
    enriched_df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "spark_sales_enriched") \
        .option("es.mapping.id", "sale_id") \
        .mode("overwrite") \
        .save()
    
    print("✓ Enriched data written to 'spark_sales_enriched' index")
    return enriched_df


def demo_elasticsearch_query_pushdown(spark):
    """Demonstrate Elasticsearch query pushdown"""
    print("\n" + "=" * 70)
    print("ELASTICSEARCH QUERY PUSHDOWN")
    print("=" * 70)
    
    # Read with ES query (pushdown to Elasticsearch)
    electronics_df = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "spark_sales") \
        .option("es.query", '{"query": {"term": {"category": "Electronics"}}}') \
        .load()
    
    print("\nElectronics only (filtered at Elasticsearch level):")
    electronics_df.show()
    
    # High value sales query
    high_value_df = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "spark_sales") \
        .option("es.query", '{"query": {"range": {"total_amount": {"gte": 3000}}}}') \
        .load()
    
    print("\nHigh value sales (>= $3000):")
    high_value_df.show()


def demo_aggregations(spark, df):
    """Demonstrate complex aggregations"""
    print("\n" + "=" * 70)
    print("COMPLEX AGGREGATIONS")
    print("=" * 70)
    
    # Aggregation with window functions
    from pyspark.sql.window import Window
    
    window_spec = Window.partitionBy("category").orderBy(desc("total_amount"))
    
    ranked_df = df \
        .withColumn("rank_in_category", row_number().over(window_spec)) \
        .withColumn("category_total", sum("total_amount").over(Window.partitionBy("category")))
    
    print("\nSales Ranked within Category:")
    ranked_df.select(
        "sale_id", "category", "product", "total_amount", 
        "rank_in_category", "category_total"
    ).show()
    
    # Summary statistics
    print("\nOverall Summary Statistics:")
    df.select(
        count("*").alias("total_transactions"),
        sum("quantity").alias("total_units_sold"),
        round(sum("total_amount"), 2).alias("total_revenue"),
        round(avg("total_amount"), 2).alias("avg_transaction_value"),
        round(min("total_amount"), 2).alias("min_transaction"),
        round(max("total_amount"), 2).alias("max_transaction")
    ).show()


def main():
    """Main function to run all demos"""
    print("\n" + "=" * 70)
    print("SPARK-ELASTICSEARCH COMPLETE INTEGRATION DEMO")
    print("=" * 70)
    
    # Create Spark session
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # 1. Write data to Elasticsearch
        sales_df = demo_write_to_elasticsearch(spark)
        
        # 2. Read data from Elasticsearch
        es_df = demo_read_from_elasticsearch(spark)
        
        # 3. SQL Analytics
        demo_spark_sql_analytics(spark, es_df)
        
        # 4. DataFrame transformations
        enriched_df = demo_dataframe_transformations(spark, es_df)
        
        # 5. Query pushdown
        demo_elasticsearch_query_pushdown(spark)
        
        # 6. Complex aggregations
        demo_aggregations(spark, es_df)
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nCreated Elasticsearch indices:")
        print("  - spark_sales")
        print("  - spark_sales_enriched")
        print("\nYou can view them in Kibana: http://localhost:5601")
        print("=" * 70)
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
