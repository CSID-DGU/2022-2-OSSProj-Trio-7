import enum
import math
from operator import truediv
from sys import version

class User:
    user_id = ""
    coin = 0
    character = 0
    buy_character = 0
    price = [0, 100, 100, 200]
    easy_score = 0
    hard_score = 0
    cat_lock = [False,False,False,False]
    

class Images(enum.Enum):
    lock = "./Image/catthema/lock.jpg"
    login = "./Image/Login.png"
    start = "./Image/StartImage.png"
    how_to_play = "./Image/howtoplay.png"
    about = "./Image/AboutPage.jpg"
    background_map1 = "./Image/catthema/map1.png"
    background_map2 = "./Image/catthema/map2.png"
    enemy_scrophion = "./Image/scorphion1-1.png"
    enemy_cactus = "./Image/Catus.png"
    missile_missile2 = "./Image/MISSILE_2.png"
    weapon_target_missile = "./Image/Weapon/spaceMissiles_012.png"

    icon_caution = "./Image/Caution.jpg"
    icon_award = "./Image/Award.jpg"

    stage_clear = "./Image/Stageclear_v1.jpg"
    chapter_clear_oasis = "./Image/ChapterClear_Oasis.jpg"
    chapter_clear_ice = "./Image/ChapterClear_Ice.jpg"
    chapter_clear_space = "./Image/ChapterClear_Space.jpg"
    chapter_cleared = "./Image/ClearedChapter.jpg"
    gameover = "./Image/Gameover_v2.jpg"

    F5S1_locked = "./Image/CharacterLocked_F5S1.jpg"
    F5S4_locked = "./Image/CharacterLocked_F5S4.jpg"
    Tank_locked = "./Image/CharacterLocked_Tank.jpg"
    stage_locked = "./Image/StageLocked_v1.jpg"

    info_infi_1 = "./Image/Info_infi_1.png"
    info_infi_2 = "./Image/Info_infi_2.png"
    info_infi_3 = "./Image/Info_infi_3.png"
    info_infi_4 = "./Image/Info_infi_4.png"
    info_infi_5 = "./Image/Info_infi_5.png"
    info_stage_1 = "./Image/Info_stage_1.png"
    info_stage_2 = "./Image/Info_stage_2.png"
    info_stage_3 = "./Image/Info_stage_3.png"
    info_stage_4 = "./Image/Info_stage_4.png"
    info_stage_5 = "./Image/Info_stage_5.png"
    info_stage_6 = "./Image/Info_stage_6.png"
    info_items = "./Image/Info_items.png"
    info_controls = "./Image/Info_controls.jpg"

    cat1 = "./Image/catthema/cat1_front.png"
    cat2 = "./Image/catthema/cat2_front.png"
    cat3 = "./Image/catthema/cat3_front.png"
    cat4 = "./Image/catthema/cat4_front.png"

    win = "./Image/catthema/win.png"
    lose = "./Image/catthema/lose.png"

    lock_cat2 = "./Image/catthema/lock_cat2.png"
    lock_cat3 = "./Image/catthema/lock_cat3.png"
    lock_cat4 = "./Image/catthema/lock_cat4.png"

    failbuy_cat2 = "./Image/catthema/failbuy_cat2.png"
    failbuy_cat3 = "./Image/catthema/failbuy_cat3.png"
    failbuy_cat4 = "./Image/catthema/failbuy_cat4.png"

class Scales(enum.Enum):
    large = (2, 2)
    default = (1, 1)
    small = (.6, .6)
    tiny = (.1, .1)
    

class Color(enum.Enum):
    RED = (200,60,50)
    BLUE = (0,60,200)
    GREEN = (50,200,50)
    YELLOW = (255,255,0)
    WHITE = (255,255,255)
    TRANSPARENT = (255,255,255,128)
    GRAY = (220,220,220)
    BLACK = (0,0,0)

class Menus(enum.Enum):
    margin_10 = 10
    margin_20 = 20
    margin_40 = 40
    margin_50 = 50
    margin_100 = 100
    margin_200 = 200
    ranking_search_result_margin = (0,20)

    fontsize_50 = 50
    fontsize_30 = 30
    fontsize_25 = 25
    fontsize_default = 20

    ID_maxchar = 20
    table_padding = 10


