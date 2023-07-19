#!/bin/bash

ExilePlatformUUID=`docker ps | grep gd_platform | awk '{print $1}'`;

if [ $ExilePlatformUUID ]; then
  docker stop $ExilePlatformUUID;
  echo "stop success";
  docker rm $ExilePlatformUUID;
  echo "rm success";
fi

echo y | docker system prune
docker build -t 'gd_platform' .
echo "build success"

# -v 宿主机目录 容器目录
docker run -v /srv/project_static:/srv/project_static -d --network host --name gd_platform gd_platform
# docker run -d --network host --name gd_platform gd_platform
# docker run -d -p 5000:5000 --name gd_platform gd_platform
echo "run success"

# cat /proc/sys/net/core/somaxconn
# echo  65535  >  /proc/sys/net/core/somaxconn