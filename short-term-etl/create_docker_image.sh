docker buildx build --provenance=False --platform=linux/amd64 -t c19-ajldka-short-term-etl:latest .

aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com

docker tag c19-ajldka-short-term-etl:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-ajldka-lmnh-plants:latest

docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-ajldka-lmnh-plants:latest