from config import settings
from models import (
    user,
    user_link,
    user_profile,
)
from sqlmodel import create_engine

# Make sure all SQLModels are imported from (models)
# before initializing the database otherwise, SQLModel
# might fail.
# See: https://github.com/fastapi/full-stack-fastapi-template/issues/28

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
