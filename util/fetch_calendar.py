from datetime import timedelta
import requests
import random
from datetime import datetime


def fetch_data_from_server(date):
    # Get the current date
    today = date
    mm = str(today.month).zfill(2)
    dd = str(today.day).zfill(2)
    yy = str(today.year)

    # Constants
    dt, hh, ll, tt, ss = "1", "1", "1", "1", "1"

    # Construct the URL with query parameters
    base_url = "https://www.holytrinityorthodox.com/calendar/doc/examples/ppp.php?"
    params = {
        "month": mm,
        "today": dd,
        "year": yy,
        "dt": dt,
        "header": hh,
        "lives": ll,
        "trp": tt,
        "scripture": ss,
        "sid": str(int(1000 * random.random())),  # Generating a random number for sid
    }

    # Send the GET request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the response text to a file
        with open(f"../content/calendar/data/{today.year}-{mm}-{dd}.html", "w") as file:
            file.write(response.text)
        print(f"../content/calendar/data/{today.year}-{mm}-{dd}.html saved")
    else:
        print(f"Error: {response.status_code} - {response.reason}")


# Run the function for dates from today through 90 days from now
start_date = datetime.now() + timedelta(60)
end_date = start_date + timedelta(days=90 + 60)
current_date = start_date
while current_date <= end_date:
    fetch_data_from_server(current_date)
    current_date += timedelta(days=1)
