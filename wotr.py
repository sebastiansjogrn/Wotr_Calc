from random import randint

# todo list: 
# add siege calculator for replacing elites to continue siege.
# add procent chance for all hit chances, from 1 to 5 for single round
# add first round only buffs, for fortification battles + cards
# relocate code within loops to outside loops where possible

# --- test armies --- #

# [normals, elites,rerolls,leader rolls]

# [regulars, elites, leadership,
# extra leader rolls (free people)/does elite give reroll(shadow)]
army1 = [3,5,3,0] 
army2 = [2,3,3,True] # note: these dont work rn


a = [7,1,5,0,0] # this works currently, for all

a1 = [3,2,5,3,0]
a2 = [10,0,4,0,0]

a3 = [1,0,1,0,0]
a4 = [5,0,3,0,0]
# --- Simulator functions --- #

#calculates average winrate of both sides
#given two armies commiting to N full battles
# b = -1 means siege (for a1, first input). 

def simbattleN (a1,b1,a2,b2,n,type):
  i = 0
  wprc1 = 0
  wprc2 = 0
  while i < n:
    a = simbattle(a1,b1,a2,b2,type)
    if a[0] == 1:
      wprc1 += 1
    elif a[0] == 2:
      wprc2 += 1   
    i += 1
  wprc1 = (wprc1 * 100) /  i
  wprc2 = (wprc2 * 100) /  i
  return (wprc1,wprc2,(100 - wprc1 - wprc2))

#simulates a full battle and returns 
# the winner and the remaining army
def simbattle (a1,b1,a2,b2,type):
  re1 = a1[2]
  re2 = a2[2]
  while dudes(a1,a2):
    if a1[4]:
      a1[2] = re1 + a1[1]
    if a2[4]:
      a2[2] = re2 + a2[1]
    a = simround(a1,b1,a2,b2,type)
    a1 = a[0]
    a2 = a[1]
  if dude(a1):
    return (1,a1,a2)
  elif dude(a2):  
    return (2,a1,a2)
  return (3,a1,a2)

#simulates one round of combat
def simround (a1, b1, a2, b2, type):
  hits1 = 0
  hits2 = 0 
  r1 = a1[0] + a1[1] + a1[3]
  r2 = a2[0] + a2[1] + a2[3]
  if r1 > 5:
    r1 = 5
  if r2 > 5:
    r2 = 5
  if type == 1:
    type = 0
    b2 -=1
    hits1 = rolldie(r1,a1[2],b1)
    hits2 = rolldie(r2,a2[2],b2)
    b2 += 1
  else :
    if type == 2 :
      b2 -= 1
    hits1 = rolldie(r1,a1[2],b1)
    hits2 = rolldie(r2,a2[2],b2)
  return [applyhits (a1,hits2), applyhits (a2,hits1), hits1, hits2]

def simhitsN(a,b,n):
  i = 0
  h = 0
  r1 = a[0] + a[1] + a[3]
  if r1 > 5:
    r1 = 5
  while i < n:
    h += rolldie(r1,a[2],b)
    i += 1
  return (h / i)

#simulates n rounds of combat given two armies, 
#returns the average amount of hits that each army produces
def simroundN(a1, b1, a2, b2, n, type):
  i = 0
  avgh1 = 0
  avgh2 = 0
  while i < n:
    a = simround (a1,b1,a2,b2, type)
    avgh1 += a[2]
    avgh2 += a[3]
    i += 1
  avgh1 = avgh1 /  i
  avgh2 = avgh2 /  i
  return (avgh1,avgh2)

# --- helper functions --- #

# rolls dies using rolls, rerolls and buffs 
# if b = -1 hits score on 6, b = 1 means hits score on 4 etc
# returns amount of hits produced
  
def rolldie(r,re,b):
  hits = 0
  hit = 5 - b
  while r:
    die = randint(1,6)
    if (die < hit) & (re > 0):
      die = randint(1,6)
      re -= 1
    if die >= hit:
      hits += 1
    r -= 1
  return hits

def rolldieN(r,re,b,n):
  i = 0
  h = 0
  while i < n:
    h += rolldie(r,re,b)
    i += 1
  return (h / i)

#applies hits on an army,
#If there are more than five units normals are killed first, 
#otherwise elites are killed to preserve maximum of rolls.

def applyhits (a,hits):
  while hits:
    if a[0] + a[1] > 5:
      if a[0] != 0:
        a[0] = a[0] - 1
      else:
        a[0] = a[0] + 1
        a[1] = a[1] - 1

    else:
      if a[1] != 0:
        a[0] = a[0] + 1
        a[1] = a[1] - 1
      else:
        a[0] = a[0] - 1

    if a[0] + a[1] == 0:
      a[2] = 0
      a[3] = 0
      return a
    hits -= 1
  return a

# checks if an army still has units
def dude(a):
  return ((a[0] != 0) | (a[1] != 0))

# checks if both armies still have units 
def dudes(a1, a2):
  return (dude(a1) & dude(a2))

# --- tests --- #

# test function for dudes
def testdudes():
  a = dudes([0,0],[0,0])
  b = dudes([1,0],[0,0])
  c = dudes([0,0],[1,0])
  d = dudes([1,1],[1,1])
  return (a == False) & (b == False) & (c == False) & d

def getArmies(verbose):
  if verbose:
    print("Welcome to the battle simulator")
    print("Please enter free peoples army:")
    print("Free people army looks like this: regulars, elites,",
    "leadership, leader rolls, does elite give leadership(1/0)")

    a1 = list(map(int,input().split(",")))
  if verbose:
    print("Please enter shadow army:")
    print("Shadown army looks like this: regulars, elites,",
    "leadership, leader rolls, does elite give leadership(1/0)")
  a2 = list(map(int,input().split(",")))
  return a1,a2

def getType(verbose):
  if verbose:
    print("Please enter type of combat:")
    print("2 = siege battle")
    print("1 = fortification battle")
    print("0 = field battle")
  return int(input())


def huntsim(eyes,moves):
  pool = 16
  rev = 9
  eye = 4
  zeroes = 2
  ones = 4
  twos = 3
  threes = 3
  hits = pool - zeroes
  for i in range(moves):
    hits = rolldie(eye,0,i-1)
    if hits > 0:
      chance = zeroes / pool
      zeroes = zeroes - 1
      pool = pool - 1



if __name__ == "__main__":
  verbose = True
  a1,a2 = getArmies(verbose)
  print(a1)
  print(a2)
  battleType = getType(verbose)
  print("The average hits for each army is: \n") 
  print(simroundN(a1,0,a2,0,2,battleType))
  print("\n Battle results are:")
  print(simbattle(a1,0,a2,0,battleType))
