import pymysql
import sys
#MariaDB 접속 정보
DB_HOST = "192.168.100.20"
DB_USER = "cjulib"
DB_PASS = "security"
DB_PORT = 3306
DB_NAME = "cju"

#메인 메뉴 루프
def main_menu():
    while True:
        print("\n--- [ 성적 관리 시스템 ] ---")
        print("1. 전체조회")
        print("2. 번호조회")
        print("3. 성적 추가")
        print("4. 성적 삭제")
        print("5. 성적 수정")
        print("6. 종료")
        print("---------------------------")
        choice = input("메뉴 선택: ")
        if choice == '1':
            select_all()
        elif choice == '2':
            select_one()
        elif choice == '3':
            insert_member()
        elif choice == '4':
            delete_member()
        elif choice == '5':
            update_member()
        elif choice == '6':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

#if __name__ == "__main__":
    #main_menu()

##################################################

def select_all():
    #전체 조회 내용
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            )
        with conn.cursor() as cursor:
            sql = "SELECT * FROM grades"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(f"--- grades 테이블 조회 결과 (총 {len(result)}건) ---")
            if result:
                for row in result:
                    print(f"SEQ: {row['member_seq']}, 수강 과목: {row['subject']}, 성적: {row['score']}, 수강 학기: {row['term']}")
            else:
                print("조회된 데이터가 없습니다.")
    except pymysql.MySQLError as e:
        print(f"데이터베이스 오류가 발생했습니다: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

def select_one():
    #번호 조회 내용
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            )
        with conn.cursor() as cursor:
            seq_input = input("조회해야 할 시퀀스 넘버를 입력하시오. : ")
            sql = "SELECT member_seq, subject, score, term FROM grades WHERE member_seq = %s"
            cursor.execute(sql, (seq_input,))
            result = cursor.fetchall()
            print(f"--- grades 테이블 조회 결과 (총 {len(result)}건) ---")
            if result:
                for row in result:
                    print(f"SEQ: {row['member_seq']}, 수강 과목: {row['subject']}, 성적: {row['score']}, 수강 학기: {row['term']}")
            else:
                print("조회된 데이터가 없습니다.")
    except pymysql.MySQLError as e:
        print(f"데이터베이스 오류가 발생했습니다: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

def insert_member():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            )
        with conn.cursor() as cursor:
            member_sep = input("번호: ")
            subject = input("과목: ")
            score = input("점수: ")
            term = input("수강 학기: ")
            sql = "INSERT INTO grades (member_seq, subject, score, term) VALUES ('" + member_sep + "', '" + subject + "', '" + score + "', '" + term + "')"
            cursor.execute(sql)
            conn.commit()
            print(f"\n성공적으로 성적을 추가했습니다.")
    except pymysql.MySQLError as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"오류 발생: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

def delete_member():
    #성적 삭제 내용
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            )
        with conn.cursor() as cursor:
            id_input = input("삭제해야 할 아이디 넘버를 입력하시오. : ")
            sql = "DELETE FROM grades WHERE id_grade = %s"
            cursor.execute(sql, (id_input))
            conn.commit()
    except pymysql.MySQLError as e:
        print(f"데이터베이스 오류가 발생했습니다: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            print(f"성공적으로 성적을 삭제했습니다.")

def update_member():
    #성적 수정 내용
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            )
        with conn.cursor() as cursor:
            sql = "UPDATE grades SET score = %s WHERE id_grade = %s"
            print("새로운 점수를 입력하세요.")
            new_score = int(input())
            print("성적을 변경할 사용자의 키를 입력하세요.")
            target_id = int(input())
            affected_rows = cursor.execute(sql, (new_score, target_id))
            conn.commit()
            if affected_rows > 0:
                print(f"성공: ID가 '{target_id}'인 사용자의 이름을 '{new_score}'으로 수정했습니다.")
            else:
                print(f"알림: ID가 '{target_id}'인 사용자를 찾을 수 없어 수정되지 않았습니다.")
    except pymysql.MySQLError as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"오류 발생: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

##################################################

main_menu()