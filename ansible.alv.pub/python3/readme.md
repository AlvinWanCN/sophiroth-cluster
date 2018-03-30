
<p align='center'> <a href='https://github.com/alvinwancn' target="_blank"> <img src='https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png' alt='Alvin Wan' width=200></a></p>

## Directory introduction

python3 software information on ansible.alv.pub

## Install python3 on ansible.alv.pub

### Install depend packges

```bash
# yum install gcc zlib zlib-devel libffi-devel -y
```

### Install python3
```bash
# wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
#  tar xf Python-3.6.5 .tar.xz -C /usr/local/src/
# cd /usr/local/src/Python-3.6.5/
# ./configure --prefix=/usr/local/python3
# make
# sudo make install
# /usr/local/python3/bin/python3 --version
Python 3.6.4

```
success install python3.

```bash
$ sudo ln -s /usr/local/python3/bin/python3 /usr/bin/
```

