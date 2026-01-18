#!/bin/bash
echo "Building Antigravity Gemini Assist Extension..."

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed."
    exit 1
fi

echo "Installing dependencies..."
npm install

echo "Compiling..."
npm run compile

echo "Packaging..."
# Try using local vsce
if [ -f "./node_modules/.bin/vsce" ]; then
    ./node_modules/.bin/vsce package
else
    # Try npx
    npx -y @vscode/vsce package
fi

echo "Done! You should see a .vsix file in this directory."
