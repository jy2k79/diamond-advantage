#!/bin/bash
# Launch The Diamond Advantage app
# Usage: ./run.sh

echo "💎 Launching The Diamond Advantage..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""

pip install -r requirements.txt -q 2>/dev/null
streamlit run diamond_advantage.py --server.headless true
