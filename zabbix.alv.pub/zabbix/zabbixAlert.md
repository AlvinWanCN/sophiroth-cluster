<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

## Zabbix Alert Configuration

 
#### Zabbix origin Email Alart

点击administration, 然后点Media types

<img src=images/1.jpg>
然后到点击email,开始进行一些配置。</br>
<img src=images/2.jpg></br>
然后配置用户 </br>
<img src=images/3.jpg></br>

然后创建一个action </br>
<img src=images/4.jpg></br>
点击operations </br>
<img src=images/5.jpg></br>
设置通知方式，添加通知对象，对象可以是组或用户 </br>
<img src=images/6.jpg></br>
然后就可以让相关的用户收到告警邮件了。


#### Zabbix script send email.

除了通过原有的zabbix配置发送email之外，我们还可以通过脚本来发送邮件。

这里我们配置一个脚本来用于发送邮件
