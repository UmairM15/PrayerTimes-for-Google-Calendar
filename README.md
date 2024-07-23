## Project: Prayer Times for Google Calendar (Markham)

This project automates the process of uploading daily prayer times to a Google Calendar. The script reads prayer times from a CSV file, filters the data for the current week (Sunday to Saturday), and creates calendar events using the Google Calendar API.

### Features
- **CSV Parsing**: Reads prayer times from a CSV file with columns for different prayers.
- **Date Handling**: Identifies the last Sunday relative to the current date and filters prayer times for the week.
- **Event Creation**: Converts prayer times to Google Calendar events with configurable durations.
- **Google Calendar Integration**: Authenticates with the Google Calendar API to upload events.

### Requirements
- Python 3.x
- Pandas
- Dateutil
- Google API Client
- OAuth2

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/prayer-times-to-google-calendar.git
   cd prayer-times-to-google-calendar
   ```

2. Install the required packages:
   ```sh
   pip install pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dateutil
   ```

3. Obtain Google Calendar API credentials:
   - Create a project on the [Google Cloud Console](https://console.developers.google.com/).
   - Enable the Google Calendar API.
   - Create OAuth 2.0 Client IDs and download the `credentials.json` file.
   - Place the `credentials.json` file in the project directory.

### Usage
1. Set the constants in the script:
   - **CLIENT_SECRETS_FILE**: Path to the `credentials.json` file.
   - **TOKEN_PICKLE_FILE**: Path to the token pickle file to store user credentials.
   - **CALENDAR_ID**: ID of the Google Calendar where events will be created.

2. Run the script:
   ```sh
   python script.py
   ```

### Script Overview
Here's an overview of the key functions in the script:

- **get_credentials()**: Handles authentication with Google Calendar API and returns credentials.
- **get_last_sunday(reference_date)**: Finds the last Sunday relative to a given date.
- **filter_week_data(df, start_date)**: Filters the prayer times for the week starting from a given date.
- **convert_to_24hr(time_str)**: Converts 12-hour time format to 24-hour format.
- **create_event(service, calendar_id, summary, start_time, end_time)**: Creates a Google Calendar event.

### Example Output
The script prints the last Sunday relative to the current date, the filtered prayer times for the week, and messages indicating the creation of events for each prayer.

```plaintext
Last Sunday relative to today: 2024-07-14
Creating event for Fajr Iqama on 2024-07-14 from 2024-07-14T05:00:00 to 2024-07-14T05:15:00
Event for Fajr Iqama created successfully.
...
```

### Configurable Prayer Durations
Prayer durations can be easily modified in the `PRAYER_DURATIONS` dictionary in the script:
```python
PRAYER_DURATIONS = {
    "Fajr Iqama": 15,
    "Zuhr Iqama": 35,
    "Asr Iqama": 20,
    "Maghrib Iqama": 30,
    "Isha Iqama": 50,
}
```

### Contributions
Feel free to submit issues or pull requests to improve the project.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
