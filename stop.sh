docker rm $(docker kill $(docker ps -aq))
docker rmi -f $(docker images -a -q)
docker container stop $(docker container ls --all --quiet)
docker container rm --force $(docker container ls --all --quiet)
docker rmi $(docker images -q)
docker volume rm --force $(docker volume ls --quiet)
docker system prune -a -f