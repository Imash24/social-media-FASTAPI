from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True,  nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")
    phone_number = Column(String)

    
    
class User(Base):  # this is the requirement for sqlalchemy model
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, unique=True, nullable = False)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default = text('now()'))
    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key= True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key= True)
    