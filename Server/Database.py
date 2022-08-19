import pymysql

# CONFIG
host = "localhost"
user = "root"
passwd = "159357"
db = "buddy_db"


def createTable() -> None:
    """ Database.py 내부에 저장된 Config 값을 이용하여 데이터베이스에 접근함.
    이후 테이블 'usertable', 'busdrivertable', 'raspberrytable' 의 존재 여부에 따라 테이블 초기화 및 생성을 수행함

    :return: None
    """
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='utf8')
        cur = conn.cursor()
    except Exception as e:
        print("[BUDDY-DB][ERR] 데이터베이스 연결에 실패했습니다. 데이터베이스 구축을 종료합니다.")
        return

    cur.execute("SHOW TABLES LIKE 'usertable'")
    result = cur.fetchone()
    flag = 0
    if result is not None:
        if "usertable" in result:
            print("[BUDDY-DB] 이미 userTable이 존재합니다. 테이블 초기화를 하시겠습니까? [Y/N]")
            print("[BUDDY-DB] INPUT >> ", end='')
            if "y" == input().lower():
                cur.execute("DROP TABLE usertable")
            else:
                flag = 1

    if flag == 0:
        cur.execute("CREATE TABLE usertable("
                    "phone char(12), name char(3), mac char(17)"
                    ")")
        conn.commit()

    cur.execute("SHOW TABLES LIKE 'busdrivertable'")
    result = cur.fetchone()
    flag = 0

    if result is not None:
        if "busdrivertable" in result:
            print("[BUDDY-DB] 이미 busdriverTable이 존재합니다. 테이블 초기화를 하시겠습니까? [Y/N]")
            print("[BUDDY-DB] INPUT >> ", end='')
            if "y" == input().lower():
                cur.execute("DROP TABLE busdrivertable")
            else:
                flag = 1

    if flag == 0:
        cur.execute("CREATE TABLE busdrivertable("
                    "vehicleno char(12), name char(3), mac char(17)"
                    ")")
        conn.commit()

    cur.execute("SHOW TABLES LIKE 'raspberrytable'")
    result = cur.fetchone()
    flag = 0

    if result is not None:
        if "raspberrytable" in result:
            print("[BUDDY-DB] 이미 raspberrytable이 존재합니다. 테이블 초기화를 하시겠습니까? [Y/N]")
            print("[BUDDY-DB] INPUT >> ", end='')
            if "y" == input().lower():
                cur.execute("DROP TABLE raspberrytable")
            else:
                flag = 1

    if flag == 0:
        cur.execute("CREATE TABLE raspberrytable("
                    "nodeid char(20), mac char(17), nodenm char(50)"
                    ")")
        conn.commit()

    conn.close()

    print("[BUDDY-DB] 테이블 생성 완료!")
    print("[BUDDY-DB] 테이블 생성을 종료합니다.")


