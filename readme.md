docker build -t kubecel-api:0.0.1 -f ./api/Dockerfile .
docker build -t kubecel-worker:0.0.1 -f ./worker/Dockerfile .
docker compose up
