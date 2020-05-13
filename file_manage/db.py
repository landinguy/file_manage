from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root@localhost/file_manage')
session = sessionmaker(bind=engine)()


def get_engine(): return create_engine('mysql+pymysql://root:root@localhost/file_manage')


def execute(sql): get_engine().connect().execute(sql)


def create_table():
    meta_data = MetaData(engine)

    # Table(
    #     'user', meta_data,
    #     Column('id', Integer, primary_key=True), Column('username', String(20)),
    #     Column('password', String(20)), Column('role', String(20))
    # )

    # Table(
    #     'file', meta_data,
    #     Column('id', Integer, primary_key=True), Column('name', String(20)),
    #     Column('uid', Integer), Column('size', Integer), Column('create_ts', String(20)),
    #     Column('content', String(60)), Column('encryption_type', SmallInteger), Column('private_key', Text),
    # )

    # Table(
    #     'fid_uid', meta_data,
    #     Column('fid', Integer, primary_key=True), Column('uid', Integer, primary_key=True)
    # )

    meta_data.create_all(engine)


def add(obj):
    session.add(obj)
    session.commit()


if __name__ == '__main__':
    create_table()
