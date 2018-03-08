

### jenkins.alv.pub Function
Auto deploy all my service configuration file and bash scripts and python scripts and my codes.

### software installation

- Install docker-latest service
```bash
# yum install docker-latest -y # Install docker-latest
```
- Start docker-latest service
```bash
# systemctl start docker-latest
# systemctl enable docker-latest
```

### pull jenkins image

- [x] docker jenkins image user manual</br>

https://hub.docker.com/_/jenkins/
```bash
# docker pull jenkins
```

- [x] run docker container
国内网络环境使得jenkins可能无法成功自动下载到一些插件，所以我是在海外的服务器上启动jenkins docker容器了，在海外的服务器上下载好了插件，然后将/jenkins目录copy了过来用的。 
```bash
# docker run -d -it --name jenkins -p 80:8080 -p 50000:50000 -v /jenkins/:/var/jenkins_home -v /etc/localtime:/etc/localtime --restart on-failure jenkins
```
主要数据目录就是/jenkins目录了，映射到容器的/var/jenkins_home目录里，所以即使删除这个容器，只有要本地的/jenkins目录里的数据还在，重新创建一个容器的时候加你/jenkins目录重新挂进去后启动容器，看到访问到的内容就还是和之前的一样，还是以前的那些数据。
