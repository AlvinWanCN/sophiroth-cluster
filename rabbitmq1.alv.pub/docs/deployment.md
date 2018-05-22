# RabbitMQ 消息队列

## Install RabbitMQ

```
yum -y install erlang socat rabbitmq-server
```

## Start RabbitMQ
RabbitMQ port is 5672

```
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
rabbitmq-plugins enable rabbitmq_management  #启动web插件端口15672
```

## 添加用户及密码
```
rabbitmqctl  add_user admin admin
rabbitmqctl  set_user_tags admin administrator
rabbitmqctl add_user openstack openstack
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
rabbitmqctl  set_user_tags openstack administrator
systemctl restart rabbitmq-server.service
netstat -antp|grep '5672'
```

```
rabbitmq-plugins list  #查看支持的插件
lsof -i:15672
```

#访问RabbitMQ,访问地址是http://rabbitmq1.alv.pub:15672

#默认用户名密码都是guest，浏览器添加openstack用户到组并登陆测试