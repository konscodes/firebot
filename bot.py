import line
from firestore import Data


def run():
    # Initialize the connection to Firestore
    data = Data()
    chore = 'garbage'

    # Get the data
    snapshot = data.get_chore_snapshot(chore)
    rotation = snapshot['rotation']
    current_index = snapshot['currentIndex']

    # Calculate the next rotation
    next_index = 0 if current_index > (len(rotation) - 1) else current_index + 1
    rooms_on_duty = snapshot['rotation'][f'{next_index}']

    # Get the names
    names = data.get_names_from_docs(rooms_on_duty)
    print('New index:', next_index, 'for rooms', rooms_on_duty)
    print('Names:', names)

    # Update the new index in the db
    data.update_index(index=next_index, chore=chore)

    # Get the group id for a line group and send a message to line
    group_id = 'Cd8838ffe33ac87f0595ac2be8ce6579f'  # Test group
    group_name = 'Omotesando House'
    names = ', '.join(names)
    message = f'Good morning dear people of {group_name}!\n\nThis week {chore} duty members: {names}'
    line.send_push(group_id, message)

if __name__ == '__main__':
    run()
