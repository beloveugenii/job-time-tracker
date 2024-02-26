from time import sleep

messages = {
    'not_impl': 'Not implemented yet',
    'ua': 'Unsupported action',
    'small_str': 'Too small string',
    'need_gender': 'A gender designation is required: [mM or fF]',
    'need_number': 'A number is required',
    'not_in_list': 'User with this number not in list',
    'interactive':
        "Enter the numbers of the required workout programs separated by spaces\n'c' for creating new training\n'r' to remove existed training\n'e' for editing the training\n'h' show this help\n'q' quit",
    'users':
        "Type user ID for choosing\n'n' create new user\n'dNUM' for removing user with id NUM\n'h' show this help\n'q' quit",
    'diary':
        "Enter the name of the food to be entered in the diary\n'n' go to the next day\n'p' go to the previous day\n'l' show food in database\n't' go to sport assistant\n'h' show this help\n'q' quit",
    'food_db':
        "Enter the name of the food to be entered in database\n'a' analyze the complex dish\n'r' remove from database\n'h' show this help\n'q' go back",
    'analyzer':
        "Enter the name of the food to be entered in the diary\n'c' create a new dish\n'r' remove an existing dish\n'h' show this help\n'q' quit",
    'activity':
        "1.2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок\n1.375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю\n1.55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю\n1.7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю или трудоемкие занятия\n1.9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности",
}

def help(*args):

    print(messages[args[0]])

    if len(args) > 1:
        sleep(args[1])
    else:
        empty_input = input()
