# 🚨 Don't change the code below 👇
print("Welcome to the Love Calculator!")
name1 = input("What is your name? \n")
name2 = input("What is their name? \n")
# 🚨 Don't change the code above 👆

#Write your code below this line 👇
lower_name1 = name1.lower()
lower_name2 = name2.lower()
t = lower_name1.count("t")
r = lower_name1.count("r")
u = lower_name1.count("u")
e = lower_name1.count("e")
T = lower_name2.count("t")
R = lower_name2.count("r")
U = lower_name2.count("u")
E = lower_name2.count("e")
TRUE = t + r + u + e + T + R + U + E

l = lower_name1.count("l")
o = lower_name1.count("o")
v = lower_name1.count("v")
e = lower_name1.count("e")
L = lower_name2.count("l")
O = lower_name2.count("o")
V = lower_name2.count("v")
E = lower_name2.count("e")
LOVE = l + o + v + e + L + O + V + E
TRUE = str(TRUE)
LOVE = str(LOVE)
score = TRUE + LOVE
print(score)
score = int(score)
if score < 10 or score > 90:
  print(f"Your score is {score}, you go together like coke and mentos.")
elif score > 40 and score < 50:
  print(f"Your score is {score}, you are alright together")
else:
  print(f"Your score is {score}")





