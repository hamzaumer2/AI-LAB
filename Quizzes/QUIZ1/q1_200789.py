# HAMZA UMER FAROOQ - 200789
# BSCS 6 B
# AI LAB QUIZ 1
# QUESTION 1


import math

x = int(input("Enter How many numbers you want to perform oprations on: "))
y = 0
for i in range(0, x):
    y = int(input("Enter a number: "))
    z = input("Enter Operator: (+,-,*,/): ")
    if z == "+":
        x = x + y
    elif z == "-":
        x = x - y
    elif z == "*":
        x = x * y
    elif z == "/":
        x = x / y
    else:
        print ("Invalid Operator")

print ("Result: ", x)