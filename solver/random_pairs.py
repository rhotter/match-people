import random
names = ["Raffi", "Santi", "Marley", "Erin", "Albert", "Brandon", "Osher", "Sasha", "Simon", "Wilfred", "Liz", "Dylan", "Anna", "Sophie"]
random.shuffle(names)
for i in range(len(names)//2):
  print(f'{names[2*i]} + {names[2*i+1]}')