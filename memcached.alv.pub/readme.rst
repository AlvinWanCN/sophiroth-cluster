###################
memcached.alv.pub
###################


.. contents::

Install memcached
`````````````````

.. code-block::

    yum install memcached -y





Start memcached
```````````````

.. code-block::

    systemctl enable memcached
    systemctl start memcached


 service port: 11211


查看memcached里缓存的内容
``````````````````````````````````

.. code-block:: bash

    memcached-tool localhost dump


