import firebase_admin
from firebase_admin import firestore

# Initialize the app with default credentials
app = firebase_admin.initialize_app()

db = firestore.client()

def get_name(room: str) -> str:
    '''Returns the name of given room resident'''
    room_ref = db.collection('users').document(room)
    name = room_ref.get().to_dict()['residentName']
    return name


def get_rooms(index: str, duty: str) -> list:
    '''Returns the room list for given team index on duty'''
    garbage_ref = db.collection('chores').document(duty)

    garbage_snapshot = garbage_ref.get().to_dict()
    garbage_rotation = garbage_snapshot['rotation']

    rooms = garbage_rotation[index]
    return rooms


#print(get_rooms('0', 'garbage'))
print(get_name('A101'))
