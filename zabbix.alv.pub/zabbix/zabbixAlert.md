<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

## Zabbix Alert Configuration

 
#### Zabbix origin Email Alert

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

```bash
# curl -fsSL https://raw.githubusercontent.com/AlvinWanCN/sophiroth-cluster/master/zabbix.alv.pub/zabbix/scripts/send_email.py > /usr/lib/zabbix/alertscripts/send_email.py
# vim /usr/lib/zabbix/alertscripts/send_email.py
```
这里我们将用于邮件告警的脚本放在了/usr/lib/zabbix/alertscripts/目录下，因为在配置文件里我们将这个配置设置为了用于存放告警脚本的目录。</br>
然后在改脚本里，需要将邮件服务器的相关信息修改为实际可以用的信息，包括地址、用户名、密码等。
####

现在我们去在web端配置脚本</br>
<img src=images/7.jpg></br>
这里我们做一些相应的配置，写上名称，选择类型，这里我们选择script，然后填写脚本名，然后写上三个参数{ALERT.SENDTO}，{ALERT.SUBJECT}，{ALERT.MESSAGE}，这三个参数会传到脚本里面。</br>
<img src=images/8.jpg></br>
添加完成</br>
<img src=images/9.jpg></br>
修改用户的告警方式</br>
<img src=images/10.jpg></br>
修改action里的内容</br>
<img src=images/11.jpg></br>

然后我们在被监控的服务器上关掉zabbix-agent之后，就会收到邮件告警了。</br>
<img src=images/12.jpg></br>