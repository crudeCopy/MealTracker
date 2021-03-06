""" a command line implementation """

from classes import *
from search import *
from os import system
import platform



### CMD-ONLY methods ###

def scr(day):
    """ clear screen, adjusts for platform """
    if platform.system() == 'Windows':
        cmd = 'cls'
    else:
        cmd = 'clear' # most other than windows use clear as far as i know
    system(cmd)

    open_msg = "*"*40 + "\n*" + " "*38 + "*\n*  MealTracker  //  Connor Chang, '22  *\n*" + " "*38 + "*\n" + "*"*40 + "\n\n"
    print(open_msg)
    print(today)
    print()

def get_search():
    """ let the user search for and select a food item """
    result = search_fc(input("query: "))

    # display the results to the user
    for i in range(len(result)):
        print(f"{i}: {result[i]['description']}", end=" ")
        if 'brandName' in result[i].keys():
            print(f"by {result[i]['brandName']}", end=" ")
        print()

    # prompt the user to choose one result
    which = int(input("Which of these options: "))

    # bind results to a new Food instance (now with extensive error handling)
    new_food = Food()

    ## name
    new_food.map_from_search(result[which])

    # return chosen result
    return new_food


def get_manual():
    """ let the user manually enter a food item """
    vals = {}

    new_food = Food()

    print("Enter the following values accordingly, enter nothing if applicable:")
    new_food.set_name(input("name: "))
    new_food.set_serv(int(input("serving size: ")), input("serving unit: "))
    new_food.set_cals(int(input("calories (kcal): ")))
    new_food.set_prot(int(input("protein (g): ")))
    new_food.set_fats(int(input("fat (g): ")))
    new_food.set_carbs(int(input("carbohydrates (g): ")))

    # return constructed result
    return new_food




### MAIN section ###

if __name__ == '__main__':

    # access stored log
    log = Log()
    log.load_data('log.dat')

    if log_day() in log.days.keys():
        today = log.days[log_day()]
    else:
        today = Day()

    # opening message
    scr(today)

    # main loop :)
    prompt = "What would you like to do?\n" + "="*30 + "\n[d]isplay\nadd by [s]earch\nadd [m]anually\n[r]emove\n[q]uit\n\n"
    keep_going = ""

    while keep_going != "q":
        scr(today)
        keep_going = input(prompt)

        if keep_going == "d":
            #display all the food you eated

            print(today)
        elif keep_going == "s":
            #something involving searching
            scr(today)
            add_to_meal = input("Which meal? " + str(list(today.meals.keys())) + "\n")
            today.meals[add_to_meal].foods.append(get_search())
        elif keep_going == "m":
            #add food manually
            scr(today)
            add_to_meal = input("Which meal? " + str(list(today.meals.keys())) + "\n")
            today.meals[add_to_meal].foods.append(get_manual())
        elif keep_going == "r":
            #remove a preexisting Food
            scr(today)
            removal_meal = input("Which meal? " + str(list(today.meals.keys())) + "\n")
            if len(today.meals[removal_meal].foods) > 0:
                removal_index = int(input(f"Which to remove? [0 - {len(today.meals[removal_meal].foods) - 1}]\n"))
                today.meals[removal_meal].foods.pop(removal_index)
            else:
                print("nothing to remove from this meal")
        elif keep_going == "q":
            print("Goodbye!")
        else:
            print("Invalid input")

    log.add_day(today)
    log.save_data('log.dat')
