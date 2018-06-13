#######################
mysql docker container
#######################

.. contents::





在服务器本地准备一个目录用于存放mysql 的数据
```````````````````````````````````````````````````````````````````
将本地磁盘映射到容器里作为数据存放目录，那样mysql的数据是保存在本地的，即使容器被销毁，数据还在，重新启动一个容器后，使用以前的数据，会和以前的数据库一样。

.. code-block:: bash

    mkdir -p /mysqldata

启动一个mysql 5.6的docker容器
````````````````````````````````

这里我们设置mysql服务的root的密码为sophiroth
.. code-block:: bash

    docker run -d -it --name mysql -v /mysqldata/:/var/lib/mysql -v /etc/localtime:/etc/localtime -e MYSQL_ROOT_PASSWORD=sophiroth -p 3306:3306 mysql:5.6


客户端访问
```````````````````
.. code-block:: bash

    mysql -uroot -psophiroth -hsaltstack