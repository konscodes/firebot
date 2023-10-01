'''Firebase Firestore database connection and test
This script will perform the basic read and write on the database'''

import firebase_admin
from firebase_admin import firestore
from datetime import datetime, timezone
import re

class DataBase:
    def __init__(self) -> None:
        self.app = firebase_admin.initialize_app()
        self.db = firestore.client()
        print('[Fire] Init successful')

    def get_rotation(self, chore: str) -> (list[list], str):
        pass
    
    def get_rotation_snapshot(self, chore: str) -> dict:
        pass

    def get_current_index(self, chore: str):
        pass

    def get_names(self, rooms: list) -> tuple:
        pass

    def update_date(self, chore: str, 
                    start_date=datetime.strptime(
                        '2022-12-25 00:00:00', '%Y-%m-%d %H:%M:%S')):
        pass

    def update_index(self, index: int, chore: str):
        pass


def get_rotation_snapshot(chore: str) -> dict:
    '''Get the rotation snapshot from the db.
    
    Args: 
        chore (str): a chore name (e.g. "garbage")

    Returns:
        dict: dict with keys for index and values for lists of rooms
    '''
    chore_ref = db.collection('chores').document(chore)
    chore_snapshot = chore_ref.get(timeout=50000).to_dict()
    return chore_snapshot


def get_current_index(chore: str):
    '''Get the index of current rooms for a given chore.

    Args: 
        chore (str): a chore name (e.g. "garbage")

    Returns:
        int: index int corresponding to rooms list in rotation dict
    '''
    chore_ref = db.collection('chores').document(chore)
    chore_snapshot = chore_ref.get(timeout=50000).to_dict()
    
    try:
        current_index = chore_snapshot['currentIndex']
    except TypeError:
        return 'Snapshot is empty. Index is missing.'
    
    return current_index


def get_rotation(chore: str) -> (list[list], str):
    '''Get a list of rooms on rotation for a given chore
    
    Args:
        chore (str): a chore name (e.g. "garbage")

    Returns:
        list[list]: a list of lists with room numbers for each team
        str: start date of the rotation for further calculations
    '''
    chore_snapshot = get_rotation_snapshot(chore)
    
    try:
        chore_rotation = chore_snapshot['rotation']
    except TypeError:
        return 'Snapshot is empty. Chore name may be wrong.'

    default_date = datetime.strptime('2022-12-25 00:00:00', '%Y-%m-%d %H:%M:%S')

    try:
        start_date = chore_snapshot['startDate']
    except TypeError and KeyError:
        print("Error: Unable to retrieve a valid date. Using default.")
        start_date = default_date

    if not isinstance(start_date, datetime):
        print("Error: The retrieved data is not a datetime object. Using default.")
        start_date = default_date

    rotation = [chore_rotation[f'{index}'] for index in range(len(chore_rotation))]
    return rotation, start_date


def calculate_duty(rotation, start_date, interval='week') -> int:
    '''Calculates who is on duty by extrapolating interval starting from a given date.
    
    Args:
        rotation(list[list]): a list of lists with room numbers for each team
        interval(str), optional: value to extrapolate over (weeks or months)

    Returns:
        tuple(index, [rooms]): an index and a list of room numbers on duty
    '''

    difference = datetime.now(tz=timezone.utc) - start_date

    weeks = difference.days // 7
    months = difference.days // 30
    print('Start date:', start_date)
    print('Delta start and current:', difference.days, 'days')
    print('Weeks', weeks, 'Months', months)

    def calculate_index(interval, rotation):
        # account for less then a single interval from the starting date
        if int(interval == 0):
            return 0, rotation[0]
        # the remainder of modula will correspond to an index in the rotation
        index = (interval % len(rotation))
        return index, rotation[index]

    if interval == 'week':
        return calculate_index(weeks, rotation)
    elif interval == 'month':
        return calculate_index(months, rotation)


def get_names(rooms: list) -> tuple:
    '''Get the names of given room residents
    
    Args:
        rooms(list): a list of rooms to check

    Returns:
        tuple(str): names of all residents in given rooms
    '''
    docs = db.collection('users').stream()
    names = [doc.to_dict()['residentName'] for doc in docs if doc.id in rooms]
    return names


def update_date(chore: str, 
                start_date=datetime.strptime('2022-12-25 00:00:00', '%Y-%m-%d %H:%M:%S')
                ):
    '''Update date for a given chore in the db.'''
    data = {
        "startDate": start_date
    }
    db.collection("chores").document(chore).set(data, merge=True)
    return 'OK'


def update_index(index: int, chore: str):
    '''Update index in the db.
        
    Args:
        index(int): index corresponding to rooms array for given rotation 
    '''
    data = {"currentIndex": index}

    pattern = r'^(garbage|groceries)$'

    if re.match(pattern, chore) is None:
        return 'Error: unable to update the index. Rotation not found.'

    db.collection("chores").document(chore).set(data, merge=True)
    return 'OK'

def main():
    '''Debug function to test the module. This wont be required in final version'''
    rotation, start_date = get_rotation(chore='groceries')
    index, rooms_on_duty = calculate_duty(rotation, start_date, interval='month')
    names = get_names(rooms_on_duty)
    print('Index:', index, 'for rooms', rooms_on_duty)
    print('Names:', names)
    #print('CurrentIndex from db:', get_current_index(chore='groceries'))
    # garbage_rotation, garbage_start_date = get_rotation(chore='garbage')
    # index, rooms_on_duty = calculate_duty(garbage_rotation, garbage_start_date)
    # names = get_names(rooms_on_duty)
    # print('Index:', index, 'for rooms', rooms_on_duty)
    # print('Names:', names)
    # print('CurrentIndex from db:', get_current_index(chore='garbage'))

if __name__ == '__main__':
    # Initialize the app with default credentials
    app = firebase_admin.initialize_app()
    db = firestore.client()

    main()
