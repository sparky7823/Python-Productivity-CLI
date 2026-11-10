def check_date(date):
    """
    Validates MM/DD date strings against standard calendar constraints, handling
    type conversion and out-of-bounds errors.
    """
    if not date:
        return False
    date_split = date.split('/')
    if len(date_split) == 2:
        month, day = date_split
        if len(month) == 2 and len(day) == 2:
            try:
                int(month)
                int(day)
            except (ValueError, TypeError):
                print('Wrong format: must be integers')
                return False
            if 0 < int(month) <= 12 and 0 < int(day) <= 31:
                return True
            else:
                print('Out of bounds')
                return False
    print('Wrong format')
    return False

# Sleep Tracker
# region
def log_hours(filename):
    """
    Appends sleep metrics to a persistent CSV.
    Parses existing records to insert new entries chronologically
    and handles state overwrites for duplicate dates.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    day = False
    while not check_date(day):
        day = input('Day in format MM/DD: ')
    hours = input('Hours sleep: ')

    new_string = f'{day}, {hours}\n'
    for line, i in zip(lines[1:], range(len(lines[1:]))):
        line_date = line.strip().split(',')[0]
        if line_date < day:
            lines.insert(i + 1, new_string)
            break
        elif line_date == day:
            if input('Do you want to overwrite this day? y or n: ') == 'y':
                lines[i + 1] = new_string
            break
        if i == len(lines[1:]):
            lines.append(new_string)

    with open(filename, 'w') as file:
        file.writelines(lines)

    print('Sleep logged ✔')


def avg_w_timeframe(lines, days):
    """
    Calculates rolling averages of sleep metrics over a dynamically defined
    chronological window.
    """
    total = 0
    for line, i in zip(lines, range(days)):
        words = line.split(',')
        total += float(words[1].strip())
    return total / days


def sleep_summary(filename):
    """
    CLI router and validation handlers for the Sleep Tracker module.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]
        print("Options: a) This week's average b) All time average c) Another time frame")
        tag = 'z'
        while not 'a' <= tag <= 'c':
            tag = input('~ ')
        if tag == 'a':
            avg = avg_w_timeframe(lines, 7)
            print(f"This week's average: {avg:.1f} hrs")
        if tag == 'b':
            avg = avg_w_timeframe(lines, len(lines))
            print(f'All time average: {avg:.1f} hrs')
        if tag == 'c':
            num_days = int(input("Number of days: "))
            avg = avg_w_timeframe(lines, num_days)
            print(f'Average of the last {num_days} days: {avg:.1f} hrs')


def sleep_tracker():
    """
    CLI router and validation handlers for the Sleep Tracker module.
    """
    filename = 'sleep_tracker.csv'
    print("Options: a) Log hours b) Get summary")
    tag = 'z'
    while not 'a' <= tag <= 'b':
        tag = input('~ ')
    if tag == 'a':
        log_hours(filename)
    if tag == 'b':
        sleep_summary(filename)

# endregion


# Menu planner
# region
def print_plan(menu_plan, filename):
    """
    Formats and outputs the weekly menu plan by executing a relational lookup
    between planned meals and their associated ingredient lists.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        recipes = {}
        for line in lines:
            line = line.split(', ')
            recipes[line[0]] = line[1:]

        print()
        print("This week's grocery list:")
        for item in menu_plan:
            plan = menu_plan[item]
            print(f'{item}: {menu_plan[item].lower()}       {[item.strip() for item in recipes[plan]]}')


def make_menu_plan(filename):
    """
    Facilitates weekly meal planning. Validates user input against the existing recipe
    database and dynamically routes to creation workflows for unrecognized entries.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        recipes = [(line.split(', '))[0] for line in lines]
        menu_plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            while True:
                plan = input(f'Recipe planned for {day}: ')
                if plan.upper() in recipes:
                    break
                else:
                    print(f'{plan} not in recipe list.')
                    if input('Do you want to add it? y or n: ') == 'y':
                        add_recipe(filename)
                        recipes.append(plan.upper())
            menu_plan[day] = plan.upper()
            print(f'{plan} planned for {day}')
        print_plan(menu_plan, filename)


def add_recipe(filename):
    """
    Captures new recipe names and ingredient arrays, serializing and
    appending the formatted data to the persistent CSV database.
    """
    name = input('Recipe name: ')
    ingredients = []
    new = True
    while not new == '':
        new = input('Enter an ingredient: ')
        ingredients.append(new)
    new_ingredients = ', '.join(ingredients).strip(', ')
    new_recipe = f'{name.upper()}, {new_ingredients}\n'
    with open(filename, 'a') as file:
        file.write(new_recipe)
    print('Recipe added ✔')


def menu_planner():
    """
    CLI router for the Menu Planner module.
    """
    filename = 'recipes.csv'
    print("Options:  a) Make menu plan  b) Add recipe")
    tag = 'z'
    while not 'a' <= tag <= 'b':
        tag = input('~ ')
    if tag == 'a':
        make_menu_plan(filename)
    if tag == 'b':
        add_recipe(filename)
    if tag == 'c':
        pass
#endregion