class Database:
    """사용자의 정보를 등록하고 조회하기 위한 DB 인터페이스 클래스
    """

    def __init__(self) -> None:
        """ Database 클래스 생성자, SQL 서버와 연결 후 연결 정보를 객체에 저장함
        Database.py 내부에 저장된 Config 값을 이용하여 데이터베이스에 접근함

        :return: None
        """

        try:
            self.conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='utf8')
            self.cur = self.conn.cursor()
        except Exception as e:
            self.conn.close()
            self.cur.close()
            self.conn = None
            self.cur = None
            print("[BUDDY-DB][ERR] 데이터베이스 연결에 실패했습니다.")
            return
        print("[BUDDY-DB] 데이터베이스 연결 완료")

    # USER Database method

    def addUser(self, name: str, phone_num: str, mac_add: str) -> bool:
        """데이터베이스에 사용자를 등록하기 위한 함수

        :param name: 추가할 사용자의 이름
        :param phone_num: 추가할 사용자의 전화번호
        :param mac_add: 추가할 사용자의 단말기 MAC 주소
        :return: boolean 사용자 등록 성공 여부 (True : 성공, False : 실패)
        """

        if self.isUserExist(name, phone_num, mac_add) == 1:
            print("[BUDDY-DB] 이미 존재하는 사용자입니다.")
            return False

        if self.isUserExist(name, phone_num, mac_add) == -1:
            return False

        try:
            sql = "INSERT INTO usertable (phone, name, mac) VALUES (%s, %s, %s)"
            self.cur.execute(sql, (phone_num, name, mac_add))
            self.conn.commit()
        except Exception as e:
            print("[BUDDY-DB][ERR] 사용자 등록 실패 -> 사용자 : ", name, phone_num, mac_add)
            print(e.args[0])
            return False

        print("[BUDDY-DB] 사용자 등록 성공 -> 사용자 : ", name, phone_num, mac_add)
        return True

    def removeUser(self, name: str, phone_num: str, mac_add: str) -> bool:
        """데이터베이스에서 사용자를 삭제하기 위한 함수

        :param name: 삭제할 사용자의 이름
        :param phone_num: 삭제할 사용자의 전화번호
        :param mac_add: 삭제할 사용자의 단말기 MAC 주소
        :return: boolean 사용자 삭제 성공 여부 (True : 성공, False : 실패)
        """

        if self.isUserExist(name, phone_num, mac_add) == 0:
            print("[BUDDY-DB] 존재하지 않는 사용자입니다.")
            return False

        if self.isUserExist(name, phone_num, mac_add) == -1:
            return False

        try:
            sql = "DELETE FROM usertable WHERE phone = %s AND name = %s AND mac = %s"
            self.cur.execute(sql, (phone_num,  name, mac_add))
            self.conn.commit()
        except Exception as e:
            print("[BUDDY-DB][ERR] 사용자 삭제 실패 -> 사용자 : ", name, phone_num, mac_add)
            print(e.args[0])
            return False

        print("[BUDDY-DB] 사용자 삭제 성공 -> 사용자 : ", name, phone_num, mac_add)
        return True

    def getUserMac(self, name: str, phone_num: str) -> str or None:
        """데이터베이스에서 사용자 이름과 전화번호를 이용하여 사용자의 단말기 Mac 주소를 검색하여 반환하는 함수

        :param name: 검색할 사용자의 이름
        :param phone_num: 검색할 사용자의 전화번호
        :return: str 사용자 단말기 Mac 주소 반환 (str : 사용자가 존재할 경우, None : 사용자가 등록되지 않았거나 실패한 경우)
        """
        try:
            sql = "SELECT * FROM usertable WHERE phone = %s AND name = %s"
            self.cur.execute(sql, (phone_num,  name))
            self.conn.commit()
            result = self.cur.fetchone()
        except Exception as e:
            print("[BUDDY-DB][ERR] 사용자 조회 실패 -> 사용자 : ", name, phone_num)
            print(e.args[0])
            return None

        print("[BUDDY-DB] 사용자 조회 성공 -> 사용자 : ", result)
        if result is not None:
            result = result[2]

        return result

    def isUserExist(self, name: str, phone_num: str, mac_add: str) -> int:
        """데이터베이스에서 해당 이름, 전화번호, 단말기 Mac 주소를 가지는 사용자가 있는지에 대한 여부를 반환한다.

        :param name: 검색할 사용자의 이름
        :param phone_num: 검색할 사용자의 전화번호
        :param mac_add: 검색할 사용자의 단말기 Mac 주소
        :return: int 존재할 경우 1, 존재하지 않을 경우 0, 그 밖의 오류는 -1을 반환한다.
        """

        try:
            sql = "select EXISTS (select * from usertable where phone = %s AND name = %s " \
                  "AND mac = %s limit 1) as success"
            self.cur.execute(sql, (phone_num, name, mac_add))
            self.conn.commit()
            result = self.cur.fetchone()
        except Exception as e:
            print("[BUDDY-DB][ERR] 사용자 조회 실패 -> 사용자 : ", name, phone_num)
            print(e.args[0])
            return -1

        return result[0]

    # BUS DRIVER Database method

    def addBusDriver(self, vehicleno: str, name: str, mac_add: str):
        """데이터베이스에 버스 운전기사를 등록하기 위한 함수

        :param name: 추가할 버스 운전기사의 이름
        :param vehicleno: 추가할 버스 운전기사의 차량 번호
        :param mac_add: 추가할 버스 운전기사의 단말기 MAC 주소
        :return: boolean 사용자 등록 성공 여부 (True : 성공, False : 실패)
        """

        if self.isBusDriverExist(vehicleno, name, mac_add) == 1:
            print("[BUDDY-DB] 이미 존재하는 버스 운전기사입니다.")
            return False

        if self.isBusDriverExist(vehicleno, name, mac_add) == -1:
            return False

        try:
            sql = "INSERT INTO busdrivertable (vehicleno, name, mac) VALUES (%s, %s, %s)"
            self.cur.execute(sql, (vehicleno, name, mac_add))
            self.conn.commit()
        except Exception as e:
            print("[BUDDY-DB][ERR] 버스 운전기사 등록 실패 -> 버스 운전기사 : ", name, vehicleno, mac_add)
            print(e.args[0])
            return False

        print("[BUDDY-DB] 버스 운전기사 등록 성공 -> 버스 운전기사 : ", name, vehicleno, mac_add)
        return True

    def removeBusDriver(self, vehicleno: str, name: str, mac_add: str) -> bool:
        """데이터베이스에서 버스 운전기사를 삭제하기 위한 함수

        :param name: 삭제할 버스 운전기사의 이름
        :param vehicleno: 삭제할 버스 운전기사의 차량 번호
        :param mac_add: 삭제할 버스 운전기사의 단말기 MAC 주소
        :return: boolean 사용자 삭제 성공 여부 (True : 성공, False : 실패)
        """

        if self.isBusDriverExist(vehicleno, name, mac_add) == 0:
            print("[BUDDY-DB] 존재하지 않는 버스 운전기사입니다.")
            return False

        if self.isBusDriverExist(vehicleno, name, mac_add) == -1:
            return False

        try:
            sql = "DELETE FROM busdrivertable WHERE vehicleno = %s AND name = %s AND mac = %s"
            self.cur.execute(sql, (vehicleno,  name, mac_add))
            self.conn.commit()
        except Exception as e:
            print("[BUDDY-DB][ERR] 버스 운전기사 삭제 실패 -> 버스 운전기사 : ", name, vehicleno, mac_add)
            print(e.args[0])
            return False

        print("[BUDDY-DB] 버스 운전기사 삭제 성공 -> 버스 운전기사 : ", name, vehicleno, mac_add)
        return True

    def getBusDriverMac(self, vehicleno: str, name: str) -> str or None:
        """데이터베이스에서 버스 운전기사 이름과 차량 번호를 이용하여 버스 운전기사의 단말기 Mac 주소를 검색하여 반환하는 함수

        :param vehicleno: 검색할 버스 운전기사의 차량 번호
        :param name: 검색할 버스 운전기사의 이름
        :return: str 버스 운전기사 단말기 Mac 주소 반환 (str : 버스 운전기사가 존재할 경우, None : 버스 운전기사가 등록되지 않았거나 실패한 경우)
        """
        try:
            sql = "SELECT * FROM busdrivertable WHERE vehicleno = %s AND name = %s"
            self.cur.execute(sql, (vehicleno,  name))
            self.conn.commit()
            result = self.cur.fetchone()
        except Exception as e:
            print("[BUDDY-DB][ERR] 버스 운전기사 조회 실패 -> 버스 운전기사 : ", name, vehicleno)
            print(e.args[0])
            return None

        print("[BUDDY-DB] 버스 운전기사 조회 성공 -> 버스 운전기사 : ", result)
        if result is not None:
            result = result[2]

        return result

    def isBusDriverExist(self, vehicleno: str, name: str, mac_add: str) -> int:
        """데이터베이스에서 해당 차량번호, 이름, 단말기 Mac 주소를 가지는 버스 운전기사가 있는지에 대한 여부를 반환한다.

        :param vehicleno: 검색할 버스 운전기사의 차량 번호
        :param name: 검색할 버스 운전기사의 이름
        :param mac_add: 검색할 버스 운전기사의 단말기 Mac 주소
        :return: int 존재할 경우 1, 존재하지 않을 경우 0, 그 밖의 오류는 -1을 반환한다.
        """

        try:
            sql = "select EXISTS (select * from busdrivertable where vehicleno = %s AND name = %s " \
                  "AND mac = %s limit 1) as success"
            self.cur.execute(sql, (vehicleno,  name, mac_add))
            self.conn.commit()
            result = self.cur.fetchone()
        except Exception as e:
            print("[BUDDY-DB][ERR] 버스 운전기사 조회 실패 -> 버스 운전기사 : ", name, vehicleno)
            print(e.args[0])
            return -1

        return result[0]

    # Raspberry PI Database method

    def getRaspberryNodeID(self, mac_add: str) -> str or None:
        """데이터베이스에서 해당 Mac 주소를 가지는 Raspberry PI의 nodeid를 반환하는 함수

        :param mac_add: 검색할 Raspberry PI의 Mac 주소
        :return: str Raspberry PI nodeid 반환 (str : Raspberry PI가 존재할 경우, None : Raspberry PI가 등록되지 않았거나 실패한 경우)
        """

        try:
            sql = "SELECT * FROM raspberrytable WHERE mac = %s"
            self.cur.execute(sql, (mac_add))
            self.conn.commit()
            result = self.cur.fetchone()
        except Exception as e:
            print("[BUDDY-DB][ERR] Raspberry PI 조회 실패 -> Raspberry PI mac: ", mac_add)
            print(e.args[0])
            return None

        print("[BUDDY-DB] Raspberry PI 조회 성공 -> Raspberry PI mac: ", result)
        if result is not None:
            result = result[0]

        return result

    def getRaspberryMAC(self, nodeid: str) -> str or None:
        """데이터베이스에서 해당 nodeid를 가지는 Raspberry PI의 MAC 주소를 반환하는 함수

        :param nodeid: 검색할 Raspberry PI의 nodeid
        :return: str Raspberry PI MAC 주소 반환 (str : Raspberry PI가 존재할 경우, None : Raspberry PI가 등록되지 않았거나 실패한 경우)
        """

        try:
            sql = "SELECT * FROM raspberrytable WHERE nodeid = %s"
            self.cur.execute(sql, (nodeid))
            self.conn.commit()
            result = self.cur.fetchone()
        except Exception as e:
            print("[BUDDY-DB][ERR] Raspberry PI 조회 실패 -> Raspberry PI nodeid: ", nodeid)
            print(e.args[0])
            return None

        print("[BUDDY-DB] Raspberry PI 조회 성공 -> Raspberry PI nodeid: ", result)
        if result is not None:
            result = result[1]

        return result

    def __del__(self) -> None:
        """ Database 클래스 소멸자. DB 인터페이스 객체가 사라짐에 따라
            데이터베이스를 저장하고 정상적으로 종료함

        :return: None
        """

        if self.conn is None:
            return
        else:
            self.conn.commit()
            self.conn.close()
            self.cur.close()


