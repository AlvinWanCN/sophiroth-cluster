#coding:utf-8
import os,subprocess,time

WORK_DIR='/home/alvin/Travel-Notes/'

os.chdir(WORK_DIR)

TODAY_DIR=WORK_DIR+time.strftime('%Y/%B')+'/'
TODAY_DIR_FILE=TODAY_DIR+time.strftime('%d.%b.%Y.%a')+'.rst'
print('Start Pull ')
subprocess.call('git pull',shell=True)
subprocess.call('mkdir -p %s'%TODAY_DIR,shell=True)
print('Start cp readme to new')
subprocess.call('cp readme.rst %s'%TODAY_DIR_FILE,shell=True)
print('Start add file to git')
subprocess.call('git add %s'%TODAY_DIR_FILE,shell=True)
print('Start commit ')
subprocess.call('git commit -m "add new daily" %s'%TODAY_DIR_FILE,shell=True)
print('Start push')
subprocess.call('git push origin master',shell=True)