import random
import math
import uuid
from typing import Dict
from Script.Core import game_type,cache_control
from Script.Config import game_config
from Script.Design import attr_calculation

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """


def get_npc_cloth(character_id: int):
    """
    根据csv换一身同样的衣服，然后随机内衣
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    无
    """
    if character_id:
        character_data = cache.character_data[character_id]
        character_data.cloth.cloth_wear = attr_calculation.get_cloth_wear_zero()
        tem_character = cache.npc_tem_data[character_id]

        for cloth_id in tem_character.Cloth:
            type = game_config.config_clothing_tem[cloth_id].clothing_type
            # print(f"debug cloth_id = {cloth_id},name = {game_config.config_clothing_tem[cloth_id].name},type = {type}")
            character_data.cloth.cloth_wear[type].append(cloth_id)
        get_underwear(character_id)

def get_underwear(character_id: int, part_flag = 0):
    """
    随机穿内衣，包括胸罩和内裤
    Keyword arguments:
    character_id -- 角色id
    part_flag -- 是否只穿某个部件，0都穿，1仅胸罩，2仅内裤
    Return arguments:
    无
    """
    character_data = cache.character_data[character_id]
    # 60,幼女,61,萝莉,62,少女,63,成年,64,长生者

    # 遍历全衣服，以下分别是正常/童装/情趣的胸罩和内裤
    bra_nor_list = []
    bra_loli_list = []
    bra_H_list = []
    pan_nor_list = []
    pan_loli_list = []
    pan_H_list = []
    for cloth_id in game_config.config_clothing_tem:
        cloth = game_config.config_clothing_tem[cloth_id]
        if cloth.clothing_type == 6:
            if cloth.tag == 0:
                bra_nor_list.append(cloth_id)
            elif cloth.tag == 1:
                bra_loli_list.append(cloth_id)
            elif cloth.tag == 2:
                bra_H_list.append(cloth_id)
        elif cloth.clothing_type == 9:
            if cloth.tag == 0:
                pan_nor_list.append(cloth_id)
            elif cloth.tag == 1:
                pan_loli_list.append(cloth_id)
            elif cloth.tag == 2:
                pan_H_list.append(cloth_id)

    # 解锁了情趣内衣的情况下，对2级攻略以上的角色增加情趣内衣
        for i in {202,203,204,212,213,214}:
            if character_data.talent[i]:
                if cache.character_data[0].pl_collection.collection_bonus == {}:
                    cache.character_data[0].pl_collection = attr_calculation.get_collection_zero()
                if cache.character_data[0].pl_collection.collection_bonus[102]:
                    bra_nor_list += bra_H_list
                    bra_loli_list += bra_H_list
                    pan_nor_list += pan_H_list
                    pan_loli_list += pan_H_list
                    break

    # 判断是否需要穿，包括是否已穿和part_flag限制
    if not len(character_data.cloth.cloth_wear[6]) and part_flag != 2:
        # 随机选择胸衣和内裤，有儿童和普通人两个分支
        if character_data.talent[102] or character_data.talent[103]:
            bra_id = random.choice(bra_loli_list)
            character_data.cloth.cloth_wear[6].append(bra_id)
        else:
            bra_id = random.choice(bra_nor_list)
            character_data.cloth.cloth_wear[6].append(bra_id)

    if not len(character_data.cloth.cloth_wear[9]) and part_flag != 1:
        if character_data.talent[102] or character_data.talent[103]:
            pan_id = random.choice(pan_loli_list)
            character_data.cloth.cloth_wear[9].append(pan_id)
        else:
            pan_id = random.choice(pan_nor_list)
            character_data.cloth.cloth_wear[9].append(pan_id)


def get_cloth_off(character_id: int):
    """
    脱成全裸
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    无
    """
    if character_id:
        character_data = cache.character_data[character_id]
        character_data.cloth.cloth_wear = attr_calculation.get_cloth_wear_zero()
        chara_special_wear_cloth(character_id)


def get_shower_cloth(character_id: int):
    """
    换上浴帽和浴巾
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    无
    """
    if character_id:
        character_data = cache.character_data[character_id]
        get_cloth_wear_zero_except_need(character_id)
        character_data.cloth.cloth_wear[0].append(51)
        character_data.cloth.cloth_wear[5].append(551)
        character_data.cloth.cloth_wear[8].append(851)


def get_sleep_cloth(character_id: int):
    """
    换上睡衣和内裤
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    无
    """
    if character_id:
        character_data = cache.character_data[character_id]
        get_cloth_wear_zero_except_need(character_id)
        choic_flag = random.randint(0,1)
        if choic_flag:
            character_data.cloth.cloth_wear[5].append(552)
            character_data.cloth.cloth_wear[8].append(852)
        else:
            character_data.cloth.cloth_wear[5].append(553)
            character_data.cloth.cloth_wear[8].append(853)
        get_underwear(character_id, part_flag = 2)


def get_swim_cloth(character_id: int):
    """
    换上泳衣的胸衣和内裤
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    无
    """
    if character_id:
        character_data = cache.character_data[character_id]
        get_cloth_wear_zero_except_need(character_id)
        choic_type = random.randint(1,14)
        character_data.cloth.cloth_wear[6].append(choic_type + 680)
        character_data.cloth.cloth_wear[9].append(choic_type + 980)
        chara_special_wear_cloth(character_id)


def chara_special_wear_cloth(character_id: int):
    """
    根据角色设定而穿上必须穿的衣物
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    无
    """
    if character_id:
        character_data = cache.character_data[character_id]
        # print(f"debug name = {character_data.name}")

        # 阿米娅必须戴戒指
        if character_data.adv == 1:
            if 701 not in character_data.cloth.cloth_wear[7]:
                character_data.cloth.cloth_wear[7].append(701)
                # print("换上戒指了")
            return [701]
    return []


def get_cloth_wear_zero_except_need(character_id: int) -> dict:
    """
    遍历当前穿着服装类型，将首饰和必要物品以外的设为空
    """
    character_data = cache.character_data[character_id]
    # print(f"debug 脱衣服前 = {character_data.cloth.cloth_wear}")
    for clothing_type in game_config.config_clothing_type:
        if len(character_data.cloth.cloth_wear[clothing_type]):
            remove_tem_list = []
            for cloth_id in character_data.cloth.cloth_wear[clothing_type]:
                # 只要不是首饰和必须穿着的衣服，就把该服装加入删掉的list里
                if (
                    game_config.config_clothing_tem[cloth_id].tag != 6 
                    and cloth_id not in chara_special_wear_cloth(character_id)
                ):
                    remove_tem_list.append(cloth_id)
            # 获得两个list的差，并赋值给当前服装
            result = [item for item in  character_data.cloth.cloth_wear[clothing_type] if item not in remove_tem_list]
            character_data.cloth.cloth_wear[clothing_type] = result
    # print(f"debug 脱衣服后 = {character_data.cloth.cloth_wear}")



'''
不用的旧函数

def creator_suit(suit_id: int, sex: int) -> Dict[int, game_type.Clothing]:
    """
    创建套装
    Keyword arguments:
    suit_name -- 套装模板
    sex -- 性别模板
    Return arguments:
    Dict[int,game_type.Clothing] -- 套装数据 服装穿戴位置:服装数据
    """
    suit_data = game_config.config_clothing_suit_data[suit_id][sex]
    clothing_data = {}
    for clothing_id in suit_data:
        clothing = creator_clothing(clothing_id)
        clothing_data[clothing.wear] = clothing
    return clothing_data


def creator_clothing(clothing_tem_id: int) -> game_type.Clothing:
    """
    创建服装的基础函数
    Keyword arguments:
    clothing_tem_id -- 服装id
    Return arguments:
    game_type.Clothing -- 生成的服装数据
    """
    clothing_data = game_type.Clothing()
    clothing_data.uid = uuid.uuid4()
    clothing_data.sexy = random.randint(1, 1000)
    clothing_data.handsome = random.randint(1, 1000)
    clothing_data.elegant = random.randint(1, 1000)
    clothing_data.fresh = random.randint(1, 1000)
    clothing_data.sweet = random.randint(1, 1000)
    clothing_data.warm = random.randint(0, 30)
    clothing_data.price = sum(
        [
            clothing_data.__dict__[x]
            for x in clothing_data.__dict__
            if isinstance(clothing_data.__dict__[x], int)
        ]
    )
    clothing_data.cleanliness = 100
    clothing_data.evaluation = game_config.config_clothing_evaluate_list[
        math.floor(clothing_data.price / 480) - 1
    ]
    clothing_data.tem_id = clothing_tem_id
    clothing_data.wear = game_config.config_clothing_tem[clothing_tem_id].clothing_type
    return clothing_data

'''