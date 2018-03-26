# .bashrc

version_tag="mixmaster_v1"

cp docker/dockerignore ./.dockerignore
docker build -t mixmaster/${version_tag}_ubuntu1704:$version_tag  . 
