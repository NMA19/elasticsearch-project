#!/bin/bash
# ============================================
# Elasticsearch Basic Commands Examples
# ============================================

ES_HOST="http://localhost:9200"

echo "============================================"
echo "1. CHECK CLUSTER HEALTH"
echo "============================================"
curl -X GET "$ES_HOST/_cluster/health?pretty"

echo ""
echo "============================================"
echo "2. LIST ALL INDICES"
echo "============================================"
curl -X GET "$ES_HOST/_cat/indices?v"

echo ""
echo "============================================"
echo "3. CREATE AN INDEX"
echo "============================================"
curl -X PUT "$ES_HOST/products" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "price": { "type": "float" },
      "category": { "type": "keyword" },
      "description": { "type": "text" },
      "in_stock": { "type": "boolean" },
      "created_at": { "type": "date" }
    }
  }
}
'

echo ""
echo "============================================"
echo "4. POST - Create Document (Auto ID)"
echo "============================================"
curl -X POST "$ES_HOST/products/_doc" -H 'Content-Type: application/json' -d'
{
  "name": "Laptop Dell XPS 15",
  "price": 1299.99,
  "category": "electronics",
  "description": "High performance laptop with 16GB RAM",
  "in_stock": true,
  "created_at": "2024-01-15"
}
'

echo ""
echo "============================================"
echo "5. PUT - Create Document (Specific ID)"
echo "============================================"
curl -X PUT "$ES_HOST/products/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "iPhone 15 Pro",
  "price": 999.99,
  "category": "electronics",
  "description": "Latest Apple smartphone with A17 chip",
  "in_stock": true,
  "created_at": "2024-02-01"
}
'

curl -X PUT "$ES_HOST/products/_doc/2" -H 'Content-Type: application/json' -d'
{
  "name": "Samsung TV 55 inch",
  "price": 799.99,
  "category": "electronics",
  "description": "4K Smart TV with HDR support",
  "in_stock": false,
  "created_at": "2024-01-20"
}
'

curl -X PUT "$ES_HOST/products/_doc/3" -H 'Content-Type: application/json' -d'
{
  "name": "Nike Air Max",
  "price": 159.99,
  "category": "shoes",
  "description": "Comfortable running shoes",
  "in_stock": true,
  "created_at": "2024-02-10"
}
'

echo ""
echo "============================================"
echo "6. GET - Retrieve Document by ID"
echo "============================================"
curl -X GET "$ES_HOST/products/_doc/1?pretty"

echo ""
echo "============================================"
echo "7. GET - Search All Documents"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty"

echo ""
echo "============================================"
echo "8. PUT - Update Document (Full Replace)"
echo "============================================"
curl -X PUT "$ES_HOST/products/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "iPhone 15 Pro Max",
  "price": 1199.99,
  "category": "electronics",
  "description": "Latest Apple smartphone with A17 chip - Updated",
  "in_stock": true,
  "created_at": "2024-02-01"
}
'

echo ""
echo "============================================"
echo "9. POST - Partial Update Document"
echo "============================================"
curl -X POST "$ES_HOST/products/_update/1" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "price": 1099.99,
    "in_stock": false
  }
}
'

echo ""
echo "============================================"
echo "10. DELETE - Delete Document"
echo "============================================"
curl -X DELETE "$ES_HOST/products/_doc/3"

echo ""
echo "============================================"
echo "11. DELETE - Delete Index"
echo "============================================"
# Uncomment to delete the index
# curl -X DELETE "$ES_HOST/products"

echo ""
echo "============================================"
echo "12. BULK INSERT"
echo "============================================"
curl -X POST "$ES_HOST/products/_bulk" -H 'Content-Type: application/json' -d'
{"index":{"_id":"4"}}
{"name":"Sony Headphones WH-1000XM5","price":349.99,"category":"electronics","description":"Noise cancelling wireless headphones","in_stock":true,"created_at":"2024-02-15"}
{"index":{"_id":"5"}}
{"name":"Adidas Ultraboost","price":189.99,"category":"shoes","description":"Premium running shoes with boost technology","in_stock":true,"created_at":"2024-02-20"}
{"index":{"_id":"6"}}
{"name":"MacBook Pro 14","price":1999.99,"category":"electronics","description":"Apple laptop with M3 Pro chip","in_stock":true,"created_at":"2024-03-01"}
'

echo ""
echo "Done! Basic commands executed."
