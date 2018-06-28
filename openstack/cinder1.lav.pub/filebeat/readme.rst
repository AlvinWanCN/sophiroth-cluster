filebeat service
######################

.. contents::

Install filebeat
``````````````````````

.. code-block:: bash

    yum install filebeat -y


Configure filbeat
`````````````````````````

.. code-block:: bash

    curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/openstack/cinder1.alv.pub/filebeat/conf.d/filebeat.yml > /etc/filebeat/filebeat.yml

Startup filebeat

.. code-block:: bash

    systemctl enable filebeat
    systemctl start filebeat


