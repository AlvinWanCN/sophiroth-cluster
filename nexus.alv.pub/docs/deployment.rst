#####################
Deploy nexus service
#####################


.. contents:: Catalog

Install java
``````````````

java download website: http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

.. code-block::

 yum install jdk-8u171-linux-x64.rpm


Install nexus
``````````````

download nexus
----------------

nexus download website: https://www.sonatype.com/oss-thank-you-tgz

.. code-block:: bash

 wget https://sonatype-download.global.ssl.fastly.net/repository/repositoryManager/oss/nexus-2.14.8-01-bundle.tar.gz

解压nexus包到指定目录

.. code-block:: bash

 tar xf nexus-2.14.8-01-bundle.tar.gz -C /usr/local/


Startup Nexus
```````````````

.. code-block:: bash

 cp /usr/local/nexus-2.14.8-01/bin/nexus /etc/init.d/
 sed  -i 's#^NEXUS_HOME.*#NEXUS_HOME=\"/usr/local/nexus-2.14.8-01/\"#' nexus
 useradd nexus
 sed -i 's/^#RUN_AS_USER.*/RUN_AS_USER=nexus/' /usr/local/nexus-2.14.8-01/bin/nexus
 /etc/init.d/nexus start

Nexus web login
`````````````````

URL:http://nexus.alv.pub:8081/nexus/

default user/password: admin/admin123

Configure nexus
````````````````

- 1, Check Repositories

- 2, Enter Central

 - 2.1,  Configure remote agent

  -- Configuraion --

  Remote Storage Location: http://maven.aliyun.com/nexus/content/groups/public/

  Central's Remote agent repositories config finished.