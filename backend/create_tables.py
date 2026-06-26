import os
import sys

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Base, engine
# Import all models so SQLAlchemy registers them
import app.models

def init_db():
    print(f"Attempting to connect to database using engine URL...")
    try:
        # This command creates all tables defined in our models
        Base.metadata.create_all(bind=engine)
        print("Successfully created all tables in the database!")
    except Exception as e:
        print("Error creating tables:")
        print(e)

if __name__ == "__main__":
    init_db()