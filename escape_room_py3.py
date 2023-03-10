from sys import exit
from time import sleep


class Office(object):

    def begin(self):
        print("Hello, you're playing Escape Room.")
        print("You're trapped in an Office.")
        print("Look for clues and tools to make your way out.")
        print("Type 'help' to find out how to play the game.")

    def help(self):
        print("Use the following commands to make your way out.")
        print("""
-->type 'look' followed by a direction such as 'up', 'down', 'left', 
    'right', 'forward'
-->type 'inspect' followed by an object in the room to inspect it.
    For eg: inspect door
-->type 'inventory' to check the items you have in your inventory.
-->type 'use' followed by an item in your inventory and specify which
     object in the room you want to use it on. For eg: use key on door.
""")


safe_state = True
circuit_breaker_state = True
vent_state = True
trapdoor_state = True
photo_state = 0
drawer_state = True
inventory = []


class Forward(Office):

    def intro(self):
        print("You look ahead and see a green door.")
        print("It is locked")

    def access_door(self):
        print("The door is locked. Look for a key to open it.")

    def use_door(self, thing1):
        if thing1 == 'key':
            print("You used the key on the door.")
            print("With trembling hands you manage to")
            print("open the lock.\n\tCongratulations! You've Escaped!")
            print("Exiting in:")
            flag = True
            while flag:
                for i in range(5, -1, -1):
                    print("\r%s" % str(i), end=' ')
                    sleep(1)
                flag = False
            exit(0)
        else:
            print("You were not able to use a %s on the door" % thing1)


class Up(Office):

    def intro(self):
        if vent_state:
            print("You look up and see a blue vent.")
            print("It is screwed to the ceiling")
        else:
            print("You look up and see the blue vent")
            print("you unscrewed.")

    def access_vent(self):
        if vent_state:
            print("The vent is screwed to the ceiling.")
        else:
            print("You have already opened the vent.")

    def use_vent(self, thing1):
        global vent_state
        global inventory
        if vent_state and thing1 == 'screwdriver':
            print("You used the screwdriver on the vent.")
            print("The vent opens and you find a hammer inside.")
            print("You pick it up.")
            inventory.append('hammer')
            vent_state = False
        elif thing1 != 'screwdriver':
            print("You were not able to use a %s on the vent." % thing1)
        else:
            self.access_vent()


class Right(Office):

    def intro(self):
        global safe_state
        global circuit_breaker_state
        if circuit_breaker_state:
            print("You look right and see a safe. Right above")
            print("it is a circuit breaker on the wall.")
        else:
            if not safe_state:
                print("You look right and see the safe you had opened.")
                print("Above it lies the circuit breaker you fixed.")
            elif not circuit_breaker_state:
                print("You look to the right and see a safe. Right")
                print("above lies the circuit breaker you fixed.")

    def access_safe(self):
        global safe_state
        global inventory
        code = '0390'
        if safe_state:
            print("The safe has a four digit code. Enter the code")
            print("to open the safe.")
            user_permission = input("Do you want to try?(y/n)\n> ")
            if user_permission == 'y':
                while True:
                    enter_code = input("[code]> ")
                    if enter_code == code:
                        print("The safe beeps and opens up.")
                        print("You find some files, a gun and a key")
                        print("You take the key and leave the rest")
                        inventory.append('key')
                        safe_state = False
                        break
                    else:
                        print("Bzzztt..")
                        print("The code you entered was wrong")
                        self.access_safe()
                        break
            else:
                pass
        else:
            self.intro()

    def access_circuit_breaker(self):
        global circuit_breaker_state
        if circuit_breaker_state:
            print("You look to the right and see a circuit breaker.")
            print("It's switches are out of place. There's a Red, Blue,")
            print("Green and White switch.")
            try_order = input("Would you like to try fixing it?(y/n)\n> ")
            if try_order == 'y':
                print("What order would you like to place the switches in?\n" \
                      "eg: RBGW")
                self.circuit_breaker_code()
            elif try_order == 'n':
                print("Okay")
                pass
            else:
                print("That was not a valid option. Going back.")
                pass
        else:
            print("The circuit breaker is fixed and running")

    def circuit_breaker_code(self):
        global circuit_breaker_state
        right_order = 'GRBW'
        order = input('[order]> ')
        if order == right_order:
            print("GRRRGRRR")
            print("The circuit is completed. You hear a sound")
            print("from underneath the rug.")
            circuit_breaker_state = False
        else:
            print("Nothing happened. That was the wrong order.")
            while True:
                try_again = input("Would you like to try again?(y/n)\n> ")
                if try_again.lower() == 'y':
                    self.access_circuit_breaker()
                    break
                elif try_again.lower() == 'n':
                    break  # TODO might be bad ending
                else:
                    print("That is an invalid response.")


class Down(Office):

    def intro(self):
        print("You look down and see a red oriental rug.")

    def access_rug(self):
        global trapdoor_state
        global circuit_breaker_state
        if circuit_breaker_state:
            print("You look under the rug and see a trapdoor. There is a")
            print("switch beside it but it seems the power is off.")
        else:
            if trapdoor_state:
                print("You look under the rug and see the trapdoor. Now that")
                print("you've fixed the circuit breaker, you press the switch")
                print("beside it and the trapdoor opens up.")
                print("There you find a crowbar.")
                inventory.append('crowbar')
                trapdoor_state = False
            else:
                print("You look under the rug. You have already opened the")
                print("trapdoor underneath")

    def access_trapdoor(self):
        self.access_rug()


