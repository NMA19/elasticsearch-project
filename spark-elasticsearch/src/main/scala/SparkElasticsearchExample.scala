import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.elasticsearch.spark.sql._

/**
 * Spark-Elasticsearch Integration Example
 * This example demonstrates how to read and write data between Spark and Elasticsearch
 */
object SparkElasticsearchExample {

  def main(args: Array[String]): Unit = {
    
    // Create Spark Session with Elasticsearch configuration
    val spark = SparkSession.builder()
      .appName("Spark-Elasticsearch Integration")
      .master("local[*]")
      .config("spark.es.nodes", "localhost")
      .config("spark.es.port", "9200")
      .config("spark.es.nodes.wan.only", "true")
      .config("spark.es.index.auto.create", "true")
      .getOrCreate()

    import spark.implicits._

    println("=" * 60)
    println("1. WRITING DATA FROM SPARK TO ELASTICSEARCH")
    println("=" * 60)

    // Create sample data
    val employees = Seq(
      ("1", "John Doe", "Engineering", 75000.0, "2020-01-15"),
      ("2", "Jane Smith", "Marketing", 65000.0, "2019-06-20"),
      ("3", "Bob Johnson", "Engineering", 80000.0, "2018-03-10"),
      ("4", "Alice Brown", "HR", 55000.0, "2021-08-05"),
      ("5", "Charlie Wilson", "Engineering", 90000.0, "2017-11-30"),
      ("6", "Diana Lee", "Marketing", 70000.0, "2020-04-22"),
      ("7", "Eve Davis", "Finance", 85000.0, "2019-09-12"),
      ("8", "Frank Miller", "Engineering", 95000.0, "2016-02-28")
    ).toDF("id", "name", "department", "salary", "hire_date")

    employees.show()

    // Write to Elasticsearch
    employees.write
      .format("org.elasticsearch.spark.sql")
      .option("es.resource", "employees")
      .option("es.mapping.id", "id")
      .mode("overwrite")
      .save()

    println("Data written to Elasticsearch index 'employees'")

    println("\n" + "=" * 60)
    println("2. READING DATA FROM ELASTICSEARCH TO SPARK")
    println("=" * 60)

    // Read from Elasticsearch
    val employeesFromES = spark.read
      .format("org.elasticsearch.spark.sql")
      .option("es.resource", "employees")
      .load()

    employeesFromES.show()
    employeesFromES.printSchema()

    println("\n" + "=" * 60)
    println("3. SPARK SQL OPERATIONS ON ELASTICSEARCH DATA")
    println("=" * 60)

    // Register as temp view for SQL queries
    employeesFromES.createOrReplaceTempView("employees")

    // SQL Query
    val engineeringEmployees = spark.sql("""
      SELECT name, salary 
      FROM employees 
      WHERE department = 'Engineering' 
      ORDER BY salary DESC
    """)
    
    println("Engineering employees (sorted by salary):")
    engineeringEmployees.show()

    // Department statistics
    val deptStats = spark.sql("""
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
    
    println("Department Statistics:")
    deptStats.show()

    println("\n" + "=" * 60)
    println("4. DATAFRAME TRANSFORMATIONS AND WRITE BACK")
    println("=" * 60)

    // Transform data
    val enrichedEmployees = employeesFromES
      .withColumn("salary_level", 
        when(col("salary") >= 90000, "Senior")
        .when(col("salary") >= 70000, "Mid")
        .otherwise("Junior"))
      .withColumn("annual_bonus", col("salary") * 0.1)

    enrichedEmployees.show()

    // Write transformed data to new index
    enrichedEmployees.write
      .format("org.elasticsearch.spark.sql")
      .option("es.resource", "employees_enriched")
      .option("es.mapping.id", "id")
      .mode("overwrite")
      .save()

    println("Enriched data written to 'employees_enriched' index")

    println("\n" + "=" * 60)
    println("5. READING WITH ELASTICSEARCH QUERY (PUSHDOWN)")
    println("=" * 60)

    // Read with Elasticsearch query pushdown
    val highSalaryEmployees = spark.read
      .format("org.elasticsearch.spark.sql")
      .option("es.resource", "employees")
      .option("es.query", """{"query": {"range": {"salary": {"gte": 75000}}}}""")
      .load()

    println("Employees with salary >= 75000:")
    highSalaryEmployees.show()

    println("\n" + "=" * 60)
    println("6. AGGREGATIONS IN SPARK")
    println("=" * 60)

    // Complex aggregation
    val aggregations = employeesFromES
      .groupBy("department")
      .agg(
        count("*").alias("count"),
        avg("salary").alias("avg_salary"),
        sum("salary").alias("total_salary")
      )
      .orderBy(desc("avg_salary"))

    println("Department Aggregations:")
    aggregations.show()

    // Stop Spark session
    spark.stop()
    
    println("\n" + "=" * 60)
    println("Spark-Elasticsearch Integration Complete!")
    println("=" * 60)
  }
}
