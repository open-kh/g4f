
COUNT=6
PORT=1337
for i in $(seq 1 $COUNT)
do
    nohub python -m interference.app ${PORT} >/dev/null 2>&1 &
    echo "app ${PORT}"
    PORT=$((PORT+1))
done
sudo lsof -i -P -n | grep LISTEN