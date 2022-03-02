"""
author : connor chang
purpose :

containers for data related to the MealTracker project
implements classes: Food, Meal, Day, Log

Log = {
    "1970/01/01" : Day,
    "1970/01/02" : Day,
    ...
}

Day = {
    'Breakfast' : Meal,
    'Lunch' : Meal,
    ...
}

Meal = [
    Food,
    Food,
    ...
]

Food = Food :)

log.days['date'].meals['meal'].foods[0] refers to a food obj from top level

"""



from time import localtime
import pickle

# TIME STUFF TO MAKE THE EXPERIENCE OF LOG DAYS EASIER

def log_day(day_offset = 0):
    """ gets the current day from the time module, formats to YYYY/MM/DD (in order of stuff to sort by), where day_offset is the days +/- today """
    time = localtime()

    year = str(time.tm_year)
    month = str(time.tm_mon)
    day = str(time.tm_mday + day_offset)

    if len(month) == 1:
        month = "0"+month
    if len(day) == 1:
        day = "0"+day

    return f"{year}/{month}/{day}"



class Food():

    """ a class that defines a food item, and contains its basic info """

    # TODO: ADD new elements such as sugar
    # TODO: ADD functionality for ops on serving size as compared to amount consumed

    def __init__(self, food_name="n/a", food_serv=0, food_serv_unit="", food_cals=0, food_prot=0, food_fats=0, food_carbs=0):
        # could possibly streamline with use of **kwargs in future
        self.name = food_name
        self.serv = food_serv
        self.serv_unit = food_serv_unit
        self.cals = food_cals
        self.prot = food_prot
        self.fats = food_fats
        self.carbs = food_carbs

    # basic calculations from given stats
    def cals_from_prot(self):
        return self.prot * 4.1
    def cals_from_fats(self):
        return self.fats * 9.3
    def cals_from_carbs(self):
        return self.carbs * 4.1

    def __str__(self):
        # written out interpretation
        value = f"{self.name}: {self.cals}kcals, {self.prot}g protein, {self.fats}g fat, {self.carbs}g carbs"
        return value

    def __eq__(self, other):
        # == overload, if one food is exactly the same as another
        if self.name != other.name:
            return False
        elif self.serv != other.serv:
            return False
        elif self.serv_unit != other.serv_unit:
            return False
        elif self.cals != other.cals:
            return False
        elif self.prot != other.prot:
            return False
        elif self.fats != other.fats:
            return False
        elif self.carbs != other.carbs:
            return False
        return True

    # MUTATORS
    def set_name(self, val):
        if type(val) == str and len(val) > 0:
            self.name = val

    def set_serv(self, val, unit=""):
        if type(val) == int and val > 0:
            self.serv = val
        if type(unit) == str and len(unit) > 0:
            self.serv_unit = unit

    def set_cals(self, val):
        if type(val) == int and val > 0:
            self.cals = val

    def set_prot(self, val):
        if type(val) == int and val > 0:
            self.prot = val

    def set_fats(self, val):
        if type(val) == int and val > 0:
            self.fats = val

    def set_carbs(self, val):
        if type(val) == int and val > 0:
            self.carbs = val


class Meal():

    """ a class that contains all the Foods that were eaten at a given meal """

    # STANDARD STUFF

    def __init__(self, food_list = []):
        self.foods = food_list[:]

    def __str__(self):
        # written out interpretation
        value = ""

        # add all foods in self.foods
        for i in range(len(self.foods)):
            value += f"{i} :: {self.foods[i]}"

            if i != len(self.foods) - 1:
                # if not last entry, add a newline
                value += "\n"

        return value

    def __add__(self, other):
        # overload + in order to "add" meals, returning a new meal with the foods of both originals
        total_meals_list = []

        # add in the first meal's contents
        for food in self.foods:
            total_meals_list.append(food)

        # add in the second meals's contents
        for food in other.foods:
            total_meals_list.append(food)

        return Food(total_meals_list)

    def __eq__(self, other):
        # == overload to see if two meals are exactly the same
        return self.foods == other.foods

    # OTHER METHODS

    def add_food(self, food):
        # adds a Food
        self.foods.append(food)

    def total_cals(self):
        # returns how many calories were eaten in the meal
        cal_total = 0

        for i in range(len(self.foods)):
            cal_total += self.foods[i].cals

        return cal_total

    def total_prot(self):
        # returns how many protein was eaten in the meal
        prot_total = 0

        for i in range(len(self.foods)):
            prot_total += self.foods[i].prot

        return prot_total

    def total_fats(self):
        # returns how many fats were eaten in the meal
        fats_total = 0

        for i in range(len(self.foods)):
            fats_total += self.foods[i].fats

        return fats_total

    def total_carbs(self):
        # returns how many carbs were eaten in the meal
        carbs_total = 0

        for i in range(len(self.foods)):
            carbs_total += self.foods[i].carbs

        return carbs_total



