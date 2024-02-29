import os, re
import calculate, data

def clear_text():
    os.system("cls")

def pause_text():
    os.system("pause")

def select_input_mode():
    clear_text()
    print("Input Modes:")
    print("1. Simple (single skill)")
    print("2. Advanced (multi-skill)")

    simple = re.compile(f"1|s|si|sim|simple", re.IGNORECASE)
    advanced = re.compile("2|a|ad|adv|advanced", re.IGNORECASE)

    print()
    while True:
        mode = input("Select input mode: ")
        if simple.match(mode):
            simple_mode()
            break
        elif advanced.match(mode):
            advanced_mode()
            break

def simple_mode():
    data.print_armor_skill_list()
    skill_id = int(input("Enter the ID of your desired armor skill: "))
    aug_budget = int(input("Enter the augment budget of your armor piece: "))
    total_skills = int(input("Enter the number of unique armor skills present: "))
    kept_skills = int(input("Enter the number of these to keep: "))

    print()
    calculate.roll(skill_id, aug_budget, total_skills, kept_skills)
    print()
    pause_text()
    print()

def advanced_mode():
    pass

while True: # main script
    simple_mode()
