#######################
mysql docker container
#######################

.. contents::


在服务器本地准备一个目录用于存放mysql 的数据
```````````````````````````````````````````````````````````````````
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