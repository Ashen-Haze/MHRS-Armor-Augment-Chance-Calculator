import csv
from decimal import Decimal

# armor skill class
class Skill:
    def __init__(self, name, aug_cost):
        self.name = name
        self.aug_cost = aug_cost

max_armor_skills = 5

# dictionary of armor skill IDs
# values are Skill objects
skills = {}
with open("armor_skills.csv") as file:
    data = csv.reader(file)
    skills = {int(id): Skill(name, int(aug_cost)) for id, name, aug_cost in data}

# dictionary of armor skill augment cost pools
# values are lists of skill IDs in each pool
skill_pools = {skill.aug_cost: [] for skill in skills.values()}
for id, skill in skills.items():
    skill_pools[skill.aug_cost].append(id)

# dictionary of probabilities for armor skill augment cost pools
# values are individual probabilities in a single augment roll
skill_pool_probs = {
    3: Decimal("0.06"),
    6: Decimal("0.04"),
    9: Decimal("0.036"),
    12: Decimal("0.028"),
    15: Decimal("0.016"),
    -10: Decimal("0.02"), # pool for skill removal
}

# print a block for every pool of armor skills
def print_armor_skill_list():
    for cost, skill_ids in skill_pools.items():
        print(f"Augments with a cost of {cost}:")
        for id in skill_ids:
            # print every ID with three digits for alignment purposes
            print('0'*(3-len(str(id))) + f"{id}. " + skills[id].name)
        print()
