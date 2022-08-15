import pymysql

# CONFIG
host = "localhost"
user = "root"
passwd = "159357"
db = "buddy_db"


# requirement : buddy_db 라는 데이터베이스가 이미 존재해야함.
# requirement : mysql Database 이어여함.
def createTable():
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, db=db, charset='utf8')
        cur = conn.cursor()
    except Exception as e:
        print("[BUDDY-DB] 데이터베이스 연결에 실패했습니다. 데이터베이스 구축을 종료합니다.")
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

    def __init__(self):
        pass

    def addUser(self):
        pass

    def removeUser(self):
        pass

    def getUserMac(self):
        pass


if __name__ == "__main__":
    createTable()
