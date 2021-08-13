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

# Vbox control
vbox_guest = 'VBoxManage guestcontrol'
vbox_snapshot = 'VBoxManage snapshot'
copyto = 'copyto --target-directory'
copyfrom = 'copyfrom --target-directory'
take_snap = 'take win-test'



'''해당 부분은 VBOX 조정'''
# gui / headless - 백그라운드 실행
#os.system('VBoxManage startvm boan_sol_win --type gui')
#sleep(40)
file_name = input("분석할 파일이름을 입력하세요. -> ")
#add_func = input("테스트용 명령어 인자를 추가해주세요. 없으면 Enter Ex) /all -> ")


os.system(vbox_guest+ ' ' + vm_name + ' ' + 'copyto --target-directory'+ ' ' + src + file_name + ' ' + name + ' ' + password)
#os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\%s --username test --password 1234 --verbose' % file_name)



os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\%s --username test --password 1234 --verbose' % file_name)
sleep(1)
os.system('VBoxManage snapshot boan_sol_win take win-test') # 스냅샷 찍기
sleep(10)

'''이 부분부터는 프로세스모니터 조종'''

os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /BackingFile C:\\test\\monitor.pml')
sleep(4)
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c C:\\test\\%s /c %s' % (file_name, add_func))
sleep(5)
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /Terminate')
sleep(6) #ipconfig 8sec
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /OpenLog C:\\test\\monitor.pml /SaveAs C:\\test\\monitor.csv')
sleep(2)
print("no error step 1")
os.system('VBoxManage guestcontrol boan_sol_win copyfrom --target-directory C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\ C:\\test\\monitor.csv --username test --password 1234 --verbose')
'''이 부분부터는 와이어샤크 조종'''
sleep(2)
# 1. 와샥키고 -> 2. 이더넷 고르고 3. 패킷 다른이름 저장누르고 4. 경로 설정 및 이름 설정
# -c 20 -> 20개 패킷 
# 게스트에서 tshark 명령 실행 후 바로 호스트 피시로 결과.csv 파일이 전달 옴 ㄱㅇㄷ
os.system('VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 --wait-stdout -- cmd.exe /c tshark -i 이더넷 -T fields -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info -c 3' + ' > C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\shark.csv')
print("성공")
sleep(1)

os.system('VBoxManage controlvm boan_sol_win poweroff') #power off vm
sleep(15)
print("꺼짐완료")
os.system('VBoxManage snapshot boan_sol_win restore win-test') #스냅샷 시점으로 복원
sleep(10)
print("스냅샷복원")
os.system('VBoxManage startvm boan_sol_win --type gui')
sleep(1)
os.system('VBoxManage snapshot boan_sol_win delete win-test')

