docker container stop $(docker container ls --all --quiet)
docker container rm --force $(docker container ls --all --quiet)
docker image rm --force $(docker images --all --quiet)
docker volume rm --force $(docker volume ls --quiet)
