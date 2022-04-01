import copy
from enum import Enum
from random import randint

import pandas as pd


class Camp(Enum):
    Light = 1
    Dark = 2


class Category(Enum):
    Townsman = 1
    Outsider = 2
    Underlings = 3
    Devil = 4


class Role:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.c_name = kwargs["c_name"]
        self.category = kwargs["category"]
        self.camp = kwargs["camp"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


g_roles_repo = {
    Category.Townsman: [
        Role(name="WasherWoman", c_name="洗衣妇", category=Category.Townsman, camp=Camp.Light),
        Role(name="Librarian", c_name="图书管理员", category=Category.Townsman, camp=Camp.Light),
        Role(name="Investigator", c_name="调查员", category=Category.Townsman, camp=Camp.Light),
        Role(name="Chef", c_name="厨师", category=Category.Townsman, camp=Camp.Light),
        Role(name="Empath", c_name="共情者", category=Category.Townsman, camp=Camp.Light),
        Role(name="FortuneTeller", c_name="占卜师", category=Category.Townsman, camp=Camp.Light),
        Role(name="Undertaker", c_name="送葬者", category=Category.Townsman, camp=Camp.Light),
        Role(name="Monk", c_name="僧侣", category=Category.Townsman, camp=Camp.Light),
        # Role(name="RavenKeeper", c_name="渡鸦看守者", category=Category.Townsman, camp=Camp.Light),
        Role(name="Virgin", c_name="童真者", category=Category.Townsman, camp=Camp.Light),
        Role(name="Slayer", c_name="杀手", category=Category.Townsman, camp=Camp.Light),
        Role(name="Soldier", c_name="士兵", category=Category.Townsman, camp=Camp.Light),
        Role(name="Mayor", c_name="市长", category=Category.Townsman, camp=Camp.Light),

        Role(name="WatchMaker", c_name="钟表匠", category=Category.Townsman, camp=Camp.Light),
        Role(name="Mathematician", c_name="数学家", category=Category.Townsman, camp=Camp.Light),

        Role(name="Philosopher", c_name="哲学家", category=Category.Townsman, camp=Camp.Light),
    ],

    Category.Outsider: [
        # Role(name="Butler", c_name="管家", category=Category.Outsider, camp=Camp.Light),
        Role(name="Drunk", c_name="酒鬼", category=Category.Outsider, camp=Camp.Light),
        # Role(name="Recluse", c_name="隐士", category=Category.Outsider, camp=Camp.Light),
        Role(name="Saint", c_name="圣徒", category=Category.Outsider, camp=Camp.Light),

        Role(name="Fool", c_name="傻瓜", category=Category.Outsider, camp=Camp.Light),
        Role(name="Lover", c_name="心上人", category=Category.Outsider, camp=Camp.Light),

        Role(name="Lunatic", c_name="疯子", category=Category.Underlings, camp=Camp.Dark),
    ],

    Category.Underlings: [
        Role(name="Poisoner", c_name="投毒者", category=Category.Underlings, camp=Camp.Dark),
        Role(name="Spy", c_name="间谍", category=Category.Underlings, camp=Camp.Dark),
        Role(name="ScarletWoman", c_name="荡妇", category=Category.Underlings, camp=Camp.Dark),
        Role(name="Baron", c_name="男爵", category=Category.Underlings, camp=Camp.Dark),

        # Role(name="EvilTwin", c_name="邪恶双子", category=Category.Underlings, camp=Camp.Dark),

        Role(name="GodFather", c_name="教父", category=Category.Underlings, camp=Camp.Dark),
    ],

    Category.Devil: [
        Role(name="LittleDevil", c_name="小恶魔", category=Category.Devil, camp=Camp.Dark),
        Role(name="Carrion", c_name="腐肢", category=Category.Devil, camp=Camp.Dark),

        Role(name="Zombie", c_name="丧尸", category=Category.Underlings, camp=Camp.Dark),
    ]
}

g_roles_repo_copy = copy.deepcopy(g_roles_repo)

# g_must_have = ["WasherWoman", "Investigator", "Chef", "FortuneTeller", "Empath", "Drunk"]
# g_must_have = ["Librarian", "Drunk"]
g_must_have = ["Philosopher", "WatchMaker", "Librarian", "Investigator", "Mathematician", "Lunatic", "Drunk", "GodFather", "Zombie"]

camp_division = {
    5: [3, 0, 1, 1],
    6: [3, 1, 1, 1],
    7: [5, 0, 1, 1],
    8: [5, 1, 1, 1],
    9: [5, 2, 1, 1],
    10: [7, 0, 2, 1],
    11: [7, 1, 2, 1],
    12: [7, 2, 2, 1],
    13: [9, 0, 3, 1],
    14: [9, 1, 3, 1],
    15: [9, 2, 3, 1]
}

g_players_table = None
g_roles = {}


def init():
    pass


def establish_roles_pool():
    global g_players_table
    global g_roles_repo
    global g_roles_repo_copy
    global g_must_have

    # print(g_players_table)
    number_of_players = g_players_table.shape[0]
    print(number_of_players)
    division = camp_division[number_of_players]

    print(division)

    roles_repo = g_roles_repo_copy
    select_roles_from_repo(Category.Underlings, division[2], roles_repo)
    has_baron = False
    for ele in g_roles[Category.Underlings]:
        if ele.name == "Baron":
            has_baron = True
    if has_baron:
        print("Baron is selected, adjust role division, two more outsiders and two less townsman")
        division[1] -= 2
        division[0] += 2

    has_godfather = False
    for ele in g_roles[Category.Underlings]:
        if ele.name == "GodFather":
            has_godfather = True
    if has_godfather:
        plus = randint(0, 1)

        if "Drunk" in g_must_have or "Lunatic" in g_must_have:
            plus = 1

        if plus == 0:
            plus = -1
            print("GodFather is selected, adjust role division, number of outsiders plus {}".format(plus))
        else:
            print("GodFather is selected, adjust role division, number of outsiders plus {}".format(plus))
        division[1] += plus
        division[0] -= plus

    select_roles_from_repo(Category.Townsman, division[0], roles_repo)
    select_roles_from_repo(Category.Outsider, division[1], roles_repo)
    select_roles_from_repo(Category.Devil, division[3], roles_repo)


def select_roles_from_repo(category, number, roles_repo):
    print("Select roles from {}".format(category))
    global g_roles
    global g_must_have
    if g_roles.get(category) is None:
        g_roles[category] = []

    # check must have
    for role_str in g_must_have:
        for role in roles_repo[category]:
            if role.name == role_str and number > 0:
                number = number - 1

                g_roles[category].insert(-1, roles_repo[category].pop(roles_repo[category].index(role)))

    for i in range(0, number):
        number_of_roles_left = len(roles_repo[category])
        selected = randint(0, number_of_roles_left - 1)

        g_roles[category].insert(-1, roles_repo[category].pop(selected))

    print("     Selected {}: {}".format(category, g_roles[category]))
    print("     Left {}: {}".format(category, roles_repo[category]))
    # print("g_roles_repo {}: {}".format(category, g_roles_repo[category]))


def dispatch_roles_to_players():
    global g_players_table
    global g_roles

    selected_roles_list = g_roles[Category.Townsman].copy()
    selected_roles_list.extend(g_roles[Category.Outsider])
    selected_roles_list.extend(g_roles[Category.Underlings])
    selected_roles_list.extend(g_roles[Category.Devil])

    for ind in g_players_table.index:
        # print(g_players_table['Name'][ind], g_players_table['Role'][ind])
        number_of_roles_left = len(selected_roles_list)
        selected = randint(0, number_of_roles_left - 1)

        role = selected_roles_list.pop(selected)
        g_players_table['Role'][ind] = role.name
        g_players_table['Role_Chinese'][ind] = role.c_name
        # print(g_players_table['Name'][ind], g_players_table['Role'][ind])


def is_category(role, category):
    for item in g_roles_repo[category]:
        if isinstance(role, Role) and role.name == item.name:
            return True
        elif isinstance(role, str) and role == item.name:
            return True

    return False


def find_index_by_col(players_table, col, value):
    for ind in players_table.index:
        if players_table[col][ind] == value:
            return ind


def suggest_role(role_name, ind):
    global g_players_table
    global g_roles_repo
    global g_roles_repo_copy
    global g_roles

    suggestion = ""
    rows = g_players_table.shape[0]

    if role_name == "WasherWoman":
        # sober
        solid_role = g_roles[Category.Townsman][0]
        solid_role_index = find_index_by_col(g_players_table, "Role", solid_role.name)
        another_role_index = randint(1, rows - 2)
        if another_role_index >= solid_role_index:
            another_role_index += 1
        if another_role_index >= ind:
            another_role_index += 1

        # Poisoned
        poisoned_role_seed = randint(1, len(g_roles_repo[Category.Townsman]))
        drunk_role = g_roles_repo[Category.Townsman][poisoned_role_seed - 1]

        poisoned_random_index1 = randint(1, rows - 1)
        if poisoned_random_index1 >= ind:
            poisoned_random_index1 += 1

        poisoned_random_index2 = randint(1, rows - 1)
        if poisoned_random_index2 >= ind:
            poisoned_random_index2 += 1

        if poisoned_random_index2 == poisoned_random_index1:
            poisoned_random_index2 = randint(1, rows - 1)
            if poisoned_random_index2 >= ind:
                poisoned_random_index2 += 1

        suggestion = "正常状态： {solid_role_index}和{random_role_index}中有{solid_role}    " \
                     "醉酒或中毒： {poisoned_random_index1}和{poisoned_random_index2}中有{drunk_role}".format(
            solid_role_index=solid_role_index,
            random_role_index=another_role_index,
            solid_role=solid_role.c_name,
            poisoned_random_index1=poisoned_random_index1,
            poisoned_random_index2=poisoned_random_index2,
            drunk_role=drunk_role.c_name)

    elif role_name == "Librarian":
        # There is no outsider in game
        if len(g_roles[Category.Outsider]) == 0:
            return

        # sober
        solid_role = g_roles[Category.Outsider][0]
        solid_role_index = find_index_by_col(g_players_table, "Role", solid_role.name)
        random_role_index = randint(1, rows - 2)
        if random_role_index >= solid_role_index:
            random_role_index += 1
        if random_role_index >= ind:
            random_role_index += 1

        # Poisoned
        poisoned_role_seed = randint(1, len(g_roles_repo[Category.Outsider]))
        drunk_role = g_roles_repo[Category.Outsider][poisoned_role_seed - 1]

        poisoned_random_index1 = randint(1, rows)
        poisoned_random_index2 = randint(1, rows)

        if poisoned_random_index2 == poisoned_random_index1:
            poisoned_random_index2 = randint(1, rows)
        suggestion = "正常状态： {solid_role_index}和{random_role_index}中有{solid_role}    " \
                     "醉酒或中毒： {poisoned_random_index1}和{poisoned_random_index2}中有{drunk_role}".format(
            solid_role_index=solid_role_index, random_role_index=random_role_index, solid_role=solid_role.c_name,
            poisoned_random_index1=poisoned_random_index1, poisoned_random_index2=poisoned_random_index2,
            drunk_role=drunk_role.c_name)

    elif role_name == "Investigator":
        # sober
        solid_role = g_roles[Category.Underlings][0]
        solid_role_index = find_index_by_col(g_players_table, "Role", solid_role.name)
        random_role_index = randint(1, rows - 2)
        if random_role_index >= solid_role_index:
            random_role_index += 1
        if random_role_index >= ind:
            random_role_index += 1

        # poisoned
        drunk_role_seed = randint(1, len(g_roles_repo[Category.Underlings]))
        drunk_role = g_roles_repo[Category.Underlings][drunk_role_seed - 1]

        poisoned_random_index1 = randint(1, rows)
        poisoned_random_index2 = randint(1, rows)
        if poisoned_random_index2 == poisoned_random_index1:
            poisoned_random_index2 = randint(1, rows)
        suggestion = "正常状态： {solid_role_index}和{random_role_index}中有{solid_role}    " \
                     "醉酒或中毒： {poisoned_random_index1}和{poisoned_random_index2}中有{drunk_role}".format(
            solid_role_index=solid_role_index, random_role_index=random_role_index, solid_role=solid_role.c_name,
            poisoned_random_index1=poisoned_random_index1, poisoned_random_index2=poisoned_random_index2,
            drunk_role=drunk_role.c_name)

    elif role_name == "Chef":
        randon_seed = randint(0, 1)
        suggestion = "醉酒或中毒： {random_seed}对邻座".format(random_seed=randon_seed)

    elif role_name == "Empath":
        randon_seed = randint(0, 2)
        suggestion = "醉酒或中毒： 左右两侧{random_seed}个是邪恶的".format(random_seed=randon_seed)

    elif role_name == "FortuneTeller":
        fake_devil = g_roles[Category.Townsman][-1]
        fake_devil_index = find_index_by_col(g_players_table, "Role", fake_devil.name)
        suggestion = "{fake_devil_index}被视为恶魔".format(fake_devil_index=fake_devil_index)

    elif role_name == "WatchMaker":
        distance = 0

        devil_index = 0
        for an_index in g_players_table.index:
            if is_category(g_players_table["Role"][an_index], Category.Devil):
                devil_index = an_index
                break
        print("WatchMaker: devil_index is {}".format(devil_index))

        for an_index in g_players_table.index:
            if is_category(g_players_table["Role"][an_index], Category.Underlings):
                a_dist = abs(an_index - devil_index) - 1
                print("WatchMaker: first calculated dist is {}".format(a_dist))
                another_dist = rows - 2 - a_dist
                print("WatchMaker: another calculated dist is {}".format(another_dist))
                a_dist = min(a_dist, another_dist)
                print("WatchMaker: a_dist is {}".format(a_dist))
                if a_dist > distance:
                    distance = a_dist

        random_distance = randint(0, g_players_table.shape[0] / 2 - 1)
        if random_distance == distance:
            random_distance = randint(0, g_players_table.shape[0] / 2 - 1)
        suggestion = "正常状态： 间隔{}个玩家    " \
                     "醉酒或中毒： 间隔{}个玩家".format(distance, random_distance)
        g_players_table['First_Night_Suggestion'][ind] = suggestion

    elif role_name == "Mathematician":
        random_seed = randint(0, 3)
        suggestion = "醉酒或中毒： {}".format(random_seed)

    elif role_name == "Philosopher":
        suggestion = ""
        suggestion += "【洗衣妇：{}】    ".format(suggest_role("WasherWoman", ind))
        suggestion += "【图书管理员：{}】    ".format(suggest_role("Librarian", ind))
        suggestion += "【调查员：{}】    ".format(suggest_role("Investigator", ind))
        suggestion += "【厨师：{}】    ".format(suggest_role("Chef", ind))
        suggestion += "【共情者：{}】    ".format(suggest_role("Empath", ind))
        suggestion += "【占卜师：{}】    ".format(suggest_role("FortuneTeller", ind))
        suggestion += "【钟表匠：{}】    ".format(suggest_role("WatchMaker", ind))
        suggestion += "【数学家：{}】    ".format(suggest_role("Mathematician", ind))

    elif role_name == "Drunk":
        print("Drunk: available townsman: {}".format(g_roles_repo_copy[Category.Townsman]))
        fake_townsman_index = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        fake_townsman = g_roles_repo_copy[Category.Townsman][fake_townsman_index]
        suggestion = "你是{}  ".format(fake_townsman.c_name)

        suggestion += suggest_role(fake_townsman.name, ind)

    elif role_name == "Lunatic":
        print("Lunatic: available devil: {}".format(g_roles_repo[Category.Devil]))
        fake_devil_index = randint(0, len(g_roles_repo[Category.Devil]) - 1)
        fake_devil_role = g_roles_repo[Category.Devil][fake_devil_index]
        print("Lunatic: {}".format(fake_devil_role))
        suggestion = "你的角色是{}    ".format(fake_devil_role.c_name)

        print("Lunatic: available townsman: {}".format(g_roles_repo_copy[Category.Townsman]))
        print("Lunatic: available outsider: {}".format(g_roles_repo_copy[Category.Outsider]))
        randon_seed1 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed1_role = g_roles_repo_copy[Category.Townsman][randon_seed1]

        randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        if randon_seed2 == randon_seed1:
            randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed2_role = g_roles_repo_copy[Category.Townsman][randon_seed2]

        randon_seed3 = randint(0, len(g_roles_repo_copy[Category.Outsider]) - 1)
        randon_seed3_role = g_roles_repo_copy[Category.Outsider][randon_seed3]
        suggestion += "{randon_seed1_role} {randon_seed2_role} {randon_seed3_role}".format(
            randon_seed1_role=randon_seed1_role.c_name,
            randon_seed2_role=randon_seed2_role.c_name,
            randon_seed3_role=randon_seed3_role.c_name)

    elif role_name == "GodFather":
        suggestion = ""
        for an_index in g_players_table.index:
            if is_category(g_players_table["Role"][an_index], Category.Outsider):
                suggestion += "{} ".format(g_players_table["Role_Chinese"][an_index])

    elif role_name == "LittleDevil":
        print("LittleDevil: available townsman: {}".format(g_roles_repo_copy[Category.Townsman]))
        print("LittleDevil: available outsider: {}".format(g_roles_repo_copy[Category.Outsider]))
        randon_seed1 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed1_role = g_roles_repo_copy[Category.Townsman][randon_seed1]

        randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        if randon_seed2 == randon_seed1:
            randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed2_role = g_roles_repo_copy[Category.Townsman][randon_seed2]

        randon_seed3 = randint(0, len(g_roles_repo_copy[Category.Outsider]) - 1)
        randon_seed3_role = g_roles_repo_copy[Category.Outsider][randon_seed3]
        suggestion = "{randon_seed1_role} {randon_seed2_role} {randon_seed3_role}".format(
            randon_seed1_role=randon_seed1_role.c_name,
            randon_seed2_role=randon_seed2_role.c_name,
            randon_seed3_role=randon_seed3_role.c_name)

    elif role_name == "Carrion":
        print("Carrion: available townsman: {}".format(g_roles_repo_copy[Category.Townsman]))
        print("Carrion: available outsider: {}".format(g_roles_repo_copy[Category.Outsider]))
        randon_seed1 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed1_role = g_roles_repo_copy[Category.Townsman][randon_seed1]

        randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        if randon_seed2 == randon_seed1:
            randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed2_role = g_roles_repo_copy[Category.Townsman][randon_seed2]

        randon_seed3 = randint(0, len(g_roles_repo_copy[Category.Outsider]) - 1)
        randon_seed3_role = g_roles_repo_copy[Category.Outsider][randon_seed3]
        suggestion = "{randon_seed1_role} {randon_seed2_role} {randon_seed3_role}".format(
            randon_seed1_role=randon_seed1_role.c_name,
            randon_seed2_role=randon_seed2_role.c_name,
            randon_seed3_role=randon_seed3_role.c_name)

        left_townsman_idx = rows if ind == 1 else ind - 1
        right_townsman_idx = 1 if ind == rows else ind + 1

        print("Carrion: left_townsman_idx is {}".format(left_townsman_idx))
        print("Carrion: right_townsman_idx is {}".format(right_townsman_idx))
        while True:
            if is_category(g_players_table["Role"][left_townsman_idx], Category.Townsman):
                print(
                    "Carrion: {left_townsman_idx} {role} is Townsman, break".format(left_townsman_idx=left_townsman_idx,
                                                                                    role=g_players_table["Role"][
                                                                                        left_townsman_idx]))
                break
            else:
                print("Carrion: {left_townsman_idx} {role} is not Townsman, continue".format(
                    left_townsman_idx=left_townsman_idx,
                    role=g_players_table["Role"][left_townsman_idx]))

            left_townsman_idx = rows if left_townsman_idx == 1 else left_townsman_idx - 1

        while True:
            if is_category(g_players_table["Role"][right_townsman_idx], Category.Townsman):
                print(
                    "Carrion: {right_townsman_idx} {role} is Townsman, break".format(
                        right_townsman_idx=right_townsman_idx,
                        role=g_players_table["Role"][
                            right_townsman_idx]))
                break
            else:
                print("Carrion: {right_townsman_idx} {role} is not Townsman, continue".format(
                    right_townsman_idx=right_townsman_idx,
                    role=g_players_table["Role"][right_townsman_idx]))

            right_townsman_idx = 1 if right_townsman_idx == rows else right_townsman_idx + 1

        suggestion += "  {left_townsman_idx}和{right_townsman_idx}中毒了".format(
            left_townsman_idx=left_townsman_idx,
            right_townsman_idx=right_townsman_idx)
        g_players_table['First_Night_Suggestion'][
            ind] = suggestion

    elif role_name == "Zombie":
        print("Zombie: available townsman: {}".format(g_roles_repo_copy[Category.Townsman]))
        print("Zombie: available outsider: {}".format(g_roles_repo_copy[Category.Outsider]))
        randon_seed1 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed1_role = g_roles_repo_copy[Category.Townsman][randon_seed1]

        randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        if randon_seed2 == randon_seed1:
            randon_seed2 = randint(0, len(g_roles_repo_copy[Category.Townsman]) - 1)
        randon_seed2_role = g_roles_repo_copy[Category.Townsman][randon_seed2]

        randon_seed3 = randint(0, len(g_roles_repo_copy[Category.Outsider]) - 1)
        randon_seed3_role = g_roles_repo_copy[Category.Outsider][randon_seed3]
        suggestion += "{randon_seed1_role} {randon_seed2_role} {randon_seed3_role}".format(
            randon_seed1_role=randon_seed1_role.c_name,
            randon_seed2_role=randon_seed2_role.c_name,
            randon_seed3_role=randon_seed3_role.c_name)




    return suggestion


def first_night_suggestion():
    global g_players_table
    global g_roles

    for ind in g_players_table.index:
        role_name = g_players_table['Role'][ind]
        suggestion = suggest_role(role_name, ind)

        g_players_table['First_Night_Suggestion'][ind] = suggestion


def load_players_list():
    global g_players_table
    g_players_table = pd.read_excel('players.xlsx', index_col=0)
    g_players_table["Role"] = "NAN"
    g_players_table["Role_Chinese"] = "NAN"
    # g_players_table["Status"] = ""
    g_players_table["First_Night_Suggestion"] = "NAN"


def generate_game():
    global g_players_table
    g_players_table.to_excel("game.xlsx")


def main():
    global g_players_table
    global g_roles_repo

    load_players_list()

    establish_roles_pool()

    dispatch_roles_to_players()

    first_night_suggestion()
    print(g_players_table)

    generate_game()


if __name__ == '__main__':
    main()
