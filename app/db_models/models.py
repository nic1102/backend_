from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    is_validated = Column(Boolean, default=False, nullable=False)

    # Relationship to songs
    songs = relationship("Song", back_populates="group")


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    is_validated = Column(Boolean, default=False, nullable=False)

    # Relationship to group
    group = relationship("Group", back_populates="songs")
    # Relationship to quotes
    quotes = relationship("Quote", back_populates="song")


class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    text = Column(String(255), unique=True, nullable=False)
    is_validated = Column(Boolean, default=False, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    dislikes = Column(Integer, default=0, nullable=False)
    # Relationships to song and rating
    song = relationship("Song", back_populates="quotes")
