import datetime
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.write',
    'https://www.googleapis.com/auth/fitness.activity.read'
]

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def insert_session_steps(creds, steps=100):
    fitness_service = build('fitness', 'v1', credentials=creds)

    # Use a fixed time in the past (e.g. last 30 minutes)
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time_dt = now - datetime.timedelta(minutes=30)
    end_time_dt = now

    # Milliseconds for dataset ID
    start_time_millis = int(start_time_dt.timestamp() * 1000)
    end_time_millis = int(end_time_dt.timestamp() * 1000)

    # Nanoseconds for step data points
    start_nanos = int(start_time_dt.timestamp() * 1e9)
    end_nanos = int(end_time_dt.timestamp() * 1e9)

    # Create or reuse custom data source
    data_source_body = {
        "dataStreamName": "PythonManualSteps",
        "type": "raw",
        "application": {
            "name": "StepUp Script"
        },
        "dataType": {
            "name": "com.google.step_count.delta",
            "field": [{
                "name": "steps",
                "format": "integer"
            }]
        },
        "device": {
            "uid": "python-script-001",
            "type": "unknown",
            "version": "1.0",
            "model": "script",
            "manufacturer": "me"
        }
    }

    try:
        result = fitness_service.users().dataSources().create(userId='me', body=data_source_body).execute()
        print("✅ Data source created.")
        data_source_id = result["dataStreamId"]
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ Data source already exists. Fetching...")
            all_sources = fitness_service.users().dataSources().list(userId='me').execute()
            matching = [src for src in all_sources.get("dataSource", []) if src["dataStreamName"] == "PythonManualSteps"]
            if matching:
                data_source_id = matching[0]["dataStreamId"]
            else:
                raise RuntimeError("❌ Data source not found even though it says it exists.")
        else:
            raise e

    dataset_id = f"{start_time_millis}-{end_time_millis}"

    # Add step data to dataset
    fitness_service.users().dataSources().datasets().patch(
        userId='me',
        dataSourceId=data_source_id,
        datasetId=dataset_id,
        body={
            "dataSourceId": data_source_id,
            "maxEndTimeNs": end_nanos,
            "minStartTimeNs": start_nanos,
            "point": [{
                "startTimeNanos": start_nanos,
                "endTimeNanos": end_nanos,
                "dataTypeName": "com.google.step_count.delta",
                "value": [{"intVal": steps}]
            }]
        }
    ).execute()

    # Create session with step data linked
    session_id = f"manual-steps-{start_time_millis}"
    fitness_service.users().sessions().update(
        userId='me',
        sessionId=session_id,
        body={
            "id": session_id,
            "name": "Manual Step Session",
            "description": f"{steps} steps manually inserted.",
            "startTimeMillis": start_time_millis,
            "endTimeMillis": end_time_millis,
            "activityType": 7,  # Walking
            "application": {
                "name": "StepUp Script"
            }
        }
    ).execute()

    print(f"✅ Inserted {steps} steps as a visible walking session!")

if __name__ == '__main__':
    creds = get_credentials()
    insert_session_steps(creds, steps=100)
