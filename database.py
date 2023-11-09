import sqlite3
import datetime

con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()


def login_check(login, password):
    cur.execute(f"SELECT * FROM Users WHERE login = '{login}' and password = '{password}'")
    try:
        records = list(cur.fetchall())[0]
    except:
        return False

    if not records:
        return False
    return records


def id_generator():
    cur.execute(f"SELECT ID FROM Users")
    res = cur.fetchall()
    res = [i[0] for i in res]
    for i in range(1, max(res) + 2):
        if i not in res:
            return i
    return False


def add_user(login, password, name, second_name):
    group = 'bvt2205'
    ID = id_generator()
    cur.execute(f"INSERT INTO Users VALUES ({ID}, '{login}', '{password}', '{name}', '{second_name}', {group})")
    con.commit()


def get_user(user_id):
    cur.execute(f"SELECT * FROM Users WHERE ID = {user_id}")
    res = cur.fetchall()[0]
    return res


def get_queue(subject_id):
    cur.execute(f'SELECT queue_list FROM queue WHERE subject_id = {subject_id}')
    res = cur.fetchall()[0]
    res = res[0].split(' ')
    return res


def create_queue_string(subject_id):
    queue = get_queue(subject_id)

    cur.execute(f'SELECT first_name, second_name FROM Users WHERE ID = {queue[0]}')
    q1 = cur.fetchall()[0]

    cur.execute(f'SELECT first_name, second_name FROM Users WHERE ID = {queue[1]}')
    q2 = cur.fetchall()[0]

    cur.execute(f'SELECT first_name, second_name FROM Users WHERE ID = {queue[2]}')
    q3 = cur.fetchall()[0]

    cur.execute(f'SELECT first_name, second_name FROM Users WHERE ID = {queue[3]}')
    q4 = cur.fetchall()[0]

    return [q1, q2, q3, q4]


def get_subjects(user_id):
    cur.execute(f"SELECT group_name FROM Users WHERE ID = {user_id}")
    group = cur.fetchall()[0][0]
    cur.execute(f"SELECT * FROM Subjects WHERE group_name = '{group}'")
    response = cur.fetchall()

    res = [i for i in response]

    return res


def week_even():
    current_date = datetime.datetime.now()
    week_number = current_date.isocalendar()[1]
    if week_number % 2 == 0:
        return True
    return False


def find_closest_day(data):
    if week_even():
        current_week_parity = 1
    else: current_week_parity = 0

      #  = datetime.datetime.now().isocalendar()[1] % 2  # Определение чётности текущей недели

    closest_day = None
    min_days_difference = float('inf')

    for item in data:
        week_parity = item[0]
        day_of_week = item[1]

        if week_parity != current_week_parity:
            continue

        # Вычисление разницы в днях между выбранным днем и текущим днем
        day_difference = (day_of_week - datetime.datetime.now().isoweekday()) % 7

        if day_difference < min_days_difference:
            min_days_difference = day_difference
            closest_day = item

    return closest_day


def nearby_subject(user_id):
    response = get_subjects(user_id)
    memory = []
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    datetime.datetime()


def can_access(user_id):
    pass

data = [
    [1, 3, '12:00'],  #
    [1, 1, '14:00'],  #
    [0, 5, '14:00'],  #
    [0, 2, '14:00'],  #
]
print(find_closest_day(data))
