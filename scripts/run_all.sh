#!/bin/bash
# ============================================
# Complete Demo Script - Run All Examples
# ============================================

ES_HOST="http://localhost:9200"

echo "============================================"
echo "ELASTICSEARCH COMPLETE DEMO"
echo "============================================"

# Check if Elasticsearch is running
echo "Checking Elasticsearch connection..."
if curl -s "$ES_HOST" > /dev/null; then
    echo "✓ Elasticsearch is running"
else
    echo "✗ Elasticsearch is not running!"
    echo "Please start Elasticsearch first:"
    echo "  docker-compose up -d"
    exit 1
fi

echo ""
echo "Running basic commands..."
./01_basic_commands.sh

echo ""
echo "Running queries..."
./02_queries.sh

echo ""
echo "Running filters and aggregations..."
./03_filters_aggregations.sh

echo ""
echo "============================================"
echo "DEMO COMPLETE!"
echo "============================================"
echo ""
echo "Access the following URLs in your browser:"
echo "  - Elasticsearch: http://localhost:9200"
echo "  - Kibana: http://localhost:5601"
echo "  - Elasticsearch Head: http://localhost:9100"
