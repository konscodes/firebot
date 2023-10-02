'''Main function to be executed with cron job.
- Access the db from fire module
- Rotate the duty
- Send a reminder to Line with line module'''
from fire import DataBase
import line_messaging
from datetime import datetime, timezone

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


def main():
    fire = DataBase()

    chore = 'garbage'
    rotation, start_date = fire.get_rotation(chore)
    index, rooms_on_duty = calculate_duty(rotation, start_date)
    names = fire.get_names(rooms_on_duty)
    print('Index:', index, 'for rooms', rooms_on_duty)
    print('Names:', names)

    group_id = 'test'
    message = 'test'
    line_messaging.send_push(group_id, message)


if __name__ == '__main__':
    main()