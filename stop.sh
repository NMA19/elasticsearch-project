#!/bin/bash
# ============================================
# Stop and Cleanup Script
# ============================================

echo "Stopping all services..."
docker-compose down

echo ""
echo "To remove all data volumes, run:"
echo "  docker-compose down -v"
echo ""
echo "All services stopped."
