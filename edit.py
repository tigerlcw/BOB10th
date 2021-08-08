import os
import logging
import sys
from time import sleep

'''해당 부분은 VBOX 조정'''

#os.system('VBoxManage startvm boan_sol_win --type gui')
#VBoxManage startvm boan_sol --type gui   #(gui | headless | sdi | separate)

#os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\1.exe --username test --password 1234 --verbose')

'''이 부분부터는 프로세스모니터 조종'''

#os.system('WireShark -D')

#os.system('VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- cmd.exe /c WireShark -D')

os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\Procmon64.exe" --username test --password 1234 --wait-stdout')
print("aa")
sleep(2) # 무조건 슬립을 줘야 안꼬임 나중에 시스템쪽 코드를 작성 하는 것이 좋아 보임.
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /Terminate')
sleep(5)

'''이 부분부터는 와이어샤크 조종'''
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c WireShark')
sleep(2)
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c WireShark -L')
print("end")
#sys.exit("exit")

#Terminate

# start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout /c Pocmon64 /Terminate