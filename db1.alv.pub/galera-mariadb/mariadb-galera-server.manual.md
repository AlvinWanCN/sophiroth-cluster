<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>



- check the number of galera cluster size

如下图查询结果所示，集群里有两台服务器。
```sql
MariaDB [(none)]> show status like 'wsrep_cluster_size';
+--------------------+-------+
| Variable_name      | Value |
+--------------------+-------+
| wsrep_cluster_size | 2     |
+--------------------+-------+
1 row in set (0.00 sec)

```

在我们再开启一台集群里服务之后再次查询,结果被成三台。
```sql
MariaDB [(none)]> show status like 'wsrep_%cluster%';
+--------------------------+--------------------------------------+
| Variable_name            | Value                                |
+--------------------------+--------------------------------------+
| wsrep_cluster_conf_id    | 3                                    |
| wsrep_cluster_size       | 3                                    |
| wsrep_cluster_state_uuid | ac13aa25-25c7-11e8-8b4a-a395e9960366 |
| wsrep_cluster_status     | Primary                              |
+--------------------------+--------------------------------------+
4 rows in set (0.00 sec)

```