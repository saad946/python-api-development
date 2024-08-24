from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Tubelight1%40@localhost/postgres"



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # This is the base class for all our models. All models should inherit from this class.

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()










# create_engine: This function is used to create an instance of an engine, which manages the connection pool and handles communication with the database.
# declarative_base: This function returns a base class from which all ORM (Object-Relational Mapping) models will inherit. It keeps track of all the models and provides a table for each.
# sessionmaker: This function is a factory for creating new Session objects, which are the main interface used to interact with the database.

# The Base class created by declarative_base() automatically manages metadata for all the models that inherit from it. Metadata is a collection of all the table objects and is responsible for creating and managing tables in the database.



# get_db: This function is a dependency that you can use in your application to get a database session.
# It creates a new session using SessionLocal().
# yield db returns the session to the caller.
# The finally block ensures that the session is closed after use, even if an exception occurs.