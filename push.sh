date=$(date '+%Y-%m-%d %H:%M:%S')
git status
git add .
git commit -m"upgrade api ${date}"
git push app g4f