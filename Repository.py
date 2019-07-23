from app import db
from typing import TypeVar,Generic

def GetAll(tablename):
    T = TypeVar('tablename')
    
