from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

coffee_menu = Menu()
coffee_machine = CoffeeMaker()
money_machine = MoneyMachine()

machine_off = False

while not machine_off:
    order = input(f"What would you like? ({coffee_menu.get_items()}): ")
    if order == "off":
        machine_off = True
    elif order == "report":
        coffee_machine.report()
        money_machine.report()
    else:
        drink_item = coffee_menu.find_drink(order)
        if coffee_machine.is_resource_sufficient(drink_item) and money_machine.make_payment(drink_item.cost):
            coffee_machine.make_coffee(drink_item)

