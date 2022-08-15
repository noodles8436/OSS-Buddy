import pymysql

# CONFIG
host = "localhost"
user = "root"
passwd = "159357"
db = "buddy_db"


def createTable():
    """ Database.py 내부에 저장된 Config 값을 이용하여 데이터베이스에 접근함
        이후 테이블 'usertable' 의 존재 여부에 따라 테이블 초기화 및 생성을 수행함

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

    print(result)

    if "usertable" == result[0]:
        print("[BUDDY-DB] 이미 userTable이 존재합니다. 테이블 초기화를 하시겠습니까? [Y/N]")
        print("[BUDDY-DB] INPUT >> ", end='')
        if "y" == input().lower():
            cur.execute("DROP TABLE usertable")
        else:
            print("[BUDDY-DB] 테이블 생성을 종료합니다.")
            return

    cur.execute("CREATE TABLE usertable("
                "phone char(12), name char(3), mac char(17)"
                ")")
    conn.commit()
    conn.close()

    print("[BUDDY-DB] 테이블 생성 완료!")
    print("[BUDDY-DB] 테이블 생성을 종료합니다.")


class Database:
    """사용자의 정보를 등록하고 조회하기 위한 DB 인터페이스 클래스
    """

    def __init__(self):
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

    def addUser(self, name: str, phone_num: str, mac_add: str) -> bool:
        """데이터베이스에 사용자를 등록하기 위한 함수

        :param name: 추가할 사용자의 이름
        :param phone_num: 추가할 사용자의 전화번호
        :param mac_add: 추가할 사용자의 단말기 MAC 주소
        :return: boolean 사용자 등록 성공 여부 (True : 성공, False : 실패)
        """

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

    def getUserMac(self, name: str, phone_num: str) -> str:
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

    def __del__(self):
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
    createTable()
    db = Database()
    db.addUser("홍길동", "01012341234", "AA:AA:AA:AA:AA:AA")
    result = db.getUserMac("홍길동", "01012341234")
    db.removeUser("홍길동", "01012341234", "AA:AA:AA:AA:AA:AA")
