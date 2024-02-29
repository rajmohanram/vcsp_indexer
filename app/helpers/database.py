from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker
from app.models.vcsp import Event
from pathlib import Path


# Get the current file directory
app_dir = Path(__file__).parent.parent.parent
# Combine the path with app.db
db_path = app_dir / 'data/app.db'
db_url = 'sqlite:///' + str(db_path)

# Create an engine
engine = create_engine(db_url)


# Create a session
def get_db_session():
    session = sessionmaker(bind=engine)
    return session()


if __name__ == "__main__":
    # Query to fetch unique values of the 'bucket' column with status 'scheduled'
    db_session = get_db_session()
    buckets = db_session.query(distinct(Event.bucket)).filter(Event.status == 'scheduled').all()

    # Print the unique bucket values
    for bucket in buckets:
        print(bucket[0])

    # Close the session
    db_session.close()
