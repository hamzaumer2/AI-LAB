# HAMZA UMER FAROOQ - 200789
# BSCS 6 B
# AI LAB QUIZ 1
# QUESTION 2


import random

def goalTest(resultant_state, goal_state):
    if resultant_state == goal_state:
        return True
    else:
        return False


def get_percept(loc, state_space):
    loc, state_space = rule_action(loc, state_space)
    return loc, state_space

def rule_action(loc, state_space):
    if loc == "A":
        if state_space[loc] == 1:
            print("Dirty..... Wiping Dirt in A...\n")
            state_space[loc] = 0
        if state_space[loc] == 2:
            print(" Messy..... Dusting Dirt in A...\n")
            state_space[loc] = 0
        else:
            print("A is clean, moving to next location...\n")
        return "B", state_space
    
    elif loc == "B":
        if state_space[loc] == 1:
            print("Dirty..... Wiping Dirt in B...\n")
            state_space[loc] = 0
        if state_space[loc] == 2:
            print(" Messy..... Dusting Dirt in B...\n")
            state_space[loc] = 0
        else:
            print("B is clean, moving to next location...\n")
        return "C", state_space
        
    elif loc == "C":
        if state_space[loc] == 1:
            print("Dirty..... Wiping Dirt in C...\n")
            state_space[loc] = 0
        if state_space[loc] == 2:
            print(" Messy..... Dusting Dirt in C...\n")
            state_space[loc] = 0
        else:
            print("C is clean, moving to next location...\n")
        return "D", state_space
        
    elif loc == "D":
        if state_space[loc] == 1:
            print("Dirty..... Wiping Dirt in D...\n")
            state_space[loc] = 0
        if state_space[loc] == 2:
            print(" Messy..... Dusting Dirt in D...\n")
            state_space[loc] = 0
        else:
            print("D is clean, moving to next location...\n")
        return "E", state_space
        
    elif loc == "E":
        if state_space[loc] == 1:
            print("Dirty..... Wiping Dirt in E...\n")
            state_space[loc] = 0
        if state_space[loc] == 2:
            print(" Messy..... Dusting Dirt in E...\n")
            state_space[loc] = 0
        else:
            print("E is clean, moving to next location...\n")
        return "F", state_space
    
    elif loc == "F":
        if state_space[loc] == 1:
            print("Dirty..... Wiping Dirt in F...\n")
            state_space[loc] = 0
        if state_space[loc] == 2:
            print(" Messy..... Dusting Dirt in F...\n")
            state_space[loc] = 0
        else:
            print("F is clean, moving to next location...\n")
        return "A", state_space


state_space = {"A": 1, "B": 2, "C": 1, "D": 2, "E": 2, "F": 1} # start state
goal_state = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0} # goal state
goal = False
path_cost = 0

state_space["A"] = random.choice([0, 1, 2])
state_space["B"] = random.choice([0, 1, 2])
state_space["C"] = random.choice([0, 1, 2])
state_space["D"] = random.choice([0, 1, 2])
state_space["E"] = random.choice([0, 1, 2])
state_space["F"] = random.choice([0, 1, 2])

start_loc = random.choice(["A", "B", "C", "D", "E", "F"])

while not goal:
    goal = goalTest(state_space, goal_state)
    if goal:
        break
    else:
        start_loc, state_space = get_percept(start_loc, state_space)

print("The agent is in goal state:")
print(state_space)