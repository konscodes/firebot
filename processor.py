import line
from firestore import Data

if __name__ == '__main__':
    data = Data()

    snapshot = data.get_chore_snapshot(chore='garbage')
    index = snapshot['currentIndex']
    rooms_on_duty = snapshot['rotation'][f'{index}']

    names = data.get_names_from_docs(rooms_on_duty)
    print('Index:', index, 'for rooms', rooms_on_duty)
    print('Names:', names)

    group_id = 'Cd8838ffe33ac87f0595ac2be8ce6579f'  # Test group
    message = ', '.join(names)

    line.send_push(group_id, message)

# TODO 
# 1. Add rotation function to +1 the current index
#   - add update index function to firestore py
# 2. Put this bot on cloud functions