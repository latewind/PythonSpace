# 导入:
from sqlalchemy import Column, String, create_engine, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
# 初始化数据库连接:
# engine = create_engine('sqlite:///D:\\PythonSpace\\tools\\mhxy-helper\\helper.db')
engine = create_engine('sqlite:///monster.db')

print('init')

# engine是2.2中创建的连接
Session = sessionmaker(bind=engine)

# 创建Session类实例
session = Session()


# 定义User对象:
class MonsterDropHistory(Base):
    # 表的名字:
    __tablename__ = 'monster_drop_history'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    monster_name = Column(String(20))
    map = Column(String(20))
    object_name = Column(String(20))
    info = Column(String(255))
    create_date = Column(DateTime)
    is_boss = Column(Boolean)


Base.metadata.create_all(engine)
