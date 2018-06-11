###################
redis.alv.pub
###################


.. contents::

Install redis
`````````````````

.. code-block::

    yum install redis -y



Configure redis
````````````````````

.. code-block::

    sed -i 's/^bind.*/bind 192.168.127.86/' /etc/redis.conf  #修改绑定IP为本机IP
    sed -i 's/^# requirepass.*/requirepass sophiroth/' /etc/redis.conf # 设置密码为sophiroth


Start redis
```````````````

.. code-block::

    systemctl enable redis
    systemctl start redis


 service port: 6379

Access redis
``````````````

.. code-block:: bash

    [root@redis ~]# redis-cli -h redis.alv.pub
    redis.alv.pub:6379> auth sophiroth
    OK
    redis.alv.pub:6379> set alvin sophiroth
    OK
    redis.alv.pub:6379> get alvin
    "sophiroth"

