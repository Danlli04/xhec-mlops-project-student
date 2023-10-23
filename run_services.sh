docker build -t abalone:solution -f Dockerfile.app .
docker run -dp 0.0.0.0:8000:8001 abalone:solution
