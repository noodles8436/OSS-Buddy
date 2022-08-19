
SERVER_IP = "localhost"
SERVER_PORT = 7777
SERVER_PACKET_SIZE = 1024

TASK_SPLIT = ";"

# 작업번호:내용

# (버스기사 등록) 20;차량번호;이름;맥주소
# (Res. 버스기사 등록) 성공 = 20;00 or 실패 = 20;01

# (버스기사 로그인) 21;차량번호;이름;맥주소
# (Res. 버스기사 로그인) 성공 = 21;00 or 실패 = 21;01

# (버스기사 알림) 22;정거장이름;남은 정거장 수

# (RaspBerry 연결) 30;nodeid;mac
# (Res. RaspBerry 연결) 성공 = 30;00 or 실패 = 30;01

# (RaspBerry 초접근 버스 안내) 32;routeid;routeNo

# (RaspBerry 주변 새로은 MAC 유저 확인 ) 33;mac;nodeid
# (Res. RaspBerry 주변 새로은 MAC 유저 확인 ) 있는 유저 = 33;00 or 없는 유저 = 33;01

# (RaspBerry 주변 등록된 유저 사라짐) 34;usermac;nodeid



# Timeout 대응 TASK CODE

CONNECTION_CHECK = "CONNECTION_CHECK"
LOCATION_SEARCH_TERM = 1
TIMEOUT_SEC = 10


# (사용자 등록) 00;이름;전화번호;맥주소
# (Res. 사용자 등록) 성공 = 00;00 or 실패 = 00;01 -> 클라는 연결을 한번 끊고 다시 시도해야함

USER_REGISTER = "00"
USER_REGISTER_SUCCESS = USER_REGISTER + TASK_SPLIT + "00"
USER_REGISTER_FAIL = USER_REGISTER + TASK_SPLIT + "01"


# (사용자 로그인) 01;이름;전화번호;맥주소
# (Res. 사용자 로그인) 성공 = 01;00 or 실패 = 01;01 <실패시 바로 접속끊기> or 실패_서버문제 = 01;02
#   or 실패_클라문제 = 01;03

USER_LOGIN = "01"
USER_LOGIN_SUCCESS = USER_LOGIN + TASK_SPLIT + "00"
USER_LOGIN_FAIL = USER_LOGIN + TASK_SPLIT + "01"
USER_LOGIN_SERVER_ERR = USER_LOGIN + TASK_SPLIT + "02"
USER_LOGIN_CLIENT_ERR = USER_LOGIN + TASK_SPLIT + "03"

# (Res. 사용자 위치 확인) 성공 = 02;00 or 실패 = 02;01
USER_LOCATION_FIND = "02"
USER_LOCATION_FIND_SUCCESS = USER_LOCATION_FIND + TASK_SPLIT + "00"
USER_LOCATION_FIND_FAIL = USER_LOCATION_FIND + TASK_SPLIT + "01"

# (사용자 버스 예약) 03;버스번호
# (Res. 사용자 버스 예약) 예약 가능한 버스 = 03;00, 예약 불가능한 버스 = 03;01



# (사용자 버스 예약 확정) 04;버스번호
# (Res. 사용자 버스 예약 확정) 성공 = 04;00, 실패 = 04;01

# (사용자 버스 예약 취소) 05;00
# (Res. 사용자 버스 예약 취소) 성공 = 05;00, 실패 = 05;01

# (사용자 버스 도착 진동) 06;00

# (서버가 사용자 로그아웃) 07;00
KICK_USER = "07" + TASK_SPLIT + "00"

# (클라가 서버를 로그아웃) 08;00
DISCONNECT_SERVER = "08" + TASK_SPLIT + "00"
