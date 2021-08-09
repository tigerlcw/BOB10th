import os
from time import sleep

'''해당 부분은 VBOX 조정'''
# gui / headless - 백그라운드 실행
#os.system('VBoxManage startvm boan_sol_win --type headless --username test --password 1234 --verbose')
#os.system('VBoxManage controlvm boan_sol_win --type headless addencpassword --username test --password 1234 --verbose')
#sleep(55)

# 호스트에서 게스트로 파일 전송

#os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\1.exe --username test --password 1234 --verbose')

'''이 부분부터는 프로세스모니터 조종'''
# 무조건 슬립을 줘야 안 꼬임 나중에 시스템 쪽 코드를 작성 하는 것이 좋아 보임.

#os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /BackingFile C:\test\kkabi.pml')
#sleep(4)
#os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /Terminate')
#sleep(8)
#os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /OpenLog C:\test\kkabi.pml /SaveAs C:\test\kkabi.csv')
#sleep(2)
#print("no error step 1")
#os.system('VBoxManage guestcontrol boan_sol_win copyfrom --target-directory C:\Users\LINKER\Desktop\PythonWorkspace\bosol\ C:\test\kkabi.csv --username test --password 1234 --verbose')

'''이 부분부터는 와이어샤크 조종'''

# 1. 와샥키고 -> 2. 이더넷 고르고 3. 패킷 다른이름 저장누르고 4. 경로 설정 및 이름 설정
# -c 20 -> 20개 패킷 
# 게스트에서 tshark 명령 실행 후 바로 호스트 피시로 결과.csv 파일이 전달 옴 ㄱㅇㄷ
os.system('VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- cmd.exe /c tshark -i eth0 -T fields -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info -c 20' + '> C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\result.csv')
print("성공")
#tshark -i eth0 -T fields -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info > C:\test\ls.csv