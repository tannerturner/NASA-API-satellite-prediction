import sys
import requests
import datetime

def get_list_of_jsons(latitude, longitude):
    url = 'https://api.nasa.gov/planetary/earth/assets'
    begin_date = '2013-01-01'
    api_key = '9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute'
    query = {
        'lat': latitude,
        'lon': longitude,
        'begin': begin_date,
        'api_key': api_key
    }

    try:
        request = requests.get(url, params=query).json()
    except requests.exceptions.RequestException as e:
        print(str(e))
        sys.exit(1)

    list_of_jsons = request['results']
    return list_of_jsons


def get_posix_timestamps(list_of_jsons):
    list_of_date_strings = []
    for x in list_of_jsons:
        list_of_date_strings.append(x['date'])
        
    time_of_date_strings = dict()
    for dateTtime in list_of_date_strings:
        [date, time] = dateTtime.split('T')
        time_of_date_strings[date] = time
        
    sorted_dates = sorted(time_of_date_strings)
    posix_timestamps = []
    for year_month_day in sorted_dates:
        [year, month, day] = year_month_day.split('-')
        [hour, minute, second] = time_of_date_strings[date].split(':')
        dt = datetime.datetime(int(year), int(month), int(day),
                               int(hour), int(minute), int(second))
        posix_timestamps.append(dt.timestamp())
        
    return posix_timestamps


def get_avg_seconds_between_pics(posix_timestamps):
    seconds_since_prev_pic = dict()
    for i in range(1, len(posix_timestamps)):
        curr = posix_timestamps[i]
        prev = posix_timestamps[i - 1]
        diff = curr - prev
        seconds_since_prev_pic[curr] = diff
        
    vals = seconds_since_prev_pic.values()
    avg_seconds_between_pics = sum(vals) / len(vals)
    
    return avg_seconds_between_pics


def predict_next_pic(list_of_jsons):
    posix_timestamps = get_posix_timestamps(list_of_jsons)
    avg_seconds_between_pics = get_avg_seconds_between_pics(posix_timestamps)
    next_pic_posix_timestamp = posix_timestamps[-1] + avg_seconds_between_pics
    next_pic_date_time = datetime.datetime.fromtimestamp(next_pic_posix_timestamp)
    
    return next_pic_date_time


def flyby(latitude=36.098592, longitude=-112.097796):
    list_of_jsons = get_list_of_jsons(latitude, longitude)
    
    if len(list_of_jsons) < 2:
        print('That location is no good! Here is the result for the Grand Canyon! :)')
        list_of_jsons = get_list_of_jsons(36.098592, -112.097796)

    next_pic_date_time = predict_next_pic(list_of_jsons)

    print('Next time: ' + str(next_pic_date_time))

    
def main():
    print('Grand Canyon:')
    flyby(36.098592, -112.097796)
    
    print('Niagara Falls:')           
    flyby(43.078154, -79.075891)
    
    print('Four Corners Monument:')
    flyby(36.998979, -109.045183)
    
    print('Bad location:')
    flyby(0, 0)

    
main()