class Left(Office):

    def intro(self):
        print("You look to your left and see a desk.")
        print("Beside the desk is a white trashcan.")

    def access_desk(self):
        print("On the desk lies a photo and a letter.")
        print("There is a drawer, but it is jammed.")

    def access_photo(self):
        global photo_state
        if photo_state == 0:
            print("There is a photo of a father celebrating his")
            print("daughter's 5th birthday behind the thick glass panel.")
        elif photo_state == 1:
            print("You break the glass panel with the hammer.")
            print("You look behind the photo and it has a date.")
            print("'March 1995'")
            photo_state = 2
        else:
            print("The photo is of a father celebrating his daughter's")
            print("5th birthday.")
            print("You look behind the photo and it has a date.")
            print("'March 1995'")

    def use_photo(self, thing1):
        global photo_state
        if thing1 == 'hammer':
            photo_state = 1
            self.access_photo()
        else:
            print("You were not able to use a %s on the photo" % thing1)

    def access_drawer(self):
        global drawer_state
        if drawer_state:
            print("The drawer is locked. Probably a bit of force might open it.")
        else:
            print("You had broken open the drawer.")

    def use_drawer(self, thing1):
        global drawer_state
        global inventory
        if drawer_state and thing1 == 'crowbar':
            print("You break open the drawer with the crowbar.")
            print("Inside it you find a screwdriver.")
            inventory.append('screwdriver')
            drawer_state = False
        elif thing1 != 'crowbar':
            print("You weren't able to use a %s on the drawer." % thing1)
        else:
            self.access_drawer()
            # TODO add screwdriver to inventory
            # TODO link with Actions.use()

    def access_trashcan(self):
        print("You look inside the trashcan. It is empty.")

    def access_letter(self):
        print("You read the handwritten letter on the desk:")
        print("\tDear Secretary,")
        print("\tThe moment you walked through the door, I knew")
        print("\tyou were the one for me. You swept me off my feet")
        print("\tthe moment our eyes first met. I hate to vent all")
        print("\tall my feelings to you in a letter, but this had")
        print("\tto be said. I hope you have the heart not to throw")
        print("\tthis letter in the trash, like the last four I sent.")
        print("\t\tSincerely,")
        print("\t\tYour Boss.")


class Actions(object):

    def __init__(self):
        self.up = Up()
        self.down = Down()
        self.left = Left()
        self.right = Right()
        self.forward = Forward()
        self.objects = {
            'door': self.forward, 'circuit breaker': self.right,
            'safe': self.right, 'rug': self.down, 'trapdoor': self.down,
            'desk': self.left, 'photo': self.left, 'trashcan': self.left,
            'letter': self.left, 'drawer': self.left, 'vent': self.up
        }

    def look(self, direction):
        directions = {
            'up': self.up, 'down': self.down, 'left': self.left,
            'right': self.right, 'forward': self.forward
        }

        if direction in list(directions.keys()):
            view = directions[direction]
            view.intro()
        else:
            print("That's not a valid direction to look at.")
            print("You can look 'up', 'down', 'left', 'right'")
            print("or 'forward'")

    def inspect(self, thing):
        if thing in list(self.objects.keys()):
            return getattr(self.objects[thing], 'access_' + thing.replace(' ', '_'))()
        else:
            print("Something went wrong.")

    def check_inventory(self):
        global inventory
        if len(inventory) > 0:
            print("You have the following items in your inventory:")
            print(', '.join(inventory))
        else:
            print("You have nothing in your inventory")

    def use(self, thing1, thing2):
        global inventory
        if thing1 in inventory:
            if thing2 in list(self.objects.keys()):
                try:
                    return getattr(self.objects[thing2], 'use_' + thing2.replace(' ', '_'))(thing1)
                except AttributeError:
                    print("You were not able to use %s on %s" % (thing1, thing2))
            else:
                print("There is no %s in the room" % thing2)
        else:
            print("You do not have a %s in your inventory" % thing1)


class Engine(object):

    def __init__(self, room):
        self.room = room
        self.action = Actions()

    def play(self):
        self.room.begin()
        while True:
            user = input("What would you like to do?\n> ")
            input_list = user.strip().split(' ')
            try:
                if user.startswith('look'):
                    self.action.look(input_list[1])
                if user.startswith('inspect'):
                    if len(input_list) < 2:
                        raise IndexError
                    else:
                        self.action.inspect(' '.join(str(x) for x in input_list[1:]))
                if user.startswith('use'):
                    if len(input_list) >= 4:
                        self.action.use(input_list[1], ' '.join(input_list[3:]))
                    else:
                        raise IndexError
                if user.startswith('inventory'):
                    self.action.check_inventory()
                if user.startswith('help'):
                    self.room.help()

            except IndexError:
                if user.startswith('look'):
                    print("Please specify a direction to look at.")
                if user.startswith('inspect'):
                    print("Please specify an object to inspect.")
                if user.startswith('use'):
                    print("Please specify an object to use %s on" % ' '.join(input_list[1:]))


office = Office()
start = Engine(office)
start.play()
