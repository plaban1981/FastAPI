# FastAPI

# build image
docker build -t banknote .

# run the docker container
docker run -p 8000:8000 -t -i  banknote

go to docker desktop and open the browser against the image/container which is being run
