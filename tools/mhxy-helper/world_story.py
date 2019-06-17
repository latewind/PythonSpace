# 导入:
from sqlalchemy import Column, String, create_engine, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
# 初始化数据库连接:
# engine = create_engine('sqlite:///D:\\PythonSpace\\tools\\mhxy-helper\\helper.db')
engine = create_engine('sqlite:///helper.db')


# 定义User对象:
class WorldStoryQuestion(Base):
    # 表的名字:
    __tablename__ = 'world_story_question'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    question = Column(String(20))
    choices = relationship("WorldStoryAnswer")


# 定义User对象:
class WorldStoryAnswer(Base):
    # 表的名字:
    __tablename__ = 'world_story_answer'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    choice = Column(String(20))
    question_id = Column(Integer, ForeignKey('world_story_question.id'))


Base.metadata.create_all(engine)

# engine是2.2中创建的连接
Session = sessionmaker(bind=engine)

# 创建Session类实例
session = Session()

query = session.query(WorldStoryQuestion).filter(WorldStoryQuestion.question.like('%箍棒是谁锻造的%')).first()


def save_data():
    a = WorldStoryAnswer(id=18, choice='唐僧', question_id=13)
    q = WorldStoryQuestion(id=13, question="寻找3个天命取经人,", choices=[a, ])
    session.add(q)
    session.commit()


def import_data():
    # save_data()
    q_start_index = 12
    a_start_index = 17

    with open('res/world_story.txt', encoding='utf-8') as f:
        for line in f.readlines():
            print(line)
            line = line.replace('\t', ' ').strip('\n').replace('、', ' ').replace('？', '')
            l = line.split(' ')
            q_start_index = q_start_index + 1
            print(l)
            print(l[0])
            c = []

            for a in l[1:]:
                a_start_index = a_start_index + 1
                print(a)
                choice = WorldStoryAnswer(id=a_start_index, choice=a, question_id=q_start_index)
                c.append(choice)
            q = WorldStoryQuestion(id=q_start_index, question=l[0], choices=c)
            session.add(q)
            session.commit()
        print(q_start_index)
        print(a_start_index)


def query_world_story(question):
    return session.query(WorldStoryQuestion).filter(WorldStoryQuestion.question.like(question)).first()
