from sqlalchemy import create_engine, insert
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, 
						String, DateTime, ForeignKey, create_engine)
from datetime import datetime
from pa91 import read_text_to_dict


if __name__ == '__main__':
    meta = MetaData()

    porn_91 = Table('porn_91', meta,
        Column('video_id', Integer(), primary_key=True, autoincrement=True),
        Column('video_title', String(50), nullable=False),
        Column('video_url', String(50), nullable=False, unique=True),
        Column('created_on', DateTime(), default=datetime.now),
    )

    engine = create_engine('sqlite:///sq')
    meta.create_all(engine)
    connection = engine.connect()

    items = read_text_to_dict()
    # print(items)
    # for i in items:
	   #  for k, v in i.items():
	   #  	print(k, v)
    ins = insert(porn_91)
    result = connection.execute(ins, items)
    print('finished')
