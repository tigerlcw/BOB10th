import sys
import os
from time import sleep
import pandas as pd
import datetime
from datetime import datetime
import csv
import numpy as np
import re
import procmon_csv

def print_menu():
    print('\nMENU')

    print('0 = 프로그램 종료') 
    # vm 종료 및 파이썬코드 종료
    print('1 = VM 시작')
    # VM 시작 코드
    print('2 = VM 스냅샷 찍기')
    # VM 스냅샷 찍기
    print('3 = 파일 검사')
    # 프로세스모니터 와이어샤크 // 볼라티비티 + 현종이형 코드 
    print('4 = vmem 메모리 추출')
    # vmem 메모리 추출 코드
    return


def main():
    option = -1

    while option != 0:
        print_menu()
        try:
            option = int(input('\nEnter an option? '))
            if option == 0:
                print('Bye')
            elif option == 1:
                procmon_csv.vm_start()
            elif option == 2:
                procmon_csv.vm_snapshot()
            elif option == 3:
                procmon_csv.file_search()
            elif option == 4:
                procmon_csv.dump_vmem()
                
            else:
                print('\nERROR: Enter a valid option!!')
        except ValueError:
            print('\nERROR: Enter a valid option!!')

    return



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()