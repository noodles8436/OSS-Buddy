
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3812/)
# OSS BUDDY - 시각장애인을 위한 스마트 버스 탑승 시스템 
- 본 프로젝트는 2022 OSS 개발자 대회 제출용 Project 입니다.

프로젝트 구조 및 설치
-----------------------

본 프로젝트는 3가지 PART로 나뉘어집니다.    
각 PART 별 폴더의 ReadMe를 참조하여 설치하시기 바랍니다.   

1. Server :
   * Raspberry PI 로부터 실시간으로 버스 위치 정보를 전달받습니다.
   * Raspberry PI 로부터 실시간으로 정류장에 접근하는 버스 정보를 전달받습니다.
   * Android 로부터 유저로부터 요청사항을 처리합니다.   

2. RaspBerry PI :
   * 국토교통부에서 제공하는 API (TAGO)를 이용하여 실시간으로 버스 정보를 얻습니다.
   * 서버에 실시간 버스 위치 정보를 전달합니다.
   * 서버에 실시간으로 버스에 접근하는 버스 정보를 전달합니다.
   
3. Android :   
   * 안드로이드 기능
   * 안드로이드 기능
   * 안드로이드 기능
   

시각장애인 전용 앱
-----------------------

 1. ### 회원가입
    Enter the following command to open Image Detection Server   
    :: CAUTION :: ***wait until "Socket Opened" Message printed***

    
 2. ### 로그인
    Open ***new Conda Prompt in Project Folder ( activated `<env-name>` )***
    Follow below command **TO OPEN CLIENT PROGRAM**   
    :: CAUTION :: ***Client IP & PORT MUST BE THE SAME AS Server IP & PORT***

   
3. ### 버스 목록 조회 및 예약
   1. At the bottom right of the program screen, find the area you want and click on the area setting button.
   2. When clicking on the button, wait for the real-time camera image to be displayed in the windo that pops up.


4. ### 버스 예약 취소
   1. Change the several values that exist in the lower left to the desired values. 
   2. Press the "Change Settings" button.   

버스기사 전용 앱
-----------------------

 1. ### 회원가입  
    1. 회원가입 버튼을 누른다.
    2. 회원가입 정보를 입력하고 회원가입을 한다.

    
 2. ### 로그인
    1. 자신이 운행하는 버스 번호와 차량 번호를 입력하고 로그인한다.

   
3. ### 버스 예약 정보 확인
   1. 자신이 운행하는 버스에 대한 예약이 진행되었을 경우, 화면에 예약자의 정류장 위치와 남은 정류장 수가 나온다.
   2. 이를 확인하여 해당 버스 정류장에 정차하여 시각장애인의 버스 탑승을 돕는다.

개발환경
----------------------
    OS  : Windows 10 Education 64 Bit (10.0, Build 19042)
    CPU : Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz (4 CPUs), ~3.2GHz
    RAM : DDR3 16GB
    GPU : NVIDIA GeForce GTX 1050 Ti 4GB

FAQ
----------------------
  - Q: 예상 질문   
  A: 예상 답변

Library License
----------------------
```
라이브러리 리스트
```

How to Conribute
----------------------
Check out the ['HOW TO CONTRIBUTE'](https://github.com/noodles8436/THE-CROSS/wiki/How-To-Contribute) item on the Github Wiki Page.   

Contributors
----------------------
***Thanks everyone who helped me with this project.***
- Advice : Song Youngwoo   
