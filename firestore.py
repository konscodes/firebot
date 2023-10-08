import re

import firebase_admin
from firebase_admin import firestore


class Data:
    def __init__(self) -> None:
        self.app_instance = firebase_admin.initialize_app()
        self.db = firestore.client(app=self.app_instance)
    
    def get_chore_snapshot(self, chore: str) -> dict:
            '''Get the rotation snapshot from the db.
            
            Args: 
                chore (str): a chore name (e.g. "garbage")

            Returns:
                dict: dict with keys for index and values for lists of rooms
            '''
            chore_ref = self.db.collection('chores').document(chore)
            chore_snapshot = chore_ref.get(timeout=50000).to_dict()
            return chore_snapshot

    def get_names_from_docs(self, rooms: list) -> list:
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
    
    def update_index(self, index: int, chore: str):
        '''Update index in the db for a given chore.
            
        Args:
            index (int): index corresponding to rooms array for given rotation
            chore (str): a chore name (e.g. "garbage")
        '''
        data = {"currentIndex": index}

        pattern = r'^(garbage|groceries)$'

        if re.match(pattern, chore) is None:
            return 'Error: unable to update the index. Rotation not found.'

        self.db.collection("chores").document(chore).set(data, merge=True)
        return 'OK'