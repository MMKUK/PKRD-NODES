#!/bin/bash

echo "📦 Staging approved/ folder only..."
git add approved/

echo "✍️ Committing approved nodes..."
git commit -m '✅ Auto-signed and approved new nodes'

echo "🚀 Pushing to GitHub..."
git push origin main

echo "🧹 Writing .gitignore to clean repo..."
cat <<EOL > .gitignore
*.txt
install.sh
pkrd-*
PKRD-NODES/
__pycache__/
*.log
EOL

git add .gitignore
git commit -m "🧹 Add .gitignore to keep repo clean"
git push origin main

echo "✅ All done!"
