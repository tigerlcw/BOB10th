import os
from time import sleep
import pandas as pd
import datetime
from datetime import datetime
import csv
import numpy as np
import re


print("분석할 파일이름을 입력하세요. ")
file_name = input()

'''해당 부분은 VBOX 조정'''
# gui / headless - 백그라운드 실행
#os.system('VBoxManage startvm boan_sol_win --type headless --username test --password 1234 --verbose')
#os.system('VBoxManage controlvm boan_sol_win --type headless addencpassword --username test --password 1234 --verbose')
#sleep(55)

# 호스트에서 게스트로 파일 전송

os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\%s --username test --password 1234 --verbose' % file_name)

'''이 부분부터는 프로세스모니터 조종'''
# 무조건 슬립을 줘야 안 꼬임 나중에 시스템 쪽 코드를 작성 하는 것이 좋아 보임.

os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /BackingFile C:\\test\\kkabi.pml')
sleep(2)
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c C:\\test\\cmd.exe')
sleep(4)
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /Terminate')
sleep(8)
os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- emd.exe /c Procmon64 /OpenLog C:\\test\\kkabi.pml /SaveAs C:\\test\\kkabi.csv')
sleep(2)
print("no error step 1")
os.system('VBoxManage guestcontrol boan_sol_win copyfrom --target-directory C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\monitor.csv C:\\test\\kkabi.csv --username test --password 1234 --verbose')

'''이 부분부터는 와이어샤크 조종'''

# 1. 와샥키고 -> 2. 이더넷 고르고 3. 패킷 다른이름 저장누르고 4. 경로 설정 및 이름 설정
# -c 20 -> 20개 패킷 
# 게스트에서 tshark 명령 실행 후 바로 호스트 피시로 결과.csv 파일이 전달 옴 ㄱㅇㄷ
os.system('VBoxManage guestcontrol boan_sol_win run --exe "C:\windows\system32\cmd.exe" --username test --password 1234 --wait-stdout -- cmd.exe /c tshark -i eth0 -T fields -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info -c 20' + '> C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\kkabi.csv')
print("성공")
#tshark -i eth0 -T fields -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info > C:\test\ls.csv



# 특정 프로그램 실행 후 30초동안의 log 수집한 csv?
# 분석해야 하는 프로그램이 wmiprvse.exe 라고 가정

# 샘플 데이터

df = pd.read_csv("C:/Users/LINKER/Desktop/PythonWorkspace/bosol/monitor.csv", error_bad_lines=False)


# 검사하고 싶은 프로그램( ex)'wmiprvse.exe' )에서 CreateFile API를 사용해 생성된 파일 이름을 file이라는 변수에 저장
process = df['Process Name'] == file_name ############### 수정해야함
df_unique = df[process]
operation = df_unique['Operation'] == 'CreateFile'
df1 = df_unique[operation]
df1 = df1[['Path']]
df1['name'] = df1['Path'].str.extract(r'([ \w-]+\.+[ \w-]+)')
#(?<=\$)[0-9.]+

df1 = df1.dropna(axis=0)
filename = df1['name'].reset_index()
filename.drop(['index'], axis=1, inplace=True)
input_name = file_name ##################### 수정해야함. 검사하려는 파일 이름 추가

filename.loc[0] = [input_name]
filename.insert(0, 'total', 1)
file = filename.groupby('total')['name'].unique().loc[1]
print("생성한 파일: ", file)


## file이라는 변수에 저장된 프로그램이 사용한 API 함수 불러오기
df_final = df[df['Process Name'].isin(file)]
df1 = df_final.reset_index(drop=True)
df2 = df1[['Operation', 'Path']]
df2

cols = ['Operation',]
df2.insert(1, 'total', 1)
df3 = df2.groupby(cols)['total'].sum().reset_index()
df3 = df3.sort_values(by = 'total')
df3 = df3.reset_index(drop=True)
print(df3)