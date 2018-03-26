:: Windows batch file

SET streamtag="stream_v206"

ECHO OFF

echo "Host Info:"
echo "Username: %USERNAME%"
echo "Home: %USERPROFILE%"

SET imageName="locistream/%streamtag%_opensuse423:%streamtag%"
SET containerName=%streamtag%   

echo "Following Docker containers are present on your system:"
docker ps -a 

echo "Creating Docker Loci-Stream container %containerName%"

docker rm -f %streamtag%

docker run -it -d --name %containerName% --workdir="/home/streamuser" ^
           -v="%USERPROFILE%:/home/streamuser" %imageName% /bin/bash  ^
           --rcfile /opt/Loci-Stream/image_env_setup.sh


echo "Container %containerName% was created."
echo "Run the ./startWindowsLociStream script to launch container"
