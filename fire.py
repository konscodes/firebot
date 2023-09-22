'''Firebase Firestore database connection and test
This script will perform the basic read and write on the database'''

import firebase_admin
from firebase_admin import firestore
from datetime import datetime

# Initialize the app with default credentials
app = firebase_admin.initialize_app()

db = firestore.client()

def get_rotation(chore: str) -> list[list]:
    '''Get a list of rooms on rotation for a given chore
    
    Args:
        chore (str): a chore name (e.g. "garbage")

    Returns:
        list[list]: a list of lists with room numbers for each team
    '''
    chore_ref = db.collection('chores').document(chore)

    chore_snapshot = chore_ref.get(timeout=50000).to_dict()
    try:
        chore_rotation = chore_snapshot['rotation']
    except TypeError:
        return 'Snapshot is empty. Chore name may be wrong'
    
    rotation = [chore_rotation[f'{index}'] for index in range(len(chore_rotation))]
    return rotation


def get_name(room: str) -> str:
    '''Get the name of given room resident'''
    room_ref = db.collection('users').document(room)
    name = room_ref.get(timeout=50000).to_dict()['residentName']
    return name


def calculate_duty(rotation, interval='week', start_date='Jan 1, 2023') -> int:
    '''Calculates who is on duty by extrapolating interval starting from a given date.
    
    Args:
        rotation(list[list]): a list of lists with room numbers for each team
        interval(str), optional: value to extrapolate over (weeks or months)
        starting_date(str), optional: starting date of the rotation 

    Returns:
        tuple(index, [rooms]): an index and a list of room numbers on duty
    '''
    start_datetime = datetime.strptime(start_date, '%b %d, %Y')
    current_datetime = datetime.now()

    difference = current_datetime - start_datetime

    weeks = difference.days // 7
    months = difference.days // 30
    print('Start date:', start_date)
    print('Delta start and current:', difference.days, 'days')
    print('Weeks', weeks, 'Months', months)

    if interval == 'week' and int(weeks==0):
        return (0, rotation[0])
    elif interval == 'week':
        index = (weeks % len(rotation))
        return (index, rotation[index])

    if interval == 'months' and int(weeks==0):
        return (0, rotation[0])
    elif interval == 'months':
        index = (months % len(rotation))
        return (index, rotation[index])


#print(get_name('A101'))
garbage_rotation = get_rotation('garbage')

rooms_on_duty = calculate_duty(garbage_rotation)
#rooms = garbage_rotation[rooms_on_duty]
print(rooms_on_duty)