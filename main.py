import functions_framework

import line
from firestore import Data


@functions_framework.http
def webhook(request=None):
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
    group_id = 'Cf76f719c42b3154f974783b4bcfb454f'  # hardcode the group id
    group_name = 'Omotesando House' # hardcode the group name
    names = ', '.join(names)
    message = f'Good morning dear people of {group_name}!\n\nThis week {chore} duty members: {names}'  # noqa: E501
    line.send_push(group_id, message)

    return 'OK', 200

if __name__ == '__main__':
    webhook()