#!/bin/bash

# PPDX Web Demo Startup Script
echo "🚀 Starting PPDX Web Demo..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found!"
    echo "Please run this script from the web_demo directory:"
    echo "cd OnlineRetrievalAndQA/web_demo/"
    echo "./run.sh"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+"
    exit 1
fi

echo "🐍 Python version:"
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Check Neo4j connection (optional)
echo "🔍 Checking system prerequisites..."

# Check if Neo4j is running (optional check)
if command -v nc &> /dev/null; then
    if nc -z localhost 7687 2>/dev/null; then
        echo "✅ Neo4j appears to be running on port 7687"
    else
        echo "⚠️  Neo4j not detected on port 7687"
        echo "   The demo will run in mock mode if PPDX components are unavailable"
    fi
fi

# Check environment variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   LLM features may not work without this environment variable"
    echo "   Set it with: export OPENAI_API_KEY='your-api-key'"
fi

echo "=================================================="
echo "🌐 Starting web server..."
echo "📡 The demo will be available at: http://localhost:8000"
echo "🔗 Open this URL in your web browser"
echo "=================================================="
echo ""
echo "💡 Tips:"
echo "   - Make sure Neo4j is running for full functionality"
echo "   - Set OPENAI_API_KEY environment variable for LLM features"
echo "   - Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 app.py