class Default(enum.Enum):
    game = {
        "size": {
            "x":0, 
            "y":0
            }
    }
    sound = {
        "sfx":{
            "volume": 0.1
        }
    }
    font = "./Font/DXHanlgrumStd-Regular.otf"
    boss = {
        "size": {
            "x":250, 
            "y":250
        },
        "velocity": [
            6,
            8,
            12
        ],
        "gun_size": 10,
        "bullet_size": {
            "x":20, 
            "y":20
        },
        "health": 12000,
        "firing_speed": [
            25, 
            20, 
            15
        ],
        "grace_timers": [
            120,
            90, 
            65
        ],
        "grace_time": 30
    }
    character = {
        "size": {
            "x":40, 
            "y":80
            },
        "invincible_period": 4.0,
        "missile":{
            "min":1,
            "max":4,
            "speed":20,
            "speed_inc":1
            },
        "max_stats":{
            "power":500,
            "fire_rate":0.3,
            "mobility":25
        }
    }
    item = {
        "duration":10.0,
        "size":{
            "x":45, 
            "y":45
        },
        "size2":{
            "x":70,
            "y":35
        },
        "size3":{
            "x":80,
            "y":33
        },
        "sound": "./Sound/Item/speedup.wav",
        "velocity":5,
        "speedup":{
            "spawn_rate": 0.004,
            "frames":[
                "./Image/catthema/item/item_milk.png", 
                "./Image/catthema/item/item_milk.png", 
                "./Image/catthema/item/item_milk.png", 
                "./Image/catthema/item/item_milk.png", 
                "./Image/catthema/item/item_milk.png",
                "./Image/catthema/item/item_milk.png"
            ]
        },
        "powerup":{
            "spawn_rate": 0.004,
            "duration":10.0,
            "frames":[
                "./Image/catthema/item/item_fish.png", 
                "./Image/catthema/item/item_fish.png", 
                "./Image/catthema/item/item_fish.png", 
                "./Image/catthema/item/item_fish.png", 
                "./Image/catthema/item/item_fish.png",
                "./Image/catthema/item/item_fish.png"
            ]
        },
        "bomb":{
            "spawn_rate": 0.004,
            "interval":1.0,
            "power":1000,
            "frames":[
                "./Image/catthema/item/item_chu.png", 
                "./Image/catthema/item/item_chu.png", 
                "./Image/catthema/item/item_chu.png", 
                "./Image/catthema/item/item_chu.png", 
                "./Image/catthema/item/item_chu.png",
                "./Image/catthema/item/item_chu.png"
            ]
        },
        "health":{
            "spawn_rate": 0.002,
            "frames":[
                "./Image/catthema/item/item_heart.png", 
                "./Image/catthema/item/item_heart.png", 
                "./Image/catthema/item/item_heart.png", 
                "./Image/catthema/item/item_heart.png",
                "./Image/catthema/item/item_heart.png"
            ]
        },
        "coin":{
            "spawn_rate": 0.002,
            "frames":[
                "./Image/catthema/item/item_coin.png", 
                "./Image/catthema/item/item_coin.png", 
                "./Image/catthema/item/item_coin.png", 
                "./Image/catthema/item/item_coin.png", 
                "./Image/catthema/item/item_coin.png",
                "./Image/catthema/item/item_coin.png"
            ]
        }
    }
    effect = {
        "speed": 0.4,
        "velocity": 5,
        "bomb":{
            "duration": 7.0,
            "size":{
                "x": 500,
                "y": 500
            },
            "frames": [
                "./Image/Effects/Bomb/frame-1.png", 
                "./Image/Effects/Bomb/frame-2.png", 
                "./Image/Effects/Bomb/frame-3.png", 
                "./Image/Effects/Bomb/frame-4.png", 
                "./Image/Effects/Bomb/frame-5.png", 
                "./Image/Effects/Bomb/frame-6.png", 
                "./Image/Effects/Bomb/frame-7.png", 
                "./Image/Effects/Bomb/frame-8.png", 
                "./Image/Effects/Bomb/frame-9.png",
                "./Image/Effects/Bomb/frame-10.png", 
                "./Image/Effects/Bomb/frame-11.png", 
                "./Image/Effects/Bomb/frame-12.png",
                "./Image/Effects/Bomb/frame-13.png", 
                "./Image/Effects/Bomb/frame-14.png", 
                "./Image/Effects/Bomb/frame-15.png"
            ],
            "sound": "./Sound/Weapon/explosion.wav"
        },
        "boom":{
            "duration": 4.0,
            "size":{
                "x": 150,
                "y": 150
            },
            "frames":[
                "./Image/Effects/Boom/frame-1.png", 
                "./Image/Effects/Boom/frame-2.png", 
                "./Image/Effects/Boom/frame-3.png", 
                "./Image/Effects/Boom/frame-4.png", 
                "./Image/Effects/Boom/frame-5.png", 
                "./Image/Effects/Boom/frame-6.png", 
            ],
            "sound": "./Sound/destroyed.wav"
        },
        "crosshair":{
            "image": "./Image/Effects/Crosshair.png",
            "size": {
                "x": 120,
                "y": 120
            },
            "velocity": 5
        }
    }
    animation = {
        "blink":{
            "speed":0.05,
            "frame":0.2,
            "duration":4.0
        },
        "interval":10.0,
        "speed":0.5
    }
    about = {
        "authors": [
            "Yaena Lee",
            "Mingyeong Jung", 
            "Dahee Choi",
        ],
        "open_source": {

            "SOUNDS":{
                "MATRIXXX_ CC0 1.0": "https://freesound.org/people/MATRIXXX_/sounds/441373/",
                "simoneyoh3998 CC0 1.0": "https://freesound.org/people/simoneyoh3998/sounds/500673/",
                "jalastram CC BY 3.0": "https://freesound.org/people/jalastram/sounds/317769/",
                "befig CC BY 3.0": "https://freesound.org/people/befig/sounds/455530/",
                "Royalty Free Music from Bensound":"www.bensound.com"
            },
            "BASE CODE":{
                "CSID-DGU/2021-1-OSSPC-MUHIRYO-4":"https://github.com/CSID-DGU/2021-1-OSSPC-MUHIRYO-4.git",
                "CSID-DGU/2021-2-OSSProj-PlusAlpha-9":"https://github.com/CSID-DGU/2021-2-OSSProj-PlusAlpha-9"
            }
        }
    }

class Utils():
    @classmethod
    def clamp(cls, val, n_min, n_max):
        return max(n_min, min(val, n_max)) 

    @classmethod
    def get_distance(cls, a, b):
        return math.sqrt((b["x"] - a["x"])**2 + (b["y"] - a["y"])**2)
