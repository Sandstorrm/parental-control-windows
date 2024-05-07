import datetime, os

points_file = 'points.txt'

def Count():
    count = 0
    points_file = 'points.txt'
    if not os.path.exists(points_file):
        with open(points_file, 'w'):
            print('Points file created.')

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    current_date = today.strftime('%m/%d/%y')
    yesterday_date = yesterday.strftime('%m/%d/%y')

    with open(points_file, 'r') as file:
        for line in file:
            date_time_str = line.strip()
            if current_date in date_time_str:
                count += 1

            if  yesterday_date in date_time_str:
                date_part, time_part = date_time_str.split(' - ')
                hour, minute_part = time_part.split(':')
                minute, period = minute_part.split()
                if period == 'PM' and int(hour) >= 10:
                    count += 1
    return count


print(Count())