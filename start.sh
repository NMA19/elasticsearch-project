#!/bin/bash
# ============================================
# Start Script for the Project
# ============================================

echo "============================================"
echo "Starting Elasticsearch Mini Project"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo ""
echo "Starting ELK Stack with Docker Compose..."
docker-compose up -d

echo ""
echo "Waiting for Elasticsearch to be ready..."
until curl -s http://localhost:9200 > /dev/null; do
    echo "  Waiting..."
    sleep 5
done

echo ""
echo "✓ Elasticsearch is ready!"
echo ""
echo "============================================"
echo "Services Running:"
echo "============================================"
echo "  Elasticsearch:     http://localhost:9200"
echo "  Kibana:            http://localhost:5601"
echo "  Elasticsearch-Head: http://localhost:9100"
echo "  Logstash:          http://localhost:9600"
echo "============================================"
echo ""
echo "Run example scripts:"
echo "  cd scripts && ./run_all.sh"
echo ""
echo "Run Python examples:"
echo "  cd python-examples"
echo "  pip install -r requirements.txt"
echo "  python elasticsearch_python.py"
echo ""
echo "Run Spark examples:"
echo "  cd spark-elasticsearch"
echo "  python spark_es_complete_demo.py"
