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
        print("1. 전체 조회")
        print("2. 번호 조회")
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
            print("프로그램을 종료합니다. 감사합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

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
            sql = "SELECT * FROM grades g JOIN member m ON m.seq = g.member_seq;"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                print("--- [ 성적 전체 목록 ] ---")
                print("번호 | 이름(ID)              | 과목명                         | 점수 | 학기        | 등록일")
                for row in result:
                    print(
                        f"{row['member_seq']}"[:3].rjust(3), " | "
                        f"{row['name']}({row['id']})"[:20].ljust(20), " | "
                        f"{row['subject']}"[:20].ljust(20), " | "
                        f"{row['score']}"[:10].rjust(10), " | "
                        f"{row['term']}"[:10].ljust(10), " | "
                        f"{row['reg_date']}"[:25].rjust(25)
                    )

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
            seq_input = input("조회할 학생 번호(시퀀스 넘버)를 입력하시오. : ")
            sql = "SELECT * FROM grades g JOIN member m ON m.seq = g.member_seq WHERE g.member_seq = %s"
            cursor.execute(sql, (seq_input,))
            result = cursor.fetchall()
            if result:
                print(f"\n--- [ {result[0]['name']} 학생의 성적 리포트 ] ---")
                print(f"- 아이디: {result[0]['id']}")
                print(f"- 학기: {result[0]['term']}")
                print("---------------------------")
                total = 0
                for idx, row in enumerate(result, start=1):
                    print(f"{idx}. {row['subject']}: {row['score']}점")
                    total += row['score']
                print("---------------------------")
                print(f"평균 점수: {total / len(result):.1f}점")
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
            print("--- [ 성적 데이터 추가 ] ---")
            member_sep = input("- 학생 번호(seq) 입력: ")
            subject = input("- 과목명 입력: ")
            score = input("- 점수 입력: ")
            term = input("- 수강 학기 입력(ex. 2026-1): ")
            sql = "INSERT INTO grades (member_seq, subject, score, term) VALUES ('" + member_sep + "', '" + subject + "', '" + score + "', '" + term + "')"
            cursor.execute(sql)
            conn.commit()
            cursor.execute("SELECT name FROM member m JOIN grades g ON m.seq = g.member_seq WHERE m.seq = %s", (member_sep,))
            result = cursor.fetchone()
            name = result['name'] if result else None
            print()
            print(f"[시스템] '{name}' 학생의 '{subject}' 성적이 성공적으로 등록되었습니다.")
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
            #print("--- [ 성적 데이터 삭제 ] ---")
            id_input = input("삭제할 성적의 고유 ID(id_grade) 입력: ")
            cursor.execute("SELECT id_grade, subject FROM grades WHERE id_grade = %s", (id_input,))
            row = cursor.fetchone()
            if not row:
                print("[시스템] 해당 ID의 성적 데이터가 존재하지 않습니다.")
                return
            confirm = input("정말로 삭제하시겠습니까? (y/n): ").lower()
            if confirm != 'y':
                print("[시스템] 삭제가 취소되었습니다.")
                return
            sql = "DELETE FROM grades WHERE id_grade = %s"
            cursor.execute(sql, (id_input))
            conn.commit()
            print()
            print(f"[시스템] {id_input}번 성적 데이터가 삭제되었습니다. (대상: {row['subject']})")
    except pymysql.MySQLError as e:
        print(f"데이터베이스 오류가 발생했습니다: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


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
            #print("--- [ 성적 데이터 수정 ] ---")
            sql = "UPDATE grades SET score = %s WHERE id_grade = %s"
            target_id = int(input("수정할 성적의 고유 ID(id_grade) 입력: "))
            cursor.execute("SELECT subject, score FROM grades WHERE id_grade = %s", (target_id,))
            row = cursor.fetchone()
            if not row:
                print("[시스템] 해당 ID의 성적 데이터가 존재하지 않습니다.")
                return
            old_score = row['score']
            subject = row['subject']
            print(f"--- 현재 정보: {subject} ({old_score}점) ---")
            new_score = int(input("- 수정할 점수 입력: "))
            affected_rows = cursor.execute(sql, (new_score, target_id))
            conn.commit()
            if affected_rows > 0:
                print()
                print(f"[시스템] 성적 수정이 완료되었습니다. ({old_score}점 → {new_score}점)")
            else:
                print("[시스템] 점수는 숫자로 입력해야 합니다.")
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