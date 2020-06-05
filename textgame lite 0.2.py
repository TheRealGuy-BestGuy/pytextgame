import random
import cmd
import textwrap
import sys
import time

#Character class

class character:
    def __init__(self, name, health, location,inventory):
        self.name = name
        self.health = health
        self.location = location
        self.inventory = []
playername = 'placeholder'
#player character
player = character(playername,10,0,[])

#enemies class
class enemy:
    def __init__(self,name,health,damage,hitchance):
        self.name = name
        self.health = health
        self.damage = damage
        self.hitchance = hitchance

#enemies
goblin = enemy('goblin',3,1,30)

#weapons class
class weapon:
    def __init__(self,name,damage,description,hitchance):
        self.name = name
        self.damage = damage
        self.description = description
        self.hitchance = hitchance

#simple string list of weapons for combat check
weaponlist = ['sword']
#weapon stats and descriptions
sword = weapon('sword',5,'A well balanced, sharp sword. You feel confident with this in your hand.',75)

#items
##__LIST OF ROOMS__##
rooms = [
    {'name':'clearing','description':'you find yourself in a forest clearing. you are surrounded by dense forest apart from a single exit to the north.','inspect':'there does not seem to be anything more of interest here','directions':['north','North','n','N'],'north':1,'action':'none','enemies':[],'roominv':[]},
    #0
    {'name':'Twisty Path','description': 'This path winds through the woods, you get an uneasy feeling here.','inspect': 'the path is dark and confusing, but you manage to see the path continues north. You also notice a large pile of leaves and brush along the path.','directions':['north','North','south','South'],'north':2,'south':0,'action':'move brush','roominv':[],'enemies':[goblin]}
]

#defining mechanics
#room specific actions
def roomaction(action):
    if action == 'move brush':
        rooms[player.location]['roominv'].append(sword)
        print('You move aside the brush to reveal an old sword, forgotten to time.')
        rooms[1]['inspect']='the path is dark and confusing, but you manage to see the path continues north. you have moved the pile of brush'
        rooms[1]['action']='noaction'
    elif action == 'noaction':
        print('that is not an actual action.')
    else:
        print("idk how you got here but the code dun messed up")
def combat(combatenemy,playerweapon):
    roll = random.randint(1,100)
    if roll <= playerweapon.hitchance:
        combatenemy.health -= playerweapon.damage
    else:
        print('you failed to hit the ',(combatenemy.name),'.')
    if combatenemy.health > 0:
        enemyroll = random.randint(1,100)
        if enemyroll <= combatenemy.hitchance:
            player.health -= combatenemy.damage
            print('you were struck by the ',(combatenemy.name),' dealing ',str(combatenemy.damage),'damage')
            print('your health is now ',str(player.health))
        else:
            print('the',(combatenemy.name),'swung and failed to strike you')
    elif combatenemy.health <= 0:
        print('you have defeated the ',(combatenemy.name),'.')
        rooms[player.location]['enemies'] = []
    


##__the actual game__##
print('#rules and commands:')
print('traveling is done by typing the direction')
print('the keyword for picking things up is take')
print('combat must be done in 3 arguments eg: attack with sword')
print('item names are all lowercase')
print('other commands: inventory, look,')
print('have fun!')
print()
print()
print()
playername = str(input('what is your name?  > ')) #gets name for player upton startup

command = '  '
while command != 'exit game':
    activeroom = rooms[player.location]
    print(rooms[player.location]['description'])
    if len(activeroom['enemies']) > 0:
        print('You see a',(activeroom['enemies'][0].name),'lurking around')
    if len(activeroom['roominv']) > 0:
        checkeditems = 0
        while checkeditems < len(activeroom['roominv']):
            print('You see a',activeroom['roominv'][checkeditems].name,'on the floor')
            checkeditems += 1
    command = str(input('what do you do?  > '))

    if command in activeroom['directions']:
        if 'north' or 'North' or 'n' or 'N' in command:
            player.location = activeroom['north']
        elif 'south' or 'South' or "S" or 's' in command:
            player.location = activeroom['south']
    elif 'look' in command:
        print(activeroom['inspect'])
    elif 'take' in command:
        if len(activeroom['roominv']) > 0:
            pickedup = 0
            while pickedup < len(activeroom['roominv']):
                print('You picked up',activeroom['roominv'][pickedup].name)
                player.inventory.append(activeroom['roominv'][pickedup])
                pickedup += 1
            activeroom['roominv'] = []
    elif activeroom['action'] in command:
        roomaction(activeroom['action'])
    elif 'inventory' in command:
        print('your inventory contains')
        invcheck = 0
        if invcheck < len(player.inventory):
            while invcheck < len(player.inventory):
                print(player.inventory[invcheck].name)
                invcheck += 1
        print('and a few crumbs.')
    elif 'eat' and 'crumbs' in command:
        print('You pick at the crumbs in the bottom of your bag, but mostly you just hair and lint.')
        print('Your stomach rumbles')
    elif 'attack' in command:
        if len(player.inventory) > 0:
            invcheck = 0
            while invcheck < len(player.inventory):
                if str(command.split()[2]) == player.inventory[invcheck].name:
                    if command.split()[2] in weaponlist:
                        combat(activeroom['enemies'][0],player.inventory[invcheck])
                invcheck += 1

        
