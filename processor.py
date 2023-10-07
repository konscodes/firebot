import line
from firestore import Data


def get_names(data: Data, chore: str) -> list:
    '''Get the list on names on duty for a given chore.

    Args:
        data (Data): firestore instance with methods to get the data
        chore (str): a chore name (e.g. "garbage")

    Returns:
        list: List of names on duty
    '''
    snapshot = data.get_chore_snapshot(chore)

    index = snapshot['currentIndex']
    rooms_on_duty = snapshot['rotation'][f'{index}']

    names = data.get_names_from_docs(rooms_on_duty)
    print('Index:', index, 'for rooms', rooms_on_duty)
    print('Names:', names)
    return names


if __name__ == '__main__':
    garbage_names = get_names(data=Data(), chore='garbage')

    group_id = 'Cd8838ffe33ac87f0595ac2be8ce6579f'  # Test group
    message = ', '.join(garbage_names)

    line.send_push(group_id, message)