etcd server
##################

.. contents::

Install and configure components
``````````````````````

#. Installa the package:

    .. code-block:: bash

        # yum install etcd -y


#. Edit the /etc/etcd/etcd.conf file and set the ETCD_INITIAL_CLUSTER, ETCD_INITIAL_ADVERTISE_PEER_URLS, ETCD_ADVERTISE_CLIENT_URLS, ETCD_LISTEN_CLIENT_URLS to the management IP address of the controller node to enable access by other nodes via the management network:

    .. code-block:: bash

        #[Member]
        ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
        ETCD_LISTEN_PEER_URLS="http://10.0.0.11:2380"
        ETCD_LISTEN_CLIENT_URLS="http://10.0.0.11:2379"
        ETCD_NAME="controller"
        #[Clustering]
        ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.0.0.11:2380"
        ETCD_ADVERTISE_CLIENT_URLS="http://10.0.0.11:2379"
        ETCD_INITIAL_CLUSTER="controller=http://10.0.0.11:2380"
        ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster-01"
        ETCD_INITIAL_CLUSTER_STATE="new"

Finalize installation
``````````````````````````

1. Enable and start the etcd service:

.. code-block:: bash

    # systemctl enable etcd
    # systemctl start etcd