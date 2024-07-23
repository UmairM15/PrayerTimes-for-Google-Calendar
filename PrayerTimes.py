import pandas as pd
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dateutil import parser
import os
import pickle
from google.auth.transport.requests import Request  # Import Request class


# Prayer durations (in minutes)
PRAYER_DURATIONS = {
    "Fajr Iqama": 15,
    "Zuhr Iqama": 35,
    "Asr Iqama": 20,
    "Maghrib Iqama": 30,
    "Isha Iqama": 50,
}

# Replace these with the correct values
CLIENT_SECRETS_FILE = "credentials.json"
TOKEN_PICKLE_FILE = "token.pickle"
CALENDAR_ID = ""  # Replace with the actual calendar ID
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Authentication function to get credentials
def get_credentials():
    creds = None
    # Load the saved credentials from file
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds


# Function to get the last Sunday
def get_last_sunday(reference_date):
    if reference_date.weekday() == 6:
        return reference_date - timedelta(days=1)
    days_since_sunday = reference_date.weekday() + 2
    last_sunday = reference_date - timedelta(days=days_since_sunday)
    return last_sunday


# Function to filter the week data
def filter_week_data(df, start_date):
    start_date = pd.to_datetime(start_date)
    end_date = start_date + timedelta(days=7)
    df["Date"] = pd.to_datetime(
        df["Month"] + " " + df["Day"].astype(str) + ", " + str(datetime.now().year),
        format="%B %d, %Y",
    )
    week_data = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    return week_data


# Function to convert 12-hour time format to 24-hour format
def convert_to_24hr(time_str):
    try:
        return parser.parse(time_str).strftime("%H:%M:%S")
    except ValueError:
        return None


# Function to create an event
def create_event(service, calendar_id, summary, start_time, end_time):
    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time,
            "timeZone": "America/Toronto",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "America/Toronto",
        },
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()


# Main script
def main():
    current_date = datetime.now()
    last_sunday = get_last_sunday(current_date)
    print(f"Last Sunday relative to today: {last_sunday.date()}")

    prayer_times_url = (
        "https://markhammasjid.ca/wp-content/scripts/ism-2019-prayer-times.csv"
    )
    prayer_times = pd.read_csv(prayer_times_url)

    week_data = filter_week_data(prayer_times, last_sunday)
    print(week_data)

    # Authenticate and build the service
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    # Upload events for the week
    for _, row in week_data.iterrows():
        for prayer, duration in PRAYER_DURATIONS.items():
            time_str = row[prayer]
            time_24hr = convert_to_24hr(time_str)
            if time_24hr:
                start_time = f"{row['Date'].strftime('%Y-%m-%d')}T{time_24hr}"
                end_time = (
                    datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
                    + timedelta(minutes=duration)
                ).strftime("%Y-%m-%dT%H:%M:%S")
                print(
                    f"Creating event for {prayer} on {row['Date'].strftime('%Y-%m-%d')} from {start_time} to {end_time}"
                )
                create_event(service, CALENDAR_ID, prayer, start_time, end_time)
                print(f"Event for {prayer} created successfully.")
            else:
                print(f"Invalid time format for {prayer}: {time_str}")


if __name__ == "__main__":
    main()
