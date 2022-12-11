import enum
import math
from operator import truediv
from sys import version


class User:
    user_id = ""
    user_nickname = ""
    coin = 0
    pcharacter = 0
    fcharacter = 3
    dcharacter = 6
    buy_pcharacter = 0
    buy_fcharacter = 3
    buy_dcharacter = 6
    price = [0, 0, 8000, 8000]
    score_score = 0
    time_score = 0.0

    police_lock = [False, False, False]
    firefighter_lock = [False, False, False]
    doctor_lock = [False, False, False]

class Images(enum.Enum):
    lock = "./Image/catthema/lock.jpg"
    login = "./Image/main.png"
    main = "./Image/main.png"
    characterSelect = "./Image/characterSelect_background.png"
    weaponback = "./Image/weaponSelect/wbackground.png"
    weapon_target_missile = "./Image/Weapon/spaceMissiles_012.png"
    pausedInfo = "./Image/thema/pauseInfo.png"
    icon_caution = "./Image/Caution.jpg"
    icon_award = "./Image/Award.jpg"

    stage_clear = "./Image/stageclearpage.png"

    info_infi_1 = "./Image/Info_infi_1.png"
    info_infi_2 = "./Image/Info_infi_2.png"
    info_infi_3 = "./Image/Info_infi_3.png"
    info_infi_4 = "./Image/Info_infi_4.png"
    info_infi_5 = "./Image/Info_infi_5.png"
    info_infi_6 = "./Image/Info_infi_6.png"
    info_stage_1 = "./Image/Info_stage_1.png"
    info_stage_2 = "./Image/Info_stage_2.png"
    info_stage_3 = "./Image/Info_stage_3.png"
    info_stage_4 = "./Image/Info_stage_4.png"
    info_stage_5 = "./Image/Info_stage_5.png"
    info_stage_6 = "./Image/Info_stage_6.png"
    info_stage_7 = "./Image/Info_stage_7.png"
    info_items = "./Image/Info_items.png"
    info_controls = "./Image/Info_controls.png"

    win = "./Image/stageclear.png"

    failbuy_doctor1 = "./Image/thema/failbuy_doctor1.png"
    failbuy_doctor2 = "./Image/thema/failbuy_doctor2.png"
    failbuy_fire1 = "./Image/thema/failbuy_fire1.png"
    failbuy_fire2 = "./Image/thema/failbuy_fire2.png"
    failbuy_police1 = "./Image/thema/failbuy_police1.png"
    failbuy_police2 = "./Image/thema/failbuy_police2.png"

    police = "./Image/policeCharacters/policeOfficer.png"
    police1 = "./Image/storeItems/police1.png"
    police2 = "./Image/storeItems/police2.png"
    fire = "./Image/fireCharacters/firefighter.png"
    fire1 = "./Image/storeItems/firefighter1.png"
    fire2 = "./Image/storeItems/firefighter2.png"

    doctor = "./Image/doctorCharacters/doctor.png"
    doctor1 = "./Image/storeItems/doctor1.png"
    doctor2 = "./Image/storeItems/doctor2.png"

    doctor_w1 = "./Image/storeItems/syringe.png"
    doctor_w2 = "./Image/storeItems/stethoscope.png"
    police_w1 = "./Image/storeItems/baton.png"
    police_w2 = "./Image/storeItems/stun_gun.png"
    fire_w1 = "./Image/storeItems/fire_hose.png"
    fire_w2 = "./Image/storeItems/fire_extinguisher.png"

    JobInfo = "./Image/JobInfo.png"

    help = "./Image/help.png";
    ranking = "./Image/ranking.png";
    stop = "./Image/stop.png";
    gameover = "./Image/gameover.png"; 
    mypage = "./Image/mypage.png"; 
    store = "./Image/store.png"; 

class Scales(enum.Enum):
    large = (2, 2)
    default = (1, 1)
    small = (.6, .6)
    tiny = (.1, .1)


class Color(enum.Enum):
    RED = (200, 60, 50)
    BLUE = (0, 60, 200)
    GREEN = (50, 200, 50)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    TRANSPARENT = (255, 255, 255, 128)
    GRAY = (220, 220, 220)
    ORANGE = (253, 111, 34)
    BLACK = (0, 0, 0)
    INDIGO = (0, 10, 63)
    NAVY = (0, 10, 63)
    SKYBLUE = (0, 100, 162)



class Menus(enum.Enum):
    margin_10 = 10
    margin_20 = 20
    margin_40 = 40
    margin_50 = 50
    margin_100 = 100
    margin_200 = 200
    ranking_search_result_margin = (0, 20)

    fontsize_50 = 50
    fontsize_30 = 30
    fontsize_25 = 25
    fontsize_default = 20

    ID_maxchar = 20
    table_padding = 10


