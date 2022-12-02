# 드림즈컴츄르 추가 파일
import pymysql
from datetime import datetime
import bcrypt
from data.Defs import User

class Database:
    def __init__(self): 
        self.dct_db = pymysql.connect(
        db="sys",
        host="dkssik12.ch80vdihvl1x.ap-northeast-2.rds.amazonaws.com",
        port = 3306,
        user="gamego",
        passwd="pygamemaking",
        charset = 'utf8'
        )
        self.salt = bcrypt.gensalt()

    def id_not_exists(self, input_id):
        # Dictionary cursor -> row 결과를 dictionary 형태로 리턴
        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM users1 WHERE user_id=%s"
        curs.execute(sql, input_id)  # input_id 데이터를 서버에 전송
        data = curs.fetchone()
        curs.close()
        if data:
            return False
        else:
            return True

    def match_idpw(self, id, pw):  # 아이디와 비번이 일치하는지 비교
        input_password = pw
        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM users1 WHERE user_id=%s"
        curs.execute(sql, id)  # 입력받은 id 서버로 전송
        data = curs.fetchone()  # 입력받은 id와 일치하는 행 하나 선택
        curs.close()
        check_password = bcrypt.checkpw(input_password.encode(
            'utf-8'), data['user_password'].encode('utf-8'))
        return check_password


    def add_id(self, user_id): #아이디 추가
        curs = self.dct_db.cursor()
        # users테이블에서 user_id 필드에 %s의 값을 삽입
        sql = "INSERT INTO users1 (user_id) VALUES (%s)"
        curs.execute(sql, user_id)
        curs.close()
        curs = self.dct_db.cursor()
        self.dct_db.commit()
        # users테이블에서 user_id 필드에 %s의 값을 삽입
        sql = "INSERT INTO tusers2 (user_id) VALUES (%s)"
        curs.execute(sql, user_id)
        self.dct_db.commit()
        curs.close()

    def add_ninkname(self, user_nickname, user_id): #닉네임 추가
        curs = self.dct_db.cursor()
        sql = "UPDATE users1 SET user_nickname=%s WHERE user_id=%s"
        curs.execute(sql,(user_nickname, user_id))
        self.dct_db.commit()

    def add_pw(self, user_pw, user_id):  # 비밀번호 & coin 초기값 추가 * 캐릭터 초기값은 1로(캐릭터 숫자로 표현)
        initial_coin = 0  # 가입시, 보유한 coin 0으로 설정
        initial_pcharacter = 0
        initial_fcharacter = 3
        initial_dcharacter = 6
        have = 5
        not_have = -1
        hashed_pw = bcrypt.hashpw(user_pw.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        # print(hashed_pw, "입력값")
        curs = self.dct_db.cursor()
        sql = "UPDATE users1 SET user_password=%s WHERE user_id=%s"
        curs.execute(sql, (hashed_pw, user_id))
        # print(hashed_pw, "라라")
        self.dct_db.commit()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_coin=%s WHERE user_id=%s"
        curs.execute(sql, (initial_coin, user_id))  # 코인 초기값 추가
        self.dct_db.commit()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_pcharacter=%s WHERE user_id=%s"
        curs.execute(sql, (initial_pcharacter, user_id))
        self.dct_db.commit()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_fcharacter=%s WHERE user_id=%s"
        curs.execute(sql, (initial_fcharacter, user_id))
        self.dct_db.commit()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_dcharacter=%s WHERE user_id=%s"
        curs.execute(sql, (initial_dcharacter, user_id))
        self.dct_db.commit()
        curs.close()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET pchar1=%s, pchar2=%s, pchar3=%s WHERE user_id=%s"
        curs.execute(sql, (have, not_have, not_have, user_id))
        self.dct_db.commit()
        curs.close()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET fchar1=%s, fchar2=%s, fchar3=%s WHERE user_id=%s"
        curs.execute(sql, (have, not_have, not_have, user_id))
        self.dct_db.commit()
        curs.close()
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET dchar1=%s, dchar2=%s, dchar3=%s WHERE user_id=%s"
        curs.execute(sql, (have, not_have, not_have, user_id))
        self.dct_db.commit()
        curs.close()
        

    def set_pchar(self):
        self.id = User.user_id
        self.char = User.pcharacter
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_pcharacter=%s WHERE user_id = %s"
        curs.execute(sql, (self.char, self.id))
        self.dct_db.commit()
        curs.close()

    def set_fchar(self):
        self.id = User.user_id
        self.char = User.fcharacter
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_fcharacter=%s WHERE user_id = %s"
        curs.execute(sql, (self.char, self.id))
        self.dct_db.commit()
        curs.close()

    def set_dchar(self):
        self.id = User.user_id
        self.char = User.dcharacter
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_dcharacter=%s WHERE user_id = %s"
        curs.execute(sql, (self.char, self.id))
        self.dct_db.commit()
        curs.close()

    def show_pmychar(self):  # 선택한 캐릭터 보여주는 함수
        self.id = User.user_id
        self.char = User.pcharacter
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT user_id,user_pcharacter FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        check_pchar = data[1]  # user_id는 인덱스 0에, user_character는 인덱스 1에 저장되어 있음
        return check_pchar
    
    def show_fmychar(self):  # 선택한 캐릭터 보여주는 함수
        self.id = User.user_id
        self.char = User.fcharacter
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT user_id,user_fcharacter FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        check_fchar = data[1]  # user_id는 인덱스 0에, user_character는 인덱스 1에 저장되어 있음
        print(check_fchar)
        return check_fchar
    
    def show_dmychar(self):  # 선택한 캐릭터 보여주는 함수
        self.id = User.user_id
        self.char = User.dcharacter
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT user_id,user_dcharacter FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        check_dchar = data[1]  # user_id는 인덱스 0에, user_character는 인덱스 1에 저장되어 있음
        return check_dchar
    
    def show_mycoin(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT user_id,user_coin FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        check_coin = data[1]  # user_id는 인덱스 0에, user_coin 인덱스 1에 저장되어 있음
        return check_coin
    
    def get_nickname(self): # 스토리라인 삽입을 위한 이름 가져오는 함수
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT user_id, user_nickname FROM users1 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        name = data[1]  # user_id는 인덱스 0에, user_coin 인덱스 1에 저장되어 있음
        return name


    def set_coin(self):
        self.id = User.user_id
        self.coin = User.coin
        print(self.coin)
        curs = self.dct_db.cursor()
        sql = "UPDATE tusers2 SET user_coin=%s WHERE user_id = %s"
        curs.execute(sql, (self.coin, self.id))
        self.dct_db.commit()
        curs.close()

    # 상점
    def buy_char(self):
        self.id = User.user_id
        self.buy = User.buy_character
        self.coin = User.coin
        self.price = User.price
        curs = self.dct_db.cursor()
        if (self.buy == 1):
            sql = "UPDATE users2 SET char2=%s WHERE user_id = %s"
            curs.execute(sql, (5, self.id))
            sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
            curs.execute(sql, (self.coin-100, self.id))
            self.dct_db.commit()
        if (self.buy == 2):
            sql = "UPDATE users2 SET char3=%s WHERE user_id = %s"
            curs.execute(sql, (5, self.id))
            sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
            curs.execute(sql, (self.coin-100, self.id))
            self.dct_db.commit()
        if (self.buy == 3):
            sql = "UPDATE users2 SET char4=%s WHERE user_id = %s"
            curs.execute(sql, (5, self.id))
            sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
            curs.execute(sql, (self.coin-200, self.id))
            self.dct_db.commit()
        curs.close()

    # 유저 게임기록 업데이트

    def update_score(self, mode, new_score):
        self.nickname = User.user_nickname
        self.id = User.user_id
        curs = self.dct_db.cursor()
        now = datetime.now()

        if mode == "score":  # score mode
            sql = "UPDATE current_score_score SET score=%s, date=%s, nickname = %s WHERE ID=%s"

        curs.execute(sql, (new_score, now.strftime('%Y-%m-%d'), self.nickname, self.id))
        self.dct_db.commit()
        curs.close()

    def update_time(self, mode, new_time):
        self.nickname = User.user_nickname
        self.id = User.user_id
        curs = self.dct_db.cursor()
        now = datetime.now()

        if mode == "time":  # time mode
            sql = "UPDATE current_time_score SET time=%s, date=%s, nickname = %s WHERE ID=%s"  

        curs.execute(sql, (new_time, now.strftime('%Y-%m-%d'), self.nickname, self.id))
        self.dct_db.commit()
        curs.close()

    # 현재 최고기록 확인
    def high_score(self, mode):
        self.nickname = User.user_nickname
        self.id = User.user_id
        curs = self.dct_db.cursor()

        if mode == "score":
            sql = "SELECT score FROM current_score_score WHERE ID=%s"

        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        highscore = data[0]
        return highscore

    def high_time(self, mode):
        self.nickname = User.user_nickname
        self.id = User.user_id
        curs = self.dct_db.cursor()

        if mode == "time":
            sql = "SELECT time FROM current_time_score WHERE ID=%s"
    
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        hightime = data[0]
        return hightime
   
    # 데이터 로드 (랭킹메뉴에서)
    def load_data(self, mode):
        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        if mode == 'score':
            sql = 'select * from current_score_score order by score desc'
        elif mode == 'time':
            sql = 'select * from current_time_score order by time desc'

        curs.execute(sql)
        data = curs.fetchall()
        curs.close()
        return data

    # 유저 랭킹 기록 있는지 확인.
    def rank_not_score_exists(self, input_id, mode):
        if mode == 'score':
            sql = "SELECT * FROM current_score_score WHERE ID=%s"

        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        curs.execute(sql, input_id)
        data = curs.fetchone()
        curs.close()
        if data:
            return False
        else:
            return True

    def rank_not_time_exists(self, input_id, mode):
        if mode == 'time':
            sql = "SELECT * FROM current_time_score WHERE ID=%s"

        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        curs.execute(sql, input_id)
        data = curs.fetchone()
        curs.close()
        if data:
            return False
        else:
            return True

    # 랭킹기록 처음인경우 점수 기록
    def update_score2(self, mode, new_score):
        now = datetime.now()
        curs = self.dct_db.cursor()
        self.nickname = User.user_nickname
        self.id = User.user_id

        if mode == "score":
            sql = "INSERT INTO current_score_score(ID, score, date, nickname ) VALUES (%s,%s,%s, %s)"

        curs.execute(sql, (self.id, new_score, now.strftime('%Y-%m-%d'), self.nickname))
        self.dct_db.commit()
        curs.close()
        print("suc")

    def update_time2(self, mode, new_time):
        now = datetime.now()
        curs = self.dct_db.cursor()
        self.nickname = User.user_nickname
        self.id = User.user_id

        if mode == "time":
            sql = "INSERT INTO current_time_score(ID,time, date,nickname) VALUES (%s,%s,%s,%s)"

        curs.execute(sql, (self.id, new_time, now.strftime('%Y-%m-%d'),self.nickname))
        self.dct_db.commit()
        curs.close()
        print("suc")

    def my_score_rank(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT nickname,score FROM current_score_score WHERE ID=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        if data == None:
            User.score_score = "None"
        else:
            score_score = data[1]  # user_id는 인덱스 0에, score 인덱스 1에 저장되어 있음
            User.score_score = score_score

    def my_time_rank(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 user_character열만 선택
        sql = "SELECT nickname,time FROM current_time_score WHERE ID=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        if data == None:
            User.time_score = "None"
        else:
            time_score = data[1]  # user_id는 인덱스 0에, time 인덱스 1에 저장되어 있음
            User.time_score = time_score

    # 데이터베이스 확인을 통해, 캐릭터가 잠겨있는지 안잠겨있는지 확인
    def pchar_lock(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 char 2,3,4 선택(char1은 목숨 무제한)
        sql = "SELECT user_id,pchar2,pchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()

        for i in range(1, 3):
            if data[i] == 0:
                User.cat_lock[i] = True

    def fchar_lock(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 char 2,3,4 선택(char1은 목숨 무제한)
        sql = "SELECT user_id,fchar2,fchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()

        for i in range(1, 3):
            if data[i] == 0:
                User.cat_lock[i] = True
    
    def dchar_lock(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        # user_id와 char 2,3,4 선택(char1은 목숨 무제한)
        sql = "SELECT user_id,dchar2,dchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()

        for i in range(1, 3):
            if data[i] == 0:
                User.cat_lock[i] = True



    def check_pchar_lock(self):
        self.char = User.pcharacter
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,pchar1,pchar2,pchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        # User.character의 인덱스는 0부터임, 지금 가져온 데이터에서 char1부터 인덱스 1이므로, +1을 한 값.
        check = data[User.pcharacter+1]
        if check == 0:  # 캐릭터가 잠겨 있으면 true
            return True
        return False  # 그렇지 않으면 false
    
    def check_fchar_lock(self):
        self.char = User.fcharacter
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,fchar1,fchar2,fchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        # User.character의 인덱스는 0부터임, 지금 가져온 데이터에서 char1부터 인덱스 1이므로, +1을 한 값.
        check = data[User.fcharacter-2]
        if check == 0:  # 캐릭터가 잠겨 있으면 true
            return True
        return False  # 그렇지 않으면 false
    
    def check_dchar_lock(self):
        self.char = User.dcharacter
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,dchar1,dchar2,dchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql, self.id)
        data = curs.fetchone()
        curs.close()
        # User.character의 인덱스는 0부터임, 지금 가져온 데이터에서 char1부터 인덱스 1이므로, +1을 한 값.
        check = data[User.dcharacter-5]
        if check == 0:  # 캐릭터가 잠겨 있으면 true
            return True
        return False  # 그렇지 않으면 false
