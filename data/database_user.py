#드림즈컴츄르 추가 파일
import pymysql
from datetime import datetime
import bcrypt
from data.Defs import User
class Database:
    def __init__(self):     
        self.dct_db = pymysql.connect(
        db="sys",
        host="database-2.cskg3bhzvpnw.ap-northeast-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        passwd="dreamscometrue",
        charset = 'utf8'
        )
        self.salt = bcrypt.gensalt()

    def id_not_exists(self,input_id):
        curs = self.dct_db.cursor(pymysql.cursors.DictCursor) #Dictionary cursor -> row 결과를 dictionary 형태로 리턴
        sql = "SELECT * FROM users1 WHERE user_id=%s"
        curs.execute(sql,input_id)  #input_id 데이터를 서버에 전송
        data = curs.fetchone()
        curs.close()
        if data:
            return False
        else:
            return True

    def match_idpw(self, id, pw): #아이디와 비번이 일치하는지 비교
        input_password =  pw
        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM users1 WHERE user_id=%s" 
        curs.execute(sql,id) #입력받은 id 서버로 전송
        data = curs.fetchone()  #입력받은 id와 일치하는 행 하나 선택
        curs.close()
        check_password = bcrypt.checkpw(input_password.encode('utf-8'),data['user_password'].encode('utf-8')) #https://velog.io/@castleq90/bcrypt%EB%B9%84%ED%81%AC%EB%A6%BD%ED%8A%B8
        '''check_password=False
        if(input_password == data['user_password'].encode('utf-8')):
            check_password = True
        print(input_password, "입력값") #이 방식을 사용할 경우, 껐다 키면 salt값이 변경되어 비밀번호가 틀렸다고 나옴''' 
        #print( data['user_password'].encode('utf-8'), "데이터베이스")
        return check_password

    def add_id(self, user_id): #아이디 추가
        curs = self.dct_db.cursor()
        sql = "INSERT INTO users1 (user_id) VALUES (%s)" #users테이블에서 user_id 필드에 %s의 값을 삽입
        curs.execute(sql, user_id)
        curs.close()
        curs = self.dct_db.cursor()
        self.dct_db.commit()
        sql = "INSERT INTO users2 (user_id) VALUES (%s)" #users테이블에서 user_id 필드에 %s의 값을 삽입
        curs.execute(sql, user_id)
        self.dct_db.commit()
        curs.close()

    def add_pw(self, user_pw, user_id): #비밀번호 & coin 초기값 추가 * 캐릭터 초기값은 1로(캐릭터 숫자로 표현)
        initial_coin = 0 #가입시, 보유한 coin 0으로 설정
        initial_character = 0
        hashed_pw = bcrypt.hashpw(user_pw.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        #print(hashed_pw, "입력값")
        curs = self.dct_db.cursor()
        sql = "UPDATE users1 SET user_password=%s WHERE user_id=%s"
        curs.execute(sql,(hashed_pw, user_id))
        #print(hashed_pw, "라라")
        self.dct_db.commit()
        curs = self.dct_db.cursor()
        sql = "UPDATE users2 SET user_coin=%s WHERE user_id=%s"
        curs.execute(sql,(initial_coin, user_id)) #코인 초기값 추가
        self.dct_db.commit()
        curs = self.dct_db.cursor()
        sql = "UPDATE users2 SET user_character=%s WHERE user_id=%s"
        curs.execute(sql,(initial_character, user_id))
        self.dct_db.commit()
        curs.close()

    def set_char(self):
        self.id = User.user_id
        self.char = User.character
        curs = self.dct_db.cursor()
        sql = "UPDATE users2 SET user_character=%s WHERE user_id = %s"
        curs.execute(sql,(self.char, self.id))
        self.dct_db.commit()
        curs.close()
    
    def show_mychar(self): #선택한 캐릭터 보여주는 함수 
        self.id = User.user_id
        self.char = User.character
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,user_character FROM users2 WHERE user_id=%s" #user_id와 user_character열만 선택
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
        check_char = data[1] #user_id는 인덱스 0에, user_character는 인덱스 1에 저장되어 있음
        return check_char

    def show_mycoin(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,user_coin FROM users2 WHERE user_id=%s" #user_id와 user_character열만 선택
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
        check_coin = data[1] #user_id는 인덱스 0에, user_coin 인덱스 1에 저장되어 있음
        return check_coin

    def set_coin(self):
        self.id = User.user_id
        self.coin = User.coin
        curs = self.dct_db.cursor()
        sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
        curs.execute(sql,(self.coin, self.id))
        self.dct_db.commit()
        curs.close()

    def buy_char(self):
        self.id = User.user_id
        self.buy = User.buy_character
        self.coin = User.coin
        self.price = User.price
        curs = self.dct_db.cursor()
        if(self.buy == 1):
            sql = "UPDATE users2 SET char2=%s WHERE user_id = %s"
            curs.execute(sql, (5, self.id))
            sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
            curs.execute(sql, (self.coin-100, self.id))
            self.dct_db.commit()
        if(self.buy == 2):
            sql = "UPDATE users2 SET char3=%s WHERE user_id = %s"
            curs.execute(sql, (5, self.id))
            sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
            curs.execute(sql, (self.coin-100, self.id))
            self.dct_db.commit()
        if(self.buy == 3):
            sql = "UPDATE users2 SET char4=%s WHERE user_id = %s"
            curs.execute(sql, (5, self.id))
            sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
            curs.execute(sql, (self.coin-200, self.id))
            self.dct_db.commit()
        curs.close()


    # 유저 게임기록 업데이트
    def update_score(self,mode,new_score):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        now = datetime.now()

        if mode == "easy": # easy mode
            sql = "UPDATE current_easy_score SET score=%s, date=%s WHERE ID=%s"
        else : # hard mode
            sql = "UPDATE current_hard_score SET score=%s, date=%s WHERE ID=%s"

        curs.execute(sql,(new_score,now.strftime('%Y-%m-%d'),self.id))
        self.dct_db.commit()
        curs.close()
    
    # 현재 최고기록 확인
    def high_score(self,mode): 
        self.id = User.user_id
        curs = self.dct_db.cursor()

        if mode == "easy":
            sql = "SELECT score FROM current_easy_score WHERE ID=%s"
        else : 
            sql = "SELECT score FROM current_hard_score WHERE ID=%s"

        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
        highscore = data[0]
        return highscore

    # 데이터 로드 (랭킹메뉴에서)
    def load_data(self, mode):    
        curs = self.dct_db.cursor(pymysql.cursors.DictCursor)
        if mode == 'easy':
            sql = 'select * from current_easy_score order by score desc'
        elif mode == 'hard':
            sql = 'select * from current_hard_score order by score desc'

        curs.execute(sql)
        data = curs.fetchall()
        curs.close()
        return data

    # 유저 랭킹 기록 있는지 확인.
    def rank_not_exists(self,input_id,mode):
        if mode == 'easy':
            sql = "SELECT * FROM current_easy_score WHERE ID=%s"
        else :
            sql = "SELECT * FROM current_hard_score WHERE ID=%s"

        curs = self.dct_db.cursor(pymysql.cursors.DictCursor) 
        curs.execute(sql,input_id)  
        data = curs.fetchone()
        curs.close()
        if data:
            return False
        else:
            return True

    #랭킹기록 처음인경우 점수 기록
    def update_score2(self,mode,new_score): 
        now = datetime.now()
        curs = self.dct_db.cursor()
        self.id = User.user_id

        if mode == "easy":
            sql = "INSERT INTO current_easy_score(ID, score, date) VALUES (%s,%s,%s)" 
        else :
            sql = "INSERT INTO current_hard_score(ID, score, date) VALUES (%s,%s,%s)" 
            
        curs.execute(sql, (self.id,new_score,now.strftime('%Y-%m-%d')))
        self.dct_db.commit()
        curs.close()
        print("suc")

    
            

    def my_easy_rank(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT ID,score FROM current_easy_score WHERE ID=%s" #user_id와 user_character열만 선택
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
        if data == None:
            User.easy_score = "None"
        else: 
            easy_score = data[1] #user_id는 인덱스 0에, score 인덱스 1에 저장되어 있음
            User.easy_score  = easy_score


    def my_hard_rank(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT ID,score FROM current_hard_score WHERE ID=%s" #user_id와 user_character열만 선택
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
        if data == None:
            User.hard_score = "None"
        else: 
            hard_score = data[1] #user_id는 인덱스 0에, score 인덱스 1에 저장되어 있음
            User.hard_score  = hard_score

    def reduce_char_life(self):#게임에서 죽으면 보유하고 있는 캐릭터의 목숨이 줄어들도록 함. 
        self.id = User.user_id
        self.char = User.character #cat2는 1, cat3는 2, cat4는 3으로 되어 있음. 
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,char1,char2,char3,char4 FROM users2 WHERE user_id=%s" #user_id와 char 2,3,4 선택(char1은 목숨 무제한)
        curs.execute(sql,self.id)
        data = curs.fetchone()  
        curs.close()

        curs = self.dct_db.cursor()
        if(data[self.char+1]>0): #목숨이 0이상일때만 1을 줄임. 
            if(self.char == 1): #선택한 캐릭터가 cat2면, cat2의 목숨을 1개 줄임. 
                sql = "UPDATE users2 SET char2=%s WHERE user_id = %s"
                curs.execute(sql, (data[self.char+1]-1, self.id))
                self.dct_db.commit()
            if(self.char == 2): #선택한 캐릭터가 cat3면, cat3의 목숨을 1개 줄임. 
                sql = "UPDATE users2 SET char3=%s WHERE user_id = %s"
                curs.execute(sql, (data[self.char+1]-1, self.id))
                self.dct_db.commit()
            if(self.char == 3): #선택한 캐릭터가 cat4면, cat4의 목숨을 1개 줄임. 
                sql = "UPDATE users2 SET char4=%s WHERE user_id = %s"
                curs.execute(sql, (data[self.char+1]-1, self.id))
                self.dct_db.commit()
            curs.close()

        if(data[self.char+1]==0):
            User.cat_lock[self.char] = True

    #데이터베이스 확인을 통해, 캐릭터가 잠겨있는지 안잠겨있는지 확인
    def char_lock(self):
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,char2,char3,char4 FROM users2 WHERE user_id=%s" #user_id와 char 2,3,4 선택(char1은 목숨 무제한)
        curs.execute(sql,self.id)
        data = curs.fetchone()  
        curs.close()

        for i in range(1,4):
            if data[i] == 0:
                User.cat_lock[i] = True

    
    def check_char_lock(self):
        self.char = User.character
        self.id = User.user_id
        curs = self.dct_db.cursor()
        sql = "SELECT user_id,char1,char2,char3,char4 FROM users2 WHERE user_id=%s" 
        curs.execute(sql,self.id)
        data = curs.fetchone()  
        curs.close()
        #User.character의 인덱스는 0부터임, 지금 가져온 데이터에서 char1부터 인덱스 1이므로, +1을 한 값.
        check = data[User.character+1]
        if check==0: #캐릭터가 잠겨 있으면 true
            return True
        return False #그렇지 않으면 false