class Default(enum.Enum):
    game = {
        "size": {
            "x": 0,
            "y": 0
        }
    }
    sound = {
        "sfx": {
            "volume": 0.1
        }
    }
    font = "./Font/강원교육튼튼.ttf"
    boss = {
        "size": {
            "x": 250,
            "y": 250
        },
        "velocity": [
            6,
            8,
            12
        ],
        "gun_size": 10,
        "bullet_size": {
            "x": 50,
            "y": 50
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
            "x": 40,
            "y": 80
        },
        "invincible_period": 4.0,
        "missile": {
            "min": 1,
            "max": 4,
            "speed": 20,
            "speed_inc": 1
        },
        "max_stats": {
            "power": 500,
            "fire_rate": 0.3,
            "mobility": 25
        }
    }
    item = {
        "duration": 10.0,
        "size": {
            "x": 45,
            "y": 45
        },
        "size2": {
            "x": 70,
            "y": 35
        },
        "size3": {
            "x": 80,
            "y": 33
        },
        "sound": "./Sound/Item/speedup.wav",
        "velocity": 5,
        "speedup": {
            "spawn_rate": 0.002,
            "frames": [
                "./Image/catthema/item/item_milk.png",
                "./Image/catthema/item/item_milk.png",
                "./Image/catthema/item/item_milk.png",
                "./Image/catthema/item/item_milk.png",
                "./Image/catthema/item/item_milk.png",
                "./Image/catthema/item/item_milk.png"
            ]
        },
        "powerup": {
            "spawn_rate": 0.002,
            "duration": 10.0,
            "frames": [
                "./Image/catthema/item/item_fish.png",
                "./Image/catthema/item/item_fish.png",
                "./Image/catthema/item/item_fish.png",
                "./Image/catthema/item/item_fish.png",
                "./Image/catthema/item/item_fish.png",
                "./Image/catthema/item/item_fish.png"
            ]
        },
        "bomb": {
            "spawn_rate": 0.002,
            "interval": 1.0,
            "power": 1000,
            "frames": [
                "./Image/Item/bomb.png",
                "./Image/Item/bomb.png",
                "./Image/Item/bomb.png",
                "./Image/Item/bomb.png",
                "./Image/Item/bomb.png",
                "./Image/Item/bomb.png"
            ]
        },
        "health": {
            "spawn_rate": 0.002,
            "frames": [
                "./Image/Item/heart.png",
                "./Image/Item/heart.png",
                "./Image/Item/heart.png",
                "./Image/Item/heart.png",
                "./Image/Item/heart.png"
            ]
        },
        "100won": {
            "spawn_rate": 0.002,
            "frames": [
                "./Image/Item/100won.png",
                "./Image/Item/100won.png",
                "./Image/Item/100won.png",
                "./Image/Item/100won.png",
                "./Image/Item/100won.png",
                "./Image/Item/100won.png"
            ]
        },
        "500won": {
            "spawn_rate": 0.001,
            "frames": [
                "./Image/Item/500won.png",
                "./Image/Item/500won.png",
                "./Image/Item/500won.png",
                "./Image/Item/500won.png",
                "./Image/Item/500won.png",
                "./Image/Item/500won.png"
            ]
        },
        "1000won": {
            "spawn_rate": 0.0005,
            "frames": [
                "./Image/Item/1000won.png",
                "./Image/Item/1000won.png",
                "./Image/Item/1000won.png",
                "./Image/Item/1000won.png",
                "./Image/Item/1000won.png",
                "./Image/Item/1000won.png"
            ]
        }
    }
    effect = {
        "speed": 0.4,
        "velocity": 5,
        "bomb": {
            "duration": 7.0,
            "size": {
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
        "boom": {
            "duration": 4.0,
            "size": {
                "x": 150,
                "y": 150
            },
            "frames": [
                "./Image/Effects/Boom/frame-1.png",
                "./Image/Effects/Boom/frame-2.png",
                "./Image/Effects/Boom/frame-3.png",
                "./Image/Effects/Boom/frame-4.png",
                "./Image/Effects/Boom/frame-5.png",
                "./Image/Effects/Boom/frame-6.png",
            ],
            "sound": "./Sound/destroyed.wav"
        },
        "crosshair": {
            "image": "./Image/Effects/Crosshair.png",
            "size": {
                "x": 120,
                "y": 120
            },
            "velocity": 5
        }
    }
    animation = {
        "blink": {
            "speed": 0.05,
            "frame": 0.2,
            "duration": 4.0
        },
        "interval": 10.0,
        "speed": 0.5
    }
    about = {
        "authors": [
            "Yaena Lee",
            "Mingyeong Jung",
            "Dahee Choi",
        ],
        "open_source": {

            "SOUNDS": {
                # shooting from a weapon
                "MATRIXXX_ CC0 1.0": "https://freesound.org/people/MATRIXXX_/sounds/441373/",
                # explosion of a bomb of normal length
                "simoneyoh3998 CC0 1.0": "https://freesound.org/people/simoneyoh3998/sounds/500673/",
                "jalastram CC BY 3.0": "https://freesound.org/people/jalastram/sounds/317769/",
                "befig CC BY 3.0": "https://freesound.org/people/befig/sounds/455530/",
                "Royalty Free Music from Bensound": "www.bensound.com"
            },
            "BASE CODE": {
                "CSID-DGU/2021-1-OSSPC-MUHIRYO-4": "https://github.com/CSID-DGU/2021-1-OSSPC-MUHIRYO-4.git",
                "CSID-DGU/2021-2-OSSProj-PlusAlpha-9": "https://github.com/CSID-DGU/2021-2-OSSProj-PlusAlpha-9"
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
