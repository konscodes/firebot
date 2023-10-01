'''Main function to be executed with cron job.
- Access the DB from fire module
- Rotate the duty
- Send a reminder to Line'''
from fire import DataBase

db = DataBase()

def main():
    print('Running main func')

if __name__ == '__main__':
    main()