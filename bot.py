'''Main function to be executed with cron job.
- Access the db from fire module
- Rotate the duty
- Send a reminder to Line with line module'''
from datetime import datetime, timezone

import line_messaging
from fire import DataBase


def calculate_duty(rotation,
                   start_date,
                   interval='week') -> tuple[int, list[int]]:
    '''Calculates who is on duty by extrapolating intervals starting from a given date.
    
    Args:
        rotation(list[list]): a list of lists with room numbers for each team
        interval(str), optional: value to extrapolate over (weeks or months)

    Returns:
        Tuple[int, List[int]]: an index and a list of room numbers on duty
    '''

    difference = datetime.now(tz=timezone.utc) - start_date

    weeks = difference.days // 7
    months = difference.days // 30
    print('Start date:', start_date)
    print('Delta start and current:', difference.days, 'days')
    print('Weeks', weeks, 'Months', months)

    def calculate_index(counter: int, rotation: list):
        # Account for less than a single interval from the starting date
        if counter == 0:
            return 0, rotation[0]
        # The remainder of the module will correspond to an index in the rotation
        index = (counter % len(rotation))
        return index, rotation[index]

    if interval == 'week':
        return calculate_index(int(weeks), rotation)
    elif interval == 'month':
        return calculate_index(int(months), rotation)
    else:
        # Default case
        return 0, rotation[0]


def main():
    fire = DataBase()

    chore = 'garbage'
    rotation, start_date = fire.get_rotation(chore)
    index, rooms_on_duty = calculate_duty(rotation, start_date)
    names = fire.get_names(rooms_on_duty)
    print('Index:', index, 'for rooms', rooms_on_duty)
    print('Names:', names)

    group_id = 'Cd8838ffe33ac87f0595ac2be8ce6579f'  # Test group
    message = str(names)
    line_messaging.send_push(group_id, message)


if __name__ == '__main__':
    main()
