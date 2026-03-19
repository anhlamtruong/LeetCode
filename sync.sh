#!/bin/bash

# 1. Commit and Push local develop
echo "🚀 Committing and pushing develop..."
git checkout develop
git add .
read -p "Enter commit message: " msg
git commit -m "$msg"
git push origin develop

# 2. Create Pull Request (develop -> master)
# --fill automatically uses your commit message/title
echo " pull request..."
gh pr create --base master --head develop --fill

# 3. Merge the Pull Request
# --merge deletes the PR and merges into master on remote
echo "Merging PR into master..."
gh pr merge --merge --auto

# 4. Update local master
echo "🔄 Syncing local master..."
git checkout master
git pull origin master

# 5. Bring those changes back to local develop
echo "🔄 Syncing local develop..."
git checkout develop
git merge master

echo "✅ All synced! You are now back on the develop branch."