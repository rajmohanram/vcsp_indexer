import logging
from app.models.vcsp import Event
from app.helpers import get_conn_vars
from app.helpers.database import get_db_session
from app.vcsp.s3reindex import reindex_bucket
from datetime import datetime
import pytz


def convert_to_syd_time(iso_utc_string):
    # Convert ISO 8601 string to datetime object
    utc_time = datetime.fromisoformat(iso_utc_string[:-1])

    # Localize UTC time to the local time zone
    local_timezone = pytz.timezone('Australia/Sydney')
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

    return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")


def process_request(data):
    records = data.get("Records")
    record = records[0]
    event_time = convert_to_syd_time(record.get("eventTime"))
    user_id = record.get("userIdentity", {}).get("principalId")
    event_name = record.get("eventName")
    s3bucket = record.get("s3", {}).get("bucket", {}).get("name")
    s3object = record.get("s3", {}).get("object", {}).get("key").replace("%2F", "/")
    status = "Scheduled"
    event = {'event_time': event_time,
             'user_id': user_id,
             'event_name': event_name,
             's3bucket': s3bucket,
             's3object': s3object,
             'status': status
             }
    return event


# @scheduler.task('interval', id='init_reindex', seconds=30)
def init_reindex(data):
    event = process_request(data)
    conn_vars = get_conn_vars()
    db_session = get_db_session()
    # buckets = db_session.query(distinct(Event.bucket)).filter(Event.status == 'scheduled').all()
    conn_vars['library_name'] = event['s3bucket']
    conn_vars['library_path'] = event['s3bucket']
    logging.info(f"Event: {event['event_name']} : Bucket: {event['s3bucket']}, Object: {event['s3object']}.")

    if not '.json' in event['s3object']:
        logging.info(f"Indexing S3 Bucket contents.")
        status = reindex_bucket(conn_vars)
        logging.info(status)

        try:
            # Insert record to table
            event = Event(eventTime=event['event_time'],
                          eventName=event['event_name'],
                          userid=event['user_id'],
                          bucket=event['s3bucket'],
                          object=event['s3object'],
                          status=status)
            db_session.add(event)
            db_session.commit()
            logging.info(f"Event added to the DB.")
        except Exception as e:
            db_session.session.rollback()
            logging.error(f"Error adding event to DB: {str(e)}")

    else:
        logging.info(f"Indexing ignored  for JSON metadata files.")

    # Close the session
    db_session.close()


