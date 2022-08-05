import pandas as pd # install lxml
from datetime import datetime

locations = [
    'Half Moon Bay, California', 
    'Huntington Beach', # url does not work with: , California
    'Providence, Rhode Island', 
    'Wrightsville Beach, North Carolina'
]

# Extract information on low tides that occur after sunrise and before sunset. 
# Return the time and height for each daylight low tide.

for location in locations:
    location = location.replace(",", "").replace(" ", "-")
    url = 'https://www.tide-forecast.com/locations/' + location + '/tides/latest'
    print(url + "\n")
    tables = pd.read_html(url)

    # Start from third table and ignore today's since no Sunset info yet, skip every 2
    for i in range(3, len(tables), 2):
        day_table = tables[i]
        sun_table = tables[i+1]
        sunrise = sun_table[0][0][9:] #'Sunrise: 7:17AM'
        sunset = sun_table[1][0][8:] #'Sunset: 7:19PM'

        for row in day_table.iterrows():
            if row[1]['Tide'] == 'Low Tide':
                tide_datetime = row[1][1] #'4:47 AM(Thu 17 March)'
                tide_time = tide_datetime.rsplit("(")[0]
                tide_date = tide_datetime.rsplit("(")[1].replace(")", "")
                tide_height = row[1][2] # '0.52 m (1.69 ft)'

                tide_dt_object = datetime.strptime(tide_time, '%H:%M %p') # H (24-hour clock) zero-padded dec num 
                sunrise_dt_object = datetime.strptime(sunrise, '%I:%M%p')
                sunset_dt_object = datetime.strptime(sunset, '%I:%M%p')

                if sunrise_dt_object < tide_dt_object < sunset_dt_object:
                    print("Low Tide on {} at {}, height of {}".format(tide_date, tide_time, tide_height))
    print("\n")


