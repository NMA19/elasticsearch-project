# Elasticsearch Mini Project

A comprehensive project demonstrating Elasticsearch operations, ELK Stack, and Spark integration for Big Data analysis.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Components](#components)
- [Usage Guide](#usage-guide)
- [Spark-Elasticsearch Integration](#spark-elasticsearch-integration)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

Before running this project, make sure you have:

- **Docker** (version 20.0+)
- **Docker Compose** (version 2.0+)
- **Python 3.8+** (for Python examples)
- **Java 11+** (for Spark examples)
- **curl** (for bash scripts)

### Install Docker (Ubuntu/Debian)

```bash
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Add user to docker group (logout/login after)
sudo usermod -aG docker $USER
```

### Install Python Dependencies

```bash
pip install elasticsearch pyspark pandas
```

---

## 📁 Project Structure

```
elasticsearch-project/
│
├── docker-compose.yml              # ELK Stack + Elasticsearch-Head
├── start.sh                        # Start all services
├── stop.sh                         # Stop all services
│
├── logstash/
│   ├── config/logstash.yml         # Logstash configuration
│   └── pipeline/logstash.conf      # Logstash pipeline
│
├── scripts/
│   ├── 00_installation.sh          # Installation guide
│   ├── 01_basic_commands.sh        # CRUD operations (POST, GET, PUT, DELETE)
│   ├── 02_queries.sh               # Search queries examples
│   ├── 03_filters_aggregations.sh  # Filters and aggregations
│   └── run_all.sh                  # Run all demo scripts
│
├── spark-elasticsearch/
│   ├── build.sbt                   # Scala build configuration
│   ├── src/main/scala/
│   │   └── SparkElasticsearchExample.scala
│   ├── pyspark_elasticsearch.py    # PySpark basic example
│   └── spark_es_complete_demo.py   # Complete PySpark demo
│
├── python-examples/
│   ├── elasticsearch_python.py     # Python client examples
│   └── requirements.txt            # Python dependencies
│
└── notebooks/
    └── elasticsearch_demo.ipynb    # Interactive Jupyter notebook
```

---

## 🚀 Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/elasticsearch-project.git
cd elasticsearch-project
```

### Step 2: Start the ELK Stack

```bash
./start.sh
```

Wait ~30 seconds for all services to start.

### Step 3: Verify Installation

```bash
# Check Elasticsearch
curl http://localhost:9200

# Check cluster health
curl http://localhost:9200/_cluster/health?pretty
```

### Step 4: Access Web Interfaces

| Service | URL | Description |
|---------|-----|-------------|
| **Elasticsearch** | http://localhost:9200 | REST API |
| **Kibana** | http://localhost:5601 | Visualization & Management |
| **Elasticsearch-Head** | http://localhost:9100 | Cluster Monitoring UI |
| **Logstash** | http://localhost:9600 | Pipeline Monitoring |

---

## 🧩 Components

### 1. Elasticsearch
- Distributed search and analytics engine
- RESTful API for CRUD operations
- Full-text search capabilities

### 2. Logstash
- Data processing pipeline
- Collects, transforms, and sends data to Elasticsearch

### 3. Kibana
- Data visualization dashboard
- Index management
- Dev Tools for queries

### 4. Elasticsearch-Head
- Web interface for cluster management
- Visual representation of indices and data

---

## 📖 Usage Guide

### Running Bash Scripts

```bash
cd scripts

# Run all examples
./run_all.sh

# Or run individually:
./01_basic_commands.sh      # CRUD operations
./02_queries.sh             # Search queries
./03_filters_aggregations.sh # Aggregations
```

### Basic CRUD Operations

#### Create (POST) - Auto-generated ID
```bash
curl -X POST "localhost:9200/products/_doc" -H 'Content-Type: application/json' -d'
{
  "name": "iPhone 15",
  "price": 999.99,
  "category": "electronics"
}'
```

#### Create (PUT) - Specific ID
```bash
curl -X PUT "localhost:9200/products/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "MacBook Pro",
  "price": 1999.99,
  "category": "electronics"
}'
```

#### Read (GET)
```bash
# Get single document
curl -X GET "localhost:9200/products/_doc/1?pretty"

# Search all documents
curl -X GET "localhost:9200/products/_search?pretty"
```

#### Update (POST)
```bash
curl -X POST "localhost:9200/products/_update/1" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "price": 1899.99
  }
}'
```

#### Delete (DELETE)
```bash
curl -X DELETE "localhost:9200/products/_doc/1"
```

### Search Queries

```bash
# Match query (full-text search)
curl -X GET "localhost:9200/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": { "name": "iPhone" }
  }
}'

# Term query (exact match)
curl -X GET "localhost:9200/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": { "category": "electronics" }
  }
}'

# Range query
curl -X GET "localhost:9200/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "price": { "gte": 500, "lte": 1500 }
    }
  }
}'

# Bool query (combining conditions)
curl -X GET "localhost:9200/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [{ "match": { "category": "electronics" }}],
      "filter": [{ "range": { "price": { "lte": 1000 }}}]
    }
  }
}'
```

### Aggregations

```bash
# Group by category
curl -X GET "localhost:9200/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": { "field": "category" }
    }
  }
}'

# Price statistics
curl -X GET "localhost:9200/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "price_stats": {
      "stats": { "field": "price" }
    }
  }
}'
```

---

## 🔗 Spark-Elasticsearch Integration

### Run PySpark Example

```bash
cd spark-elasticsearch

# Install PySpark
pip install pyspark

# Run the complete demo
python spark_es_complete_demo.py
```

### PySpark Code Example

```python
from pyspark.sql import SparkSession

# Create Spark session with ES connector
spark = SparkSession.builder \
    .appName("Spark-ES") \
    .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", "9200") \
    .getOrCreate()

# Write DataFrame to Elasticsearch
df.write \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", "my_index") \
    .mode("overwrite") \
    .save()

# Read from Elasticsearch
df = spark.read \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", "my_index") \
    .load()

df.show()
```

---

## 🐍 Python Client Examples

```bash
cd python-examples

# Install dependencies
pip install -r requirements.txt

# Run examples
python elasticsearch_python.py
```

### Python Code Example

```python
from elasticsearch import Elasticsearch

# Connect
es = Elasticsearch(["http://localhost:9200"])

# Create document
es.index(index="products", id=1, document={
    "name": "Laptop",
    "price": 1299.99
})

# Search
results = es.search(index="products", query={
    "match": {"name": "Laptop"}
})

print(results['hits']['hits'])
```

---

## 🛠 Troubleshooting

### Elasticsearch not starting?

```bash
# Check Docker logs
docker logs elasticsearch

# Increase virtual memory (Linux)
sudo sysctl -w vm.max_map_count=262144
```

### Port already in use?

```bash
# Find process using port 9200
sudo lsof -i :9200

# Kill the process
sudo kill -9 <PID>
```

### Connection refused?

```bash
# Wait for Elasticsearch to be ready
until curl -s localhost:9200 > /dev/null; do sleep 5; done
echo "Elasticsearch is ready!"
```

### Reset everything

```bash
# Stop and remove all data
docker-compose down -v

# Start fresh
./start.sh
```

---

## 🛑 Stop Services

```bash
./stop.sh

# Or with data cleanup
docker-compose down -v
```

---

## 👥 Team Members

- Member 1 - [Role]
- Member 2 - [Role]
- Member 3 - [Role]
- Member 4 - [Role]
- Member 5 - [Role]

---

## 📚 Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Elasticsearch-Spark Connector](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html)

---

## 📄 License

This project is for educational purposes - BIDA Mini Project 02
