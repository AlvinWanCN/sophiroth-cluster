openstack
#################


.. contents::


配置数据库
`````````````````

因为我已经存在一个数据库集群了，所以这里省略数据库的搭建，直接使用我的数据库

.. code-block:: mysql

    mysql -uroot -p

    create database keystone;
    grant all privileges on keystone.* to 'keystone'@'localhost' identified by 'keystone';
    grant all privileges on keystone.* to 'keystone'@'%' identified by 'keystone';

    create database glance;
    grant all privileges on glance.* to 'glance'@'localhost' identified by 'glance';
    grant all privileges on glance.* to 'glance'@'%' identified by 'glance';

    create database nova;
    grant all privileges on nova.* to 'nova'@'localhost' identified by 'nova';
    grant all privileges on nova.* to 'nova'@'%' identified by 'nova';

    create database nova_api;
    grant all privileges on nova_api.* to 'nova'@'localhost' identified by 'nova';
    grant all privileges on nova_api.* to 'nova'@'%' identified by 'nova';
    create database nova_cell0;

    grant all privileges on nova_cell0.* to 'nova'@'localhost' identified by 'nova';
    grant all privileges on nova_cell0.* to 'nova'@'%' identified by 'nova';

    create database neutron;
    grant all privileges on neutron.* to 'neutron'@'localhost' identified by 'neutron';
    grant all privileges on neutron.* to 'neutron'@'%' identified by 'neutron';

    create database cinder;
    grant all privileges on cinder.* to 'cinder'@'localhost' identified by 'cinder';
    grant all privileges on cinder.* to 'cinder'@'%' identified by 'cinder';

    flush privileges;
    select user,host from mysql.user;
    show databases;


rabbitmq配置
``````````````````

详细配置点进rabbitmq1.alv.pub去看

