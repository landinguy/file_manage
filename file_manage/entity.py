from sqlalchemy import Column, String, Integer, Text, SmallInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:root@localhost/file_manage')
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(20))
    role = Column(String(20))


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    uid = Column(Integer)
    size = Column(Integer)
    create_ts = Column(String(20))
    content = Column(String(40))
    encryption_type = Column(SmallInteger)
    private_key = Column(Text)


class FidUid(Base):
    __tablename__ = 'fid_uid'

    fid = Column(Integer, primary_key=True)
    uid = Column(Integer, primary_key=True)

# 创建所有表
# def create_table():
#     Base.metadata.create_all(engine)

# if __name__ == '__main__':
#     create_table()
