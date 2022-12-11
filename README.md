# 2022-2-OSSProj-trio-7

## Shooting Game based on pygame

## Info

- python ![Generic badge](https://img.shields.io/badge/python-3-blue.svg)
  ![Generic badge](https://img.shields.io/badge/pygame-2.0.2-blue.svg)
  ![Generic badge](https://img.shields.io/badge/pygame_menu-4.2.0-blue.svg)
  ![Generic badge](https://img.shields.io/badge/pymysql-1.0.2-blue.svg)

- 라이선스 ![Generic badge](https://img.shields.io/badge/license-MIT-green.svg)
- 개발 환경 <img alt="" src ="https://img.shields.io/badge/IDE-VSCode-indianred">
- 운영 체제 ![Generic badge](https://img.shields.io/badge/OS-windows,mac_os,ubuntu-blue.svg)

## Base Code

[CSID-DGU/2022-1-OSSProj-DreamsComeTrue-4](https://github.com/CSID-DGU/2022-1-OSSProj-DreamsComeTrue-4) MIT LICENSE

## Team

✔ 팀장 : 동국대학교 산업시스템공학과 [유근태](https://github.com/Felix-Silas)

✔ 팀원 : 동국대학교 철학과 [송우영](https://github.com/wooyoung0830)

✔ 팀원 : 동국대학교 경영정보학과 [노성균](https://github.com/RohSungKyun)

## 프로젝트 소개

---

### 어린이 직업체험 슈팅게임

<br />

## 설치 및 실행 방법 (on Ubuntu)

---

#### 1. install python3

```
sudo apt-get update
sudo apt install python3-pip
```

#### 2. install pygame 2.0.2

```
sudo pip3 install pygame==2.0.2
```

#### 3. install pygame_menu 4.2.0

```
sudo pip3 install pygame_menu==4.2.0
```

#### 4. install pymysql 1.0.2

```
sudo pip3 install pymysql==1.0.2
```

#### 5. install bcrypt

```
pip install bcrypt
```

#### 6. download/clone this project and go to the directory

```
git clone https://github.com/CSID-DGU/2022-2-OSSProj-Trio-7.git
cd 2022-2-OSSProj-Trio-7
```

#### 7. run Main.py

```
python3 Main.py
```

# 기능 소개

## 로그인 및 회원가입

|메인화면|회원가입|로그인|
|---|---|---|
|![image](https://user-images.githubusercontent.com/62867581/206364740-63f072ed-d8ae-484a-82d2-c89eb6d3474a.png)|![image](https://user-images.githubusercontent.com/62867581/206831446-25e5a466-8b2a-4dc7-815b-f8f5d55ec1e3.png)|![image](https://user-images.githubusercontent.com/62867581/206831439-bf7ff28d-be8b-4886-999c-656de02f7133.png)|
|- 메인화면에서 로그인과 회원가입을 진행할 수 있다. |- 회원가입 시 아이디, 비밀번호, 닉네임을 입력한다. |- 회원가입 시 입력한 아이디, 비밀번호, 닉네임을 입력한다.|


## 직업(캐릭터) 선택 및 모드 선택

|직업 선택|직업 소개|모드 선택|
|---|---|---|
|![image](https://user-images.githubusercontent.com/62867581/206364773-315aeea5-ef74-4c46-b13d-63c10509e016.png)|![image](https://user-images.githubusercontent.com/62867581/206364790-6cf5048a-5368-44d3-b1f9-4a5f7ecff11d.png)|![image](https://user-images.githubusercontent.com/62867581/206829902-0ff31ca3-3f05-4ed1-bebd-779dc28cf307.png)|
|- 사용자는 원하는 직업을 선택할 수 있다. |- 각 직업에 대한 정보가 궁금하다면 '직업이 궁금하나요?'버튼을 통해 정보를 확인할 수 있다. |- 사용자는 원하는 게임의 모드를 선택할 수 있다.|

## 튜토리얼 모드
|튜토리얼 선택|로딩 화면|플레이 화면 |
|---|---|---|
|![image](https://user-images.githubusercontent.com/62867581/206829695-252e5a54-afea-46c1-a922-d0d3935766a7.png)|![image](https://user-images.githubusercontent.com/62867581/206823079-caf635ae-a7e2-4ddd-bac5-e83a8a02c1cc.png)|![image](https://user-images.githubusercontent.com/62867581/206823089-5b9dc637-1fc4-401e-8ac8-f8c12d000a23.png)|
|- 메인화면에서 튜토리얼 모드를 선택한다. |- ENTER 키를 눌러서 튜토리얼을 시작한다. |- 안내에 따라 조작법을 익힌다.|

## 캐릭터 소개
게임플레이시 사용자가 선택할 수 있는 캐릭터 종류입니다.
|경찰관|소방관|의사|
|---|---|---|
|경찰관|소방관|의사|
|경찰관|소방관|의사|
|경찰관|소방관|의사|

## 마이페이지 및 캐릭터 상점, 무기 구매
|상점 화면 |구매 불가 화면 |마이페이지 |무기 구매 화면 |
|---|---|---|---|
|![image](https://user-images.githubusercontent.com/62867581/206829988-a9230f95-b6ef-4d1b-95d0-c6e7ab2bbaf8.png)|![image](https://user-images.githubusercontent.com/62867581/206830010-90965e20-ea86-4a5b-8b53-3607fedce589.png)|![image](https://user-images.githubusercontent.com/62867581/206829971-b1488f5d-1585-4e1c-99f7-03f8cf93441b.png)|![image](https://user-images.githubusercontent.com/62867581/206830388-b112c2b7-040a-4c04-804c-d297cbef98ae.png)|
|- 상점에서 사용자는 캐릭터를 구매할 수 있다.|- 보유한 코인이 부족하다면 캐릭터를 구매할 수 없다.|- 마이페이지에서 사용자가 보유하고 있는 캐릭터를 선택해 장착할 수 있다.|각 모드의 플레이 시작 시 원하는 무기를 구매할 수 있다.|

## 인피니티 모드
|인피니티 모드|플레이 화면|궁극기 기능|게임 종료|
|---|---|---|---|
|![Info_infi_1](https://user-images.githubusercontent.com/62867581/206830811-851699e4-9a62-4c26-95b4-71e68c938211.png)|![image](https://user-images.githubusercontent.com/62867581/206830596-390061ec-4487-4505-bbbd-579cea43cebe.png)|![image](https://user-images.githubusercontent.com/62867581/206830623-82d1a90c-780e-4fd1-b206-1c9a9b587334.png)|![image](https://user-images.githubusercontent.com/62867581/206830644-dc8bb7bb-e84c-436e-aef4-e74db45c9c8a.png)|
|- 모드 선택 화면에서 SCORE/TIME의 무한 모드를 선택한다. |- 아이템과 코인을 획득하고 몹을 처치한다. |- 몹을 10마리 잡으면 S키를 이용해 궁극기를 사용할 수 있다.| - 게임이 종료되면 모드 시작시 선택한 랭킹에 등록된다.|

## 랭킹
인피니티 모드에서 선택한 SCORE/TIME에 따라 랭킹이 매겨집니다.
|랭킹 보기|로딩 화면|플레이 화면 |
|---|---|---|
|![image](https://user-images.githubusercontent.com/62867581/206830027-264b696d-21f5-478d-9401-d8d0a6d70003.png)|![image](https://user-images.githubusercontent.com/62867581/206830038-90e1623e-f68f-46e6-addf-d90cd653f571.png)|![image](https://user-images.githubusercontent.com/62867581/206830053-c8262158-2a39-4fc3-9896-a02beed7bef7.png)
|- 랭킹 모드 화면에서 점수 랭킹/ 시간 랭킹을 선택한다. |- 점수별 랭킹을 보여준다.  |- 시간별 랭킹을 보여준다.|

## 스테이지 모드
|스테이지 모드|스토리 라인|플레이 화면|보스 화면|게임 종료 화면|
|---|---|---|---|---|
|![Info_stage_1](https://user-images.githubusercontent.com/62867581/206830782-14bbadc5-e11f-475b-8d2a-d6279d7a75b6.png)|![image](https://user-images.githubusercontent.com/62867581/206830660-4e18aa44-5ae9-4666-82e8-a55565b0b1f3.png) |![image](https://user-images.githubusercontent.com/62867581/206830677-eed0e9a0-7cc6-4aa4-9a6b-872adc3f5eee.png)|![image](https://user-images.githubusercontent.com/62867581/206831104-68982974-8ba2-4d00-90dd-0bbbafb5a73b.png) |![image](https://user-images.githubusercontent.com/62867581/206831151-f70e3393-8952-4368-84ca-75f699837889.png)|
|- 모드 선택 화면에서 원하는 단계의 스테이지 모드를 선택한다. |- 안내메시지로 목표점수를 확인한다. |- SPACE키를 눌러 스토리 라인을 따라간다. |- 목표점수를 도달하면 등장하는 보스를 처치한다.|- 게임이 종료되면 다음 스테이지로 넘어갈 수 있다.|

## 설명서
|아이템 설명서|조작키 설명서|
|---|---|
|![image](https://user-images.githubusercontent.com/62867581/203493629-74f3976a-d194-4553-aef6-5e4ec63fbb52.png)|![image](https://user-images.githubusercontent.com/62867581/203493665-1cb1cf44-deaf-4109-8e05-09609c14f843.png) |


## 부가 기능
|소리 ON/OFF|도움말 페이지|
|---|---|
|![image](https://user-images.githubusercontent.com/62867581/206831334-309cdf9c-eb99-4e57-bf13-d07d81baeb44.png)|![image](https://user-images.githubusercontent.com/62867581/206831467-7765d38a-39d0-4f3d-a701-f0e39e6d762b.png)|
|- 게임모드 선택화면과 게임 플레이 화면에서 소리를  ON/OFF 할 수 있다. |- 게임플레이에 관한 자세한 안내사항은 도움말페이지에서 확인할 수 있다.|

# References

http://www.pygame.org/docs
<br/>
https://pygame-menu.readthedocs.io/en/4.2.0/_source/widgets_frame.html

## Sound credit

https://pixabay.com/ko/music/
```
Winning Elevation - Hot Music
Hip Hop Rock Beats - QubeSounds
Powerful Stylish Stomp Rock (Lets Go) - MarkJuly
Powerful Energetic Sport Rock Trailer - QubeSounds
```
<br/>
others : https://github.com/CSID-DGU/2022-1-OSSProj-DreamsComeTrue-4

## Image credit

All images created by Trio team
