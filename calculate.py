from data import *
from math import log
from decimal import Decimal, getcontext
getcontext().prec = 50

def roll(skill_id, aug_budget, total_skills, kept_skills):
    if total_skills >= max_armor_skills:
        # armor piece cannot have more than maximum of unique armor skills
        print("Armor piece cannot get any more skills from augmentation.")
    else:
        # chance to add selected skill from respective skill pool
        cost_pool = skills[skill_id].aug_cost
        skills_in_pool = len(skill_pools[cost_pool])
        chance_from_pool = 1 / Decimal(skills_in_pool)

        # chance to safely remove unwanted skills
        chance_of_safe_removal = Decimal(total_skills - kept_skills) / Decimal(total_skills)

        # Standard Augmentation
        # adds or removes one skill
        average_def_aug_cost = Decimal("1.080") / Decimal("0.400") # magic number for R10 armor
        average_aug_budget = aug_budget - average_def_aug_cost # forced defense augment
        average_skill_total = total_skills

        total_aug_probs = sum(skill_pool_probs.values())
        chance_of_pool = skill_pool_probs[cost_pool] / total_aug_probs
        chance_of_skill_addition = chance_of_pool * chance_from_pool
        chance_of_pool = skill_pool_probs[-10] / total_aug_probs
        chance_of_skill_removal = chance_of_pool * chance_of_safe_removal

        chance_of_skill_addition *= average_aug_budget / cost_pool # modify skill addition chance by portion of overspent/underspent budget
        chance_from_standard_aug = chance_of_skill_addition + chance_of_skill_removal

        for aug_cost, aug_prob in skill_pool_probs.items(): # decrease average budget by average augment cost
            average_aug_budget -= aug_cost * (aug_prob / total_aug_probs)
        average_skill_total += 1 - (chance_of_pool * 2) # increase average skill total by average added skill chance

        # Skills+ Augmentation
        # adds one skill and removes one skill
        total_aug_probs = sum([prob for cost, prob in skill_pool_probs.items() if cost > 0]) # skill removal guaranteed separately
        chance_of_pool = skill_pool_probs[cost_pool] / total_aug_probs
        chance_of_skill_addition = chance_of_pool * chance_from_pool
        chance_from_skills_plus_aug = chance_of_skill_addition * chance_of_safe_removal

        # chance to add selected skill in additional augments
        def chance_from_added_augs(aug_budget):
            average_aug_cost = Decimal("2.950") # magic number for R10 armor
            average_augs = aug_budget / average_aug_cost
            chance_of_skill_addition = skill_pool_probs[cost_pool] * chance_from_pool
            chance_of_skill_removal = skill_pool_probs[-10] * chance_of_safe_removal
            return 1 - (1 - (chance_of_skill_addition + chance_of_skill_removal)) ** average_augs
        
        chance_from_standard_aug = 1 - (1 - chance_from_standard_aug) * (1 - chance_from_added_augs(average_aug_budget))
        chance_from_skills_plus_aug = 1 - (1 - chance_from_skills_plus_aug) * (1 - chance_from_added_augs(aug_budget + 10))

        # print a block of statistics for each type of armor augmentation
        def print_stats(chance_per_roll):
            print(f"Average chance per roll: {round(chance_per_roll * 100, 3)}%")
            expected_attempts = round(log(Decimal("0.01"),  1 - chance_per_roll), 3)
            print(f"Expected number of attempts to achieve 99% confidence: {expected_attempts}")
            expected_attempts = round(log(Decimal("0.001"),  1 - chance_per_roll), 3)
            print(f"Expected number of attempts to achieve 99.9% confidence: {expected_attempts}")

        print("======= Standard Augmentation =======")
        print_stats(chance_from_standard_aug)

        print()
        
        print("======= Skills+ Augmentation =======")
        print_stats(chance_from_skills_plus_aug)
