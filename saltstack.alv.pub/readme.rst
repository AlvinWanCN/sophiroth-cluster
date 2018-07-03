saltstack server
########################

.. code-block:: bash


costom init start
``````````````````````````

.. code-block:: bash

    # cat /etc/rc.local
    su alvin -c "curl -s https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/saltstack.alv.pub/scripts/startup_sophirothpxe.py|python"