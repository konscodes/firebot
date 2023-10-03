'''Firebase Firestore database connection and test
This script will perform the basic read and write on the database'''

import re
from datetime import datetime

import firebase_admin
from firebase_admin import firestore


class DataBase:

    def __init__(self) -> None:
        self.app = firebase_admin.initialize_app()
        self.db = firestore.client()
        print('[Fire] Init successful')

    def get_rotation_snapshot(self, chore: str) -> dict:
        '''Get the rotation snapshot from the db.
        
        Args: 
            chore (str): a chore name (e.g. "garbage")

        Returns:
            dict: dict with keys for index and values for lists of rooms
        '''
        chore_ref = self.db.collection('chores').document(chore)
        chore_snapshot = chore_ref.get(timeout=50000).to_dict()
        return chore_snapshot

    def get_rotation(self, chore: str) -> tuple[list[list], datetime]:
        '''Get a list of rooms on rotation for a given chore
        
        Args:
            chore (str): a chore name (e.g. "garbage")

        Returns:
            list[list]: a list of lists with room numbers for each team
            datetime: start date of the rotation for further calculations
        '''
        chore_snapshot = self.get_rotation_snapshot(chore)
        default_date = datetime.strptime('2022-12-25 00:00:00',
                                         '%Y-%m-%d %H:%M:%S')
        try:
            chore_rotation = chore_snapshot['rotation']
        except TypeError:
            error = 'Snapshot is empty. Chore name may be wrong.'
            print(error)
            return ([], default_date)

        try:
            start_date = chore_snapshot['startDate']
        except (TypeError, KeyError):
            print("Error: Unable to retrieve a valid date. Using default.")
            start_date = default_date

        if not isinstance(start_date, datetime):
            print(
                "Error: The retrieved data is not a datetime object. Using default."
            )
            start_date = default_date

        rotation = [
            chore_rotation[f'{index}'] for index in range(len(chore_rotation))
        ]
        return rotation, start_date

    def get_current_index(self, chore: str):
        '''Get the index of current rooms for a given chore.

        Args: 
            chore (str): a chore name (e.g. "garbage")

        Returns:
            int: index int corresponding to rooms list in rotation dict
        '''
        chore_ref = self.db.collection('chores').document(chore)
        chore_snapshot = chore_ref.get(timeout=50000).to_dict()

        try:
            current_index = chore_snapshot['currentIndex']
        except TypeError:
            return 'Snapshot is empty. Index is missing.'

        return current_index

    def get_names(self, rooms: list) -> list:
        '''Get the names of given room residents
        
        Args:
            rooms(list): a list of rooms to check

        Returns:
            list(str): names of all residents in given rooms
        '''
        docs = self.db.collection('users').stream()
        names = [
            doc.to_dict()['residentName'] for doc in docs if doc.id in rooms
        ]
        return names

    def get_code(self) -> str:
        '''Get the pass code from the db.
        The code will be used to associate with Line group id'''
        return '5034'

    def update_group_id(self, code: str, group_id: str):
        '''Associate the id of a Line group with db instance using access code.
        
        Args:
            code(str): pass code associated with db instance (part of the collection)
            group_id(str): Line group chat id
        '''
        data = {"groupID": group_id}
        self.db.collection(code).document('LineGroup').set(data, merge=True)
        return 'OK'

    def update_date(self, chore: str, start_date: datetime):
        '''Update date for a given chore in the db.

        Args:
            chore(str): a chore name (e.g. "garbage")
            start_date(datetime): start of the rotation; default value is 
                datetime.strptime('2022-12-25 00:00:00', '%Y-%m-%d %H:%M:%S')
        '''
        data = {"startDate": start_date}
        self.db.collection("chores").document(chore).set(data, merge=True)
        return 'OK'

    def update_index(self, index: int, chore: str):
        '''Update index in the db.
            
        Args:
            index(int): index corresponding to rooms array for given rotation 
        '''
        data = {"currentIndex": index}

        pattern = r'^(garbage|groceries)$'

        if re.match(pattern, chore) is None:
            return 'Error: unable to update the index. Rotation not found.'

        self.db.collection("chores").document(chore).set(data, merge=True)
        return 'OK'
