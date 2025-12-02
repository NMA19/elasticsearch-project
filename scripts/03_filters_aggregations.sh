#!/bin/bash
# ============================================
# Elasticsearch Filters and Aggregations
# ============================================

ES_HOST="http://localhost:9200"

echo "============================================"
echo "1. FILTER CONTEXT - More Efficient for Exact Matches"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "category": "electronics" } },
        { "range": { "price": { "gte": 500, "lte": 1500 } } },
        { "term": { "in_stock": true } }
      ]
    }
  }
}
'

echo ""
echo "============================================"
echo "2. COMBINED QUERY AND FILTER"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "description": "laptop smartphone" } }
      ],
      "filter": [
        { "term": { "category": "electronics" } },
        { "range": { "price": { "lte": 2000 } } }
      ]
    }
  }
}
'

echo ""
echo "============================================"
echo "3. AGGREGATION - Terms (Group by Category)"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "4. AGGREGATION - Stats (Price Statistics)"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "price_stats": {
      "stats": {
        "field": "price"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "5. AGGREGATION - Extended Stats"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "price_extended_stats": {
      "extended_stats": {
        "field": "price"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "6. AGGREGATION - Avg, Min, Max, Sum"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "avg_price": { "avg": { "field": "price" } },
    "min_price": { "min": { "field": "price" } },
    "max_price": { "max": { "field": "price" } },
    "total_price": { "sum": { "field": "price" } }
  }
}
'

echo ""
echo "============================================"
echo "7. AGGREGATION - Range Buckets"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 200 },
          { "from": 200, "to": 500 },
          { "from": 500, "to": 1000 },
          { "from": 1000 }
        ]
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "8. AGGREGATION - Date Histogram"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "products_over_time": {
      "date_histogram": {
        "field": "created_at",
        "calendar_interval": "month"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "9. NESTED AGGREGATION - Stats per Category"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category"
      },
      "aggs": {
        "avg_price": {
          "avg": {
            "field": "price"
          }
        },
        "price_stats": {
          "stats": {
            "field": "price"
          }
        }
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "10. FILTER AGGREGATION"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "in_stock_products": {
      "filter": {
        "term": { "in_stock": true }
      },
      "aggs": {
        "avg_price": {
          "avg": { "field": "price" }
        }
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "11. TOP HITS AGGREGATION"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": {
        "field": "category"
      },
      "aggs": {
        "top_products": {
          "top_hits": {
            "size": 2,
            "sort": [{ "price": "desc" }],
            "_source": ["name", "price"]
          }
        }
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "12. CARDINALITY AGGREGATION (Count Distinct)"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "unique_categories": {
      "cardinality": {
        "field": "category"
      }
    }
  }
}
'

echo ""
echo "Done! Filter and aggregation examples executed."
