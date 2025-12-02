"""
PySpark - Elasticsearch Integration Example
This script demonstrates how to connect PySpark with Elasticsearch
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, sum as spark_sum, desc

def main():
    # Create Spark Session with Elasticsearch configuration
    spark = SparkSession.builder \
        .appName("PySpark-Elasticsearch Integration") \
        .master("local[*]") \
        .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
        .config("spark.es.nodes", "localhost") \
        .config("spark.es.port", "9200") \
        .config("spark.es.nodes.wan.only", "true") \
        .config("spark.es.index.auto.create", "true") \
        .getOrCreate()

    print("=" * 60)
    print("1. WRITING DATA FROM PYSPARK TO ELASTICSEARCH")
    print("=" * 60)

    # Create sample data
    data = [
        ("1", "John Doe", "Engineering", 75000.0, "2020-01-15"),
        ("2", "Jane Smith", "Marketing", 65000.0, "2019-06-20"),
        ("3", "Bob Johnson", "Engineering", 80000.0, "2018-03-10"),
        ("4", "Alice Brown", "HR", 55000.0, "2021-08-05"),
        ("5", "Charlie Wilson", "Engineering", 90000.0, "2017-11-30"),
        ("6", "Diana Lee", "Marketing", 70000.0, "2020-04-22"),
        ("7", "Eve Davis", "Finance", 85000.0, "2019-09-12"),
        ("8", "Frank Miller", "Engineering", 95000.0, "2016-02-28")
    ]
    
    columns = ["id", "name", "department", "salary", "hire_date"]
    employees_df = spark.createDataFrame(data, columns)
    
    employees_df.show()

    # Write to Elasticsearch
    employees_df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "employees_pyspark") \
        .option("es.mapping.id", "id") \
        .mode("overwrite") \
        .save()

    print("Data written to Elasticsearch index 'employees_pyspark'")

    print("\n" + "=" * 60)
    print("2. READING DATA FROM ELASTICSEARCH TO PYSPARK")
    print("=" * 60)

    # Read from Elasticsearch
    employees_from_es = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "employees_pyspark") \
        .load()

    employees_from_es.show()
    employees_from_es.printSchema()

    print("\n" + "=" * 60)
    print("3. SPARK SQL OPERATIONS ON ELASTICSEARCH DATA")
    print("=" * 60)

    # Register as temp view for SQL queries
    employees_from_es.createOrReplaceTempView("employees")

    # SQL Query
    engineering_employees = spark.sql("""
        SELECT name, salary 
        FROM employees 
        WHERE department = 'Engineering' 
        ORDER BY salary DESC
    """)
    
    print("Engineering employees (sorted by salary):")
    engineering_employees.show()

    # Department statistics
    dept_stats = spark.sql("""
        SELECT 
            department,
            COUNT(*) as employee_count,
            ROUND(AVG(salary), 2) as avg_salary,
            MIN(salary) as min_salary,
            MAX(salary) as max_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC
    """)
    
    print("Department Statistics:")
    dept_stats.show()

    print("\n" + "=" * 60)
    print("4. DATAFRAME TRANSFORMATIONS AND WRITE BACK")
    print("=" * 60)

    # Transform data
    enriched_employees = employees_from_es \
        .withColumn("salary_level", 
            when(col("salary") >= 90000, "Senior")
            .when(col("salary") >= 70000, "Mid")
            .otherwise("Junior")) \
        .withColumn("annual_bonus", col("salary") * 0.1)

    enriched_employees.show()

    # Write transformed data to new index
    enriched_employees.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "employees_enriched_pyspark") \
        .option("es.mapping.id", "id") \
        .mode("overwrite") \
        .save()

    print("Enriched data written to 'employees_enriched_pyspark' index")

    print("\n" + "=" * 60)
    print("5. READING WITH ELASTICSEARCH QUERY (PUSHDOWN)")
    print("=" * 60)

    # Read with Elasticsearch query pushdown
    high_salary_employees = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", "employees_pyspark") \
        .option("es.query", '{"query": {"range": {"salary": {"gte": 75000}}}}') \
        .load()

    print("Employees with salary >= 75000:")
    high_salary_employees.show()

    print("\n" + "=" * 60)
    print("6. AGGREGATIONS IN PYSPARK")
    print("=" * 60)

    # Complex aggregation
    aggregations = employees_from_es \
        .groupBy("department") \
        .agg(
            count("*").alias("count"),
            avg("salary").alias("avg_salary"),
            spark_sum("salary").alias("total_salary")
        ) \
        .orderBy(desc("avg_salary"))

    print("Department Aggregations:")
    aggregations.show()

    # Stop Spark session
    spark.stop()
    
    print("\n" + "=" * 60)
    print("PySpark-Elasticsearch Integration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
