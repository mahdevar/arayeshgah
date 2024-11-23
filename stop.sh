docker container stop $(docker container ls -a -q)
docker container rm --force $(docker container ls -a -q)
docker rm $(docker kill $(docker ps -a -q))
docker rmi -f $(docker images -a -q)
docker rmi $(docker images -q)
docker volume rm -f $(docker volume ls -q)
docker system prune -a -f