if __name__ == "__main__":
    pass
    #createTable()
    #db = Database()

    #print("\n")

    #db.addUser("홍길동", "01012341234", "AA:AA:AA:AA:AA:AA")
    #db.addUser("홍길동", "01012341234", "AA:AA:AA:AA:AA:AA")
    #print(db.getUserMac('홍길동', '01012341234'))
    #db.removeUser("홍길동", "01012341234", "AA:AA:AA:AA:AA:AA")
    #db.removeUser("홍길동", "01012341234", "AA:AA:AA:AA:AA:AA")

    #print("\n")

    #db.addBusDriver('경기17바1234', '기사님', 'BB:BB:BB:BB:BB:BB')
    #db.addBusDriver('경기17바1234', '기사님', 'BB:BB:BB:BB:BB:BB')
    #print(db.getBusDriverMac('경기17바1234', '기사님'))
    #db.removeBusDriver('경기17바1234', '기사님', 'BB:BB:BB:BB:BB:BB')
    #db.removeBusDriver('경기17바1234', '기사님', 'BB:BB:BB:BB:BB:BB')

    #print("\n")

    #node_c = db.getRaspberryNodeID('CC:CC:CC:CC:CC:CC')
    #node_d = db.getRaspberryNodeID('DD:DD:DD:DD:DD:DD')
    #db.getRaspberryMAC(node_c)
    #db.getRaspberryMAC(node_d)
