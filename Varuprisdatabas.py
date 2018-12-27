
#Databas som uppdateras kontinuerligt när man matar in data
class Grocery:

    def __init__(self, name, code, quantity, price):
        self.name = name
        self.code = code
        self.current_quantity = quantity
        self.starting_quantity = quantity
        self.price = price

    def get_name(self):
        return self.name

    def get_code(self):
        return self.code

    def get_current_quantity(self):
        return self.current_quantity

    def get_price(self):
        return self.price

    def get_starting_quantity(self):
        return self.starting_quantity

    #Funktion som ändrar kvantiteten i lagret, och ser till att lagret inte
    #blir större än start-antalet.
    def change_quantity(self, change):
        if self.current_quantity - change >= 0:
            if self.current_quantity - change > self.starting_quantity:
                self.current_quantity = self.starting_quantity
            else:
                self.current_quantity -= change
        else:
            self.current_quantity = 0

    def is_in_store(self, my_quantity):
        if int(my_quantity) <= int(self.current_quantity):
            return True
        return False


#Funktion som läser in fil
def open_file():
    read_file = open('varulager.txt', 'r')
    read_file = read_file.readlines()
    return read_file


#Funktion som behandlar filen
def create_starting_groceries(read_file):
    starting_groceries_lines = []
    for i in read_file:
        starting_groceries_lines.append(i.replace("\n",''))
    starting_groceries = []
    for i in starting_groceries_lines:
        starting_groceries.append(i.split(' '))
    return starting_groceries

#Funktion som skapar instanser av varor och returnerar lista av dessa
def create_groceries(starting_groceries):
    current_groceries = []
    for grocery in starting_groceries:
        my_name = grocery[0]
        my_code = grocery[1]
        my_quantity = grocery[2]
        my_price = grocery[3]
        my_grocery = Grocery(my_name, int(my_code), int(my_quantity), float(my_price))
        current_groceries.append(my_grocery)
    return current_groceries


#Funktion som skapar kvitto
def receipt(current_groceries):
    print("Grocery\t      Quantity   A-price   Sum")
    print("______________________________________")
    total_price = 0
    total_quantity = 0
    for grocery in current_groceries:
        amount_wanted = grocery.get_starting_quantity() - \
                        grocery.get_current_quantity()
        grocery_sum = amount_wanted * grocery.get_price()
        if amount_wanted:
            total_price += grocery_sum
            total_quantity += amount_wanted
            print("{} \t\t  {} \t  {} \t  {}".format(grocery.get_name(),
            str(amount_wanted), str(grocery.get_price()), str(grocery_sum)))

    print("______________________________________")
    print("Total \t\t  {} \t\t  {}".format(str(total_quantity),
    str(total_price)))

def introduction_program():
    print("\n \n")
    print("145 Varuprisdatabas \n")
    print("1. Write a valid grocery code and requested quantity seperated by a blank space.")
    print("2. If you want to remove groceries, write a minus sign before the quantity you would like to remove.")
    print("3. To write out receipt and quit this program, write a hashtag. \n")
    print("This is an example: \n")
    print("100 2")

def safe_int(input):
    try:
        return int(input)
    except:
        print("Did not understand {}, try again".format(input))
        return False

def pick_groceries(current_groceries):
    #Behandlar inmatning och hanterar om användare matar in "fel"
    while True:
        user_input = input('>  ')
        user_input_splitted = user_input.split(' ')
        my_code = None
        my_quantity = None

        if user_input == '#':
            receipt(current_groceries)
            break

        if not user_input_splitted[0].isdigit():
            print("Please only write digits")
        else:
            my_code = safe_int(user_input_splitted[0])

        if len(user_input_splitted) == 1:
                my_quantity = 1
        elif len(user_input_splitted) >= 2:
            if not user_input_splitted[1].strip("-").isdigit():
                print("Please only write digits")
            else:
                my_quantity = safe_int(user_input_splitted[1])

        grocery_exists = False
        for grocery in current_groceries:
            if my_code == grocery.get_code():
                grocery_exists = True
                if my_quantity:
                    if grocery.is_in_store(my_quantity):
                        grocery.change_quantity(my_quantity)
                    else:
                        print("We only have {} in store".format(grocery.get_current_quantity()))

        if not grocery_exists:
            print("Please write a valid code.")


def main():
    read_file = open_file()
    starting_groceries = create_starting_groceries(read_file)
    current_groceries = create_groceries(starting_groceries)
    introduction_program()
    pick_groceries(current_groceries)

main()
