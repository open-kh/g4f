date=$(date '+%Y-%m-%d %H:%M:%S')
git add .
git commit -m"upgrade api ${date}"
git status
git push app g4f