class Day():

    """ a class that contains all the Meals that were eaten in a day """

    # STANDARD STUFF

    def __init__(self, meal_dict = {}):
        if len(meal_dict) == 0:
            breakfast = Meal()
            lunch = Meal()
            dinner = Meal()
            self.meals = {"Breakfast":breakfast, "Lunch":lunch, "Dinner":dinner}
        else:
            self.meals = meal_dict.copy()

    def __str__(self):
        # written out interpretation
        value = ""

        for key in self.meals.keys():
            value += f"{key}\n{'~'*20}\n{self.meals[key]}"

            if key != list(self.meals.keys())[-1]:
                # if not last entry, add a newline
                value += "\n"

        return value

    def __eq__(self, other):
        # == overload to see if two Days are the same
        return self.meals == other.meals # interestingly, this doesn't account for order

    # OTHER METHODS

    def add_meal(self, meal, meal_name = "Other"):
        # adds a Meal

        # figure out the meal's name
        if meal_name in self.meals.keys():
            # True when the name is not taken
            unique = False
            # i is the number tested at the end of the name
            i = 0

            while not unique:
                i += 1
                if meal_name + " " + str(i) not in self.meals.keys():
                    meal_name += " " + str(i)
                    unique = True

        # adds the given meal at the given meal name
        self.meals[meal_name] = meal

    def total_cals(self):
        # returns how many calories were eaten in the day
        cal_total = 0

        for key in self.meals.keys():
            cal_total += self.meals[key].total_cals()

        return cal_total

    def total_prot(self):
        # returns how many protein was eaten in the day
        prot_total = 0

        for key in self.meals.keys():
            prot_total += self.meals[key].total_prot()

        return prot_total

    def total_fats(self):
        # returns how many fats were eaten in the day
        fats_total = 0

        for key in self.meals.keys():
            fats_total += self.meals[key].total_fats()

        return fats_total

    def total_carbs(self):
        # returns how many carbs were eaten in the day
        carbs_total = 0

        for key in self.meals.keys():
            carbs_total += self.meals[key].total_carbs()

        return carbs_total



class Log():

    """ a class that contains all past days """

    # STANDARD STUFF

    def __init__(self, day_dict = {}):
        self.days = day_dict.copy()

    def __str__(self):
        # written representation; use at own risk, will be very long
        value = ""

        # just in case days are out of order
        sorted_keys = list(self.days.keys())
        sorted_keys.sort()

        for key in sorted_keys:
            value += f"{key}\n{'='*20}\n{self.days[key]}"

            if key != list(self.days.keys())[-1]:
                value += "\n"

        return value

    def __eq__(self, other):
        # == overload so we can see if two logs are the same
        return self.days == other.days

    # OTHER METHODS

    def add_day(self, day, date = log_day()):
        # add a day to self.days
        self.days[date] = day

    def save_data(self, filename):
        # save data til next session
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def load_data(self, filename):
        # load data from last session
        try:
            with open(filename, 'rb') as file:
                loaded = pickle.load(file)
                self.days = loaded.days
        except FileNotFoundError:
            self.save_data(filename) # if none exists, creates a new one
            self.load_data(filename)

########################################################################################
##       TODO: delete "main" section                                                  ##
########################################################################################
if __name__ == '__main__':
    food = Food("Lobstah Sauze", 100, "mL", 130, 5, 20, 15)

    meal = Meal()
    meal.add_food(food)
    meal.add_food(food)
    meal.add_food(food)

    day = Day()
    day.add_meal(meal, "Bkft")
    day.add_meal(meal, "Lnch")
    day.add_meal(meal, "Dnnr")
    day.add_meal(meal)

    log = Log()
    log.add_day(day, log_day(-1))
    log.add_day(day)

    print(log)
    print()

    print(day)
    print()

    print(meal)
    print()

    print(food)
    print()

    food = Food("Lol")

    print(day)
    print()

    print(f"Food cals : {day.meals['Bkft'].foods[0].cals}\nMeal cals : {day.meals['Bkft'].total_cals()}\nDay cals : {day.total_cals()}")
