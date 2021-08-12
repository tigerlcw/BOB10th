import os
from time import sleep
import pandas as pd
import datetime
from datetime import datetime
import csv
import numpy as np
import re

vm_name = 'boan_sol_win'
name = '--username test'
password = '--password 1234 --verbose'
# host addr
src = 'C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\'
# guest addr
des = 'C:\\test\\'
# guest cmd addr
cmd_addr = 'C:\Windows\SysWOW64\cmd.exe'

# guest control
vbox_guest = 'VBoxManage guestcontrol'



'''해당 부분은 VBOX 조정'''
# gui / headless - 백그라운드 실행
#os.system('VBoxManage startvm boan_sol_win --type gui')
#sleep(40)
file_name = input("분석할 파일이름을 입력하세요. -> ")
#add_func = input("테스트용 명령어 인자를 추가해주세요. 없으면 Enter Ex) /all -> ")


os.system(vbox_guest+ ' ' + vm_name + ' ' + 'copyto --target-directory'+ ' ' + src + file_name + ' ' + name + ' ' + password)
#os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\%s --username test --password 1234 --verbose' % file_name)
