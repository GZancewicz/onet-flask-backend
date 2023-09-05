from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import pytz
from calendar_credentials import get_api_key


def fetch_calendar_events(api_key=get_api_key()):
    # Initialize the Calendar API client with an API key
    service = build("calendar", "v3", developerKey=api_key)

    # Get the current time in Central Time
    central = pytz.timezone("US/Central")
    now_central = datetime.now(central)

    # Set the time to midnight to represent the start of the day in Central Time
    start_of_today_central = now_central.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Calculate the date 7 days later, also at midnight in Central Time
    end_of_7_days_central = start_of_today_central + timedelta(days=7)

    # Convert to ISO format
    timeMin = start_of_today_central.isoformat()
    timeMax = end_of_7_days_central.isoformat()

    print("Fetching events from:", timeMin)
    print("Fetching events up to:", timeMax)

    # Fetch events
    events_result = (
        service.events()
        .list(
            calendarId="s37s3qvlf9nobhplqp0umlcafs@group.calendar.google.com",  # Replace with your actual Calendar ID
            timeMin=timeMin,
            timeMax=timeMax,
            maxResults=15,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    # Convert to JSON
    events_json = json.dumps(events, indent=4)

    return events_json


def extract_events(events_json):
    events_list = json.loads(events_json)
    extracted_events = []
    last_date = None  # Initialize variable to keep track of the last date

    for event in events_list:
        original_start_time = event["start"].get("dateTime")

        # Skip the event if dateTime is not present
        if original_start_time is None:
            continue

        # Parse the original start time into a datetime object
        original_start_time = datetime.fromisoformat(original_start_time)

        # Convert to the event's local time zone
        local_tz = pytz.timezone(event["start"].get("timeZone", "UTC"))
        local_start_time = original_start_time.astimezone(local_tz)

        # Format the date and time as required
        formatted_date = local_start_time.strftime("%a - %b %d").replace(" 0", " ")
        formatted_time = (
            local_start_time.strftime("%-I:%M%p").lower().lstrip("0").replace(":00", "")
        )

        # Extract the event summary
        summary = event.get("summary", "No Summary")

        # Check if the date is different from the last one or if it's the first entry
        if last_date is None or last_date != formatted_date:
            date_to_use = formatted_date
        else:
            date_to_use = ""

        # Update the last date
        last_date = formatted_date

        # Create a dictionary with the extracted info
        extracted_event = {
            "date": date_to_use,
            "time": formatted_time,
            "service": summary,
        }

        extracted_events.append(extracted_event)

    return extracted_events


def return_calendar_events():
    events_json = fetch_calendar_events()
    calendar_json = extract_events(events_json)
    return calendar_json


if __name__ == "__main__":
    test_json = fetch_calendar_events()
    # calendar_json = return_calendar_events()
    print("Fetched events in JSON format:")
    print(test_json)