# To-do List
# region
def view_todos(filename):
    """
    Deserializes the to-do list CSV and applies sorting algorithms to display tasks
    ordered either by integer priority rank or estimated completion time.
    """
    current = load_current(filename)
    print("View by: a) Priority level  b) Time estimate")
    tag = 'z'
    while not 'a' <= tag <= 'b':
        tag = input('~ ')
    if tag == 'a':
        one = []
        two = []
        three = []
        for key in current:
            if current[key][0] == '1':
                one.append(key)
            elif current[key][0] == '2':
                two.append(key)
            elif current[key][0] == '3':
                three.append(key)
        print(f'Level 1: {', '.join(one)}')
        print(f'Level 2: {', '.join(two)}')
        print(f'Level 3: {', '.join(three)}')
    if tag == 'b':
        ordered = []
        for key in current: # Cook
            line = [key, current[key][0], current[key][1]]
            if not ordered:
                ordered.append(line)
            else:
                for i in range(len(ordered)):
                    check1 = int(ordered[i][2])
                    check2 = int(line[2])
                    if check1 > check2:
                        ordered.insert(i, line)
                        break
                    if i == len(ordered) - 1:
                        ordered.append(line)
        for item in ordered:
            print(f'{item[0]}: {item[2]} minutes')


def add_todos(filename):
    """
    Captures new tasks, priority levels, and time estimates.
    Validates against duplicate keys before appending to the persistent CSV.
    """
    current = load_current(filename)
    with open(filename, 'a') as file:
        while True:
            new = input("New item: ")
            if new == '':
                break
            elif new in current.keys():
                print('This item already exists')
            else:
                rank = input("Priority level 1-3: ")
                time = input("Time estimate (in minutes): ")
                new_line = f'{new}, {rank}, {time}\n'
                current[new] = [rank, time]
                file.write(f'{new_line}')


def check_off(filename):
    """
    Executes Delete operations (CRUD) for completed tasks.
    Removes the target key from the active dictionary state and
    overwrites the CSV to maintain persistence.
    """
    current = load_current(filename)
    c_pretty = [key for key in current]
    with open(filename, 'w') as file:
        while True:
            print(c_pretty)
            done = input('Completed task: ')
            if done == '':
                break
            elif done not in c_pretty:
                print('This item does not exist')
            else:
                del current[done]
                c_pretty.remove(done)

        updated = []
        for item in current:
            new_line = f'{item}, {current[item][0]}, {current[item][1]}\n'
            updated.append(new_line)
        file.writelines(updated)


def load_current(filename):
    """
    Deserializes a structured CSV file into a nested Python dictionary
    for rapid memory access and state management.
    """
    current = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            items = line.split(', ')
            time = items[2].strip()
            current[items[0]] = [items[1], time]
    return current


def todos():
    """
    CLI router for the To-Do List module.
    Handles user navigation for viewing, appending, and deleting tasks.
    """
    filename = 'to_dos.csv'
    print("Options: a) View  b) Add items  c) Check off items")
    tag = 'z'
    while not 'a' <= tag <= 'c':
        tag = input('~ ')
    if tag == 'a':
        view_todos(filename)
    if tag == 'b':
        add_todos(filename)
    if tag == 'c':
        check_off(filename)
# endregion


# Scheduler
# region
def scheduler_helper(slot, to_do):
    """
    A recursive constraint-optimization algorithm.
    Evaluates the task dictionary against a defined time constraint
    to identify and return the optimal combination of tasks based on
    duration and priority limits.
    """
    choice = ''
    choice_time = 0
    for item in to_do:
        time = to_do[item][1]
        if int(time) <= slot:
            if choice_time == 0:
                choice = item
                choice_time = time
            elif int(time) == int(choice_time):
                if to_do[item][0] < to_do[choice][0]:
                    choice = item
                    choice_time = time
            elif int(time) > int(choice_time):
                choice = item
                choice_time = time
    extra = None
    if choice_time == 0:
        return False, None
    elif int(choice_time) < slot:
        new_slot = slot - int(choice_time)
        new_to_do = to_do
        del new_to_do[choice]
        extra = scheduler_helper(new_slot, new_to_do)
    return choice, extra


def scheduler():
    """
    CLI routers initializing the application loop and handling
    user navigation across the productivity modules.
    """
    filename = 'to_dos.csv'
    to_do = load_current(filename)
    while True:
        slot = input("Time slot in minutes: ")
        if slot == '':
            break
        slot = int(slot)
        choice, extra = scheduler_helper(slot, to_do)
        if not choice:
            print("None of your to-dos fit in this slot")
        else:
            print(f'{choice}')
            while True:
                if extra is not None:
                    print(f'{extra[0]}')
                    extra = extra[1]
                else:
                    break
# endregion

def main():
    """
    CLI routers initializing the application loop and handling
    user navigation across the productivity modules.
    """
    print('Welcome to the life planner!')
    tag = 'z'
    while True:
        print()
        print("Options:  a) To-do list  b) Sleep tracker  c) Menu plan  d) Scheduler")
        while not 'a' <= tag <= 'd':
            tag = input('~ ')
            if tag == '':
                return
        if tag == 'a':
            todos()
            tag = 'z'
        elif tag == 'b':
            sleep_tracker()
            tag = 'z'
        elif tag == 'c':
            menu_planner()
            tag = 'z'
        elif tag == 'd':
            scheduler()
            tag = 'z'


if __name__ == "__main__":
    main()