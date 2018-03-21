
<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

zabbix内置的一些常用变量如下：


```txt
故障：{TRIGGER.STATUS}，服务器：{HOSTNAME1}发生:{TRIGGER.NAME}故障！
告警主机：{HOSTNAME1}，IP地址：{HOST.CONN}
告警时间：{EVENT.DATE}{EVENT.TIME}
告警等级：{TRIGGER.SEVERITY}
告警信息：{TRIGGER.NAME}
告警项目：{TRIGGER.KEY1}
问题详情：{ITEM.NAME}:{ITEM.VALUE}
当前状态：{TRIGGER.STATUS}:{ITEM.VALUE1}
事件ID：{EVENT.ID}
恢复：{TRIGGER.STATUS}，服务器：{HOSTNAME1}已经恢复！:{TRIGGER.NAME}
告警主机：{HOSTNAME1} ，IP地址：{HOST.CONN}
告警时间：{EVENT.DATE}{EVENT.TIME}
告警等级：{TRIGGER.SEVERITY}
告警信息：{TRIGGER.NAME}
告警项目：{TRIGGER.KEY1}
问题详情：{ITEM.NAME}:{ITEM.VALUE}
当前状态：{TRIGGER.STATUS}:{ITEM.VALUE1}
事件ID：{EVENT.ID}

主机显示名：{HOST.NAME}
```


这里我们自定义告警内容：

问题发生时的告警通知
<img src=../images/59.jpg>

问题解决了、恢复时的通知

<img src=../images/59.jpg>
