mkdir -p build/
cp Dockerfile requirements.txt build/
cp -r babsproj/ build/
docker compose up -d --build