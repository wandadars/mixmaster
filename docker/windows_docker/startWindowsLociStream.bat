::Windows bat file for starting up the container
SET streamtag="stream_v206"

docker start %streamtag%
docker exec -it %streamtag% /bin/bash --rcfile /opt/Loci-Stream/image_env_setup.sh
