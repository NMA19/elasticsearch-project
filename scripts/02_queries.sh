#!/bin/bash
# ============================================
# Elasticsearch Queries Examples
# ============================================

ES_HOST="http://localhost:9200"

echo "============================================"
echo "1. MATCH QUERY - Full Text Search"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "description": "laptop"
    }
  }
}
'

echo ""
echo "============================================"
echo "2. MATCH_ALL QUERY - Get All Documents"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}
'

echo ""
echo "============================================"
echo "3. TERM QUERY - Exact Match (Keyword)"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "category": "electronics"
    }
  }
}
'

echo ""
echo "============================================"
echo "4. TERMS QUERY - Multiple Exact Values"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "terms": {
      "category": ["electronics", "shoes"]
    }
  }
}
'

echo ""
echo "============================================"
echo "5. RANGE QUERY - Numeric Range"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "price": {
        "gte": 100,
        "lte": 500
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "6. RANGE QUERY - Date Range"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "created_at": {
        "gte": "2024-02-01",
        "lte": "2024-03-01"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "7. BOOL QUERY - Combining Queries"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "category": "electronics" } }
      ],
      "must_not": [
        { "term": { "in_stock": false } }
      ],
      "should": [
        { "match": { "description": "laptop" } }
      ],
      "filter": [
        { "range": { "price": { "gte": 500 } } }
      ]
    }
  }
}
'

echo ""
echo "============================================"
echo "8. MULTI_MATCH QUERY - Search Multiple Fields"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "multi_match": {
      "query": "Apple",
      "fields": ["name", "description"]
    }
  }
}
'

echo ""
echo "============================================"
echo "9. WILDCARD QUERY"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "wildcard": {
      "name": {
        "value": "*phone*"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "10. PREFIX QUERY"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "prefix": {
      "name": {
        "value": "Mac"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "11. FUZZY QUERY - Typo Tolerance"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "fuzzy": {
      "name": {
        "value": "iphon",
        "fuzziness": "AUTO"
      }
    }
  }
}
'

echo ""
echo "============================================"
echo "12. EXISTS QUERY - Field Exists"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "exists": {
      "field": "description"
    }
  }
}
'

echo ""
echo "============================================"
echo "13. QUERY WITH SORTING"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  },
  "sort": [
    { "price": "desc" },
    { "created_at": "asc" }
  ]
}
'

echo ""
echo "============================================"
echo "14. QUERY WITH PAGINATION"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  },
  "from": 0,
  "size": 2
}
'

echo ""
echo "============================================"
echo "15. QUERY WITH SOURCE FILTERING"
echo "============================================"
curl -X GET "$ES_HOST/products/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  },
  "_source": ["name", "price"]
}
'

echo ""
echo "Done! Query examples executed."
