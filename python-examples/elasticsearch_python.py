"""
Elasticsearch Python Client Examples
This script demonstrates basic CRUD operations and queries using the official Python client
"""

from elasticsearch import Elasticsearch
from datetime import datetime
import json

# Connect to Elasticsearch
es = Elasticsearch(
    hosts=["http://localhost:9200"],
    # For secured clusters:
    # basic_auth=("username", "password")
)

def pretty_print(title, response):
    """Helper function to print responses nicely"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(json.dumps(response, indent=2, default=str))


def check_connection():
    """Check if Elasticsearch is running"""
    if es.ping():
        print("✓ Connected to Elasticsearch!")
        info = es.info()
        print(f"  Cluster: {info['cluster_name']}")
        print(f"  Version: {info['version']['number']}")
        return True
    else:
        print("✗ Could not connect to Elasticsearch")
        return False


def create_index():
    """Create an index with mappings"""
    index_name = "products_python"
    
    # Delete index if exists
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    
    # Create index with mappings
    mappings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "price": {"type": "float"},
                "category": {"type": "keyword"},
                "description": {"type": "text"},
                "in_stock": {"type": "boolean"},
                "created_at": {"type": "date"}
            }
        }
    }
    
    response = es.indices.create(index=index_name, body=mappings)
    pretty_print("CREATE INDEX", response)
    return index_name


def create_document(index_name):
    """POST - Create a document with auto-generated ID"""
    doc = {
        "name": "Laptop Dell XPS 15",
        "price": 1299.99,
        "category": "electronics",
        "description": "High performance laptop with 16GB RAM",
        "in_stock": True,
        "created_at": datetime.now()
    }
    
    response = es.index(index=index_name, document=doc)
    pretty_print("POST - Create Document (Auto ID)", response)
    return response['_id']


def create_document_with_id(index_name):
    """PUT - Create documents with specific IDs"""
    documents = [
        {
            "_id": "1",
            "name": "iPhone 15 Pro",
            "price": 999.99,
            "category": "electronics",
            "description": "Latest Apple smartphone with A17 chip",
            "in_stock": True,
            "created_at": "2024-02-01"
        },
        {
            "_id": "2",
            "name": "Samsung TV 55 inch",
            "price": 799.99,
            "category": "electronics",
            "description": "4K Smart TV with HDR support",
            "in_stock": False,
            "created_at": "2024-01-20"
        },
        {
            "_id": "3",
            "name": "Nike Air Max",
            "price": 159.99,
            "category": "shoes",
            "description": "Comfortable running shoes",
            "in_stock": True,
            "created_at": "2024-02-10"
        },
        {
            "_id": "4",
            "name": "Sony Headphones WH-1000XM5",
            "price": 349.99,
            "category": "electronics",
            "description": "Noise cancelling wireless headphones",
            "in_stock": True,
            "created_at": "2024-02-15"
        },
        {
            "_id": "5",
            "name": "MacBook Pro 14",
            "price": 1999.99,
            "category": "electronics",
            "description": "Apple laptop with M3 Pro chip",
            "in_stock": True,
            "created_at": "2024-03-01"
        }
    ]
    
    for doc in documents:
        doc_id = doc.pop('_id')
        response = es.index(index=index_name, id=doc_id, document=doc)
        print(f"Created document with ID: {doc_id}")
    
    # Refresh index to make documents searchable immediately
    es.indices.refresh(index=index_name)
    print("\n✓ All documents created")


def get_document(index_name, doc_id):
    """GET - Retrieve a document by ID"""
    response = es.get(index=index_name, id=doc_id)
    pretty_print(f"GET - Document ID: {doc_id}", response)


def search_all(index_name):
    """GET - Search all documents"""
    response = es.search(index=index_name, query={"match_all": {}})
    pretty_print("GET - Search All Documents", response)


def update_document(index_name, doc_id):
    """PUT/POST - Update a document"""
    # Partial update
    response = es.update(
        index=index_name,
        id=doc_id,
        doc={
            "price": 899.99,
            "in_stock": False
        }
    )
    pretty_print(f"UPDATE - Document ID: {doc_id}", response)


def delete_document(index_name, doc_id):
    """DELETE - Delete a document"""
    response = es.delete(index=index_name, id=doc_id)
    pretty_print(f"DELETE - Document ID: {doc_id}", response)


def bulk_insert(index_name):
    """Bulk insert documents"""
    from elasticsearch.helpers import bulk
    
    documents = [
        {"_index": index_name, "_id": "6", "_source": {"name": "Adidas Ultraboost", "price": 189.99, "category": "shoes", "description": "Premium running shoes", "in_stock": True, "created_at": "2024-02-20"}},
        {"_index": index_name, "_id": "7", "_source": {"name": "Canon EOS R5", "price": 3899.99, "category": "cameras", "description": "Professional mirrorless camera", "in_stock": True, "created_at": "2024-01-10"}},
        {"_index": index_name, "_id": "8", "_source": {"name": "iPad Pro 12.9", "price": 1099.99, "category": "electronics", "description": "Apple tablet with M2 chip", "in_stock": True, "created_at": "2024-02-25"}}
    ]
    
    success, failed = bulk(es, documents)
    print(f"\n✓ Bulk insert: {success} succeeded, {len(failed)} failed")


# ============================================
# QUERIES
# ============================================

def match_query(index_name):
    """Match query - full text search"""
    response = es.search(
        index=index_name,
        query={
            "match": {
                "description": "laptop"
            }
        }
    )
    pretty_print("MATCH QUERY", response)


def term_query(index_name):
    """Term query - exact match"""
    response = es.search(
        index=index_name,
        query={
            "term": {
                "category": "electronics"
            }
        }
    )
    pretty_print("TERM QUERY", response)


def range_query(index_name):
    """Range query"""
    response = es.search(
        index=index_name,
        query={
            "range": {
                "price": {
                    "gte": 500,
                    "lte": 1500
                }
            }
        }
    )
    pretty_print("RANGE QUERY", response)


def bool_query(index_name):
    """Bool query - combining conditions"""
    response = es.search(
        index=index_name,
        query={
            "bool": {
                "must": [
                    {"match": {"category": "electronics"}}
                ],
                "must_not": [
                    {"term": {"in_stock": False}}
                ],
                "filter": [
                    {"range": {"price": {"gte": 500}}}
                ]
            }
        }
    )
    pretty_print("BOOL QUERY", response)


def aggregation_query(index_name):
    """Aggregation query"""
    response = es.search(
        index=index_name,
        size=0,
        aggs={
            "categories": {
                "terms": {"field": "category"}
            },
            "price_stats": {
                "stats": {"field": "price"}
            },
            "price_ranges": {
                "range": {
                    "field": "price",
                    "ranges": [
                        {"to": 500},
                        {"from": 500, "to": 1000},
                        {"from": 1000}
                    ]
                }
            }
        }
    )
    pretty_print("AGGREGATION QUERY", response)


def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("ELASTICSEARCH PYTHON EXAMPLES")
    print("=" * 60)
    
    # Check connection
    if not check_connection():
        return
    
    # Create index
    index_name = create_index()
    
    # CRUD Operations
    print("\n\n>>> CRUD OPERATIONS <<<")
    
    # Create
    auto_id = create_document(index_name)
    create_document_with_id(index_name)
    bulk_insert(index_name)
    
    # Read
    get_document(index_name, "1")
    search_all(index_name)
    
    # Update
    update_document(index_name, "1")
    
    # Verify update
    get_document(index_name, "1")
    
    # Delete
    delete_document(index_name, "3")
    
    # Refresh for queries
    es.indices.refresh(index=index_name)
    
    # Queries
    print("\n\n>>> QUERIES <<<")
    match_query(index_name)
    term_query(index_name)
    range_query(index_name)
    bool_query(index_name)
    
    # Aggregations
    print("\n\n>>> AGGREGATIONS <<<")
    aggregation_query(index_name)
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
