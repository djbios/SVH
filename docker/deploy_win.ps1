$MEDIA_PATH="D:\\media"
docker-compose -p svh build --pull
docker-compose  -f docker-compose.yml -f docker-compose.windows.yml -p svh up -d --remove-orphans