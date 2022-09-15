
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
   * 회원가입 정보를 서버로 전달합니다.
   * 유저는 서버에 유저의 위치 정보를 전달합니다.
   * 유저는 서버로부터 버스정류장 정보를 얻습니다.
   * 유저는 버스 예약할 버스 번호를 서버에 전달합니다.
   * 유저는 서버로부터 예약한 버스 번호와 도착유무 정보를 얻습니다.
   * 버스기사 유저는 서버로부터 예약한 사람이 있는 버스정류장과 남은 정거장 수를 얻습니다.
   

시각장애인 전용 앱
-----------------------

 1. ### 회원가입
    1. 회원가입 버튼을 누른다.
    2. 회원가입 정보를 입력하고 회원가입을 한다.

    
 2. ### 로그인
    1. 회원가입한 정보를 입력하고 로그인 한다.

   
3. ### 근처 버스 정류장 찾기
   1. 근처에 있는 버스 정류장 위치를 찾습니다.

4. ### 버스 예약하기
   1. 버튼 조작을 통해 버스를 예약합니다. (한번 클릭 : 버스 정보 안내, 두번 클릭 : 다른 버스 탐색, 길게 누르기 : 예약하기)
   2. 길게 누르면 예/아니오 버튼을 통해 한번 더 확인합니다. (두번 클릭 : 예약 또는 예약 취소)

5. ### 버스 정보 확인
   1. 화면에 예약한 버스 정보와 얼마나 나왔는지 알려줍니다.
   2. 버스가 2정거장 이하로 남았을 때, 진동을 통해 준비해야함을 알립니다.
   3. 버스가 버스 정류장에 도착하였다면, 진동을 통해서 버스에 탑승해야함을 알립니다.
   
6. ### 버스 예약 취소
   1. 버튼을 더블 클릭하여 버스 예약을 취소합니다.

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


Contribute 방법
----------------------
Contribute 방법은 본 Project의 [Github WIKI](https://github.com/noodles8436/OSS-Buddy/wiki) 를 참고해주세요.

Contributors
----------------------
***본 프로젝트에 도움을 주신 분들께 감사드립니다.***
- 프로젝트 조언 : 연세대학교 미래캠퍼스 소프트웨어학부 고요한 교수님
- 프로젝트 조언 : 연세대학교 미래캠퍼스 소프트웨어학부 홍정희 교수님
- 통신 관련 조언 : 연세대학교 미래캠퍼스 소프트웨어학부 21학번 최성하 학우
