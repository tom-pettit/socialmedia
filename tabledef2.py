from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
postengine = create_engine('sqlite:///socialmediaposts.db', echo=True)
Base = declarative_base()
 
########################################################################
class Posts(Base):
    """"""
    __tablename__ = "posts"
 
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    user = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, title, text, user):
        """"""
        self.title = title
        self.text = text
        self.user = user
# create tables
Base.metadata.create_all(postengine)
