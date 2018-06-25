elk.alv.pub server
##############################




Install java and elasticsearch
`````````````````````````````````````

.. code-block:: bash

    yum install java -y
    yum install https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.0.rpm -y

Configure elasticsearch and system
```````````````````````````````


.. code-block:: bash

    chown elasticsearch /etc/elasticsearch/ -R
    vim /etc/elasticsearch/elasticsearch.yml
    node.name: elk.alv.pub
    http.port: 9200
    network.host: 192.168.127.89


    vim  /etc/security/limits.conf
    * soft nofile 65536
    * hard nofile 65536

    vim /etc/sysctl.conf
    vm.max_map_count=262144

.. code-block::

    sysctl -p


Install logstash
`````````````````````````````````

    yum install https://artifacts.elastic.co/downloads/logstash/logstash-6.3.0.rpm -y

Configure logstash
`````````````````````````````````

.. code-block:: bash

    vim /etc/logstash/logstash.yml
    http.host: "192.168.127.89"

    vim /etc/logstash/conf.d/elk.conf
    input {
    file {
    path => ["/var/log/*.log","/tmp/logstash.test"]
    }
      beats {
                    port => "5044"
            }
    }

    filter {
    if ([message] =~ "^ \[QC\] INFO"){
    drop {}
    }
    if ([message] =~ "^alvin"){
    drop {}
    }
    }
    output {
    elasticsearch { hosts => ["192.168.127.89:9200"] }
    stdout { codec => rubydebug }
    }


Install kibana
```````````````````````

.. code-block:: bash

    yum install https://artifacts.elastic.co/downloads/kibana/kibana-6.3.0-x86_64.rpm -y

Configure kibana
`````````````````````````

.. code-block:: bash

    yum ins

    cd /usr/local/kibana-5.0.0-linux-x86_64/
    vim config/kibana.yml
    server.host: "192.168.127.89"
    elasticsearch.url: "http://elk.alv.pub:9200"

    nohup /usr/local/kibana-5.0.0-linux-x86_64/bin/kibana &> /tmp/kibana.log &

Install filebeat
```````````````````````

.. code-block:: bash

    yum install https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.3.0-x86_64.rpm

