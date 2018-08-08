<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>


### 创建并启动我的docker nginx容器

```
# cd /home/alvin/docker_service/nginx/
# mkdir -p {config,logs,www}
# ls
config  logs  www
# docker run -d -it \
 -p 80:80 -p 443:443 \
 -v `pwd`/www:/www \
 -v `pwd`/config:/etc/nginx/conf.d \
 -v `pwd`/logs:/var/log/nginx \
 -v /etc/localtime:/etc/localtime \
 --name nginx \
 --privileged=true \
 --restart=always \
 nginx
```

config 目录用于存放nginx配置的，logs目录存放日志。