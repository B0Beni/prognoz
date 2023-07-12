# db_session.py - cоздание базы данных и сесии по работе с ней
# FileField
# Если из формы добавлен файл, то обюращаться к нему при обработке формы следует так: f.form.<название поля с файлом
# ORM - Object Relationship Mapping
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = orm.declarative_base()

created = None  #  создана ли сессия

def global_init(db_file):
    global created

    if created:
        return
# выше, если бд была создана выходимю если нет создаем

    if not db_file or not db_file.strip():   # убрали пробелы
        raise Exception("Забыли подключить файл базы!")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'  # проверка использования потока данных

    print(f'Мы подключились к базе данных для отладки: {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    created = orm.sessionmaker(bind=engine)

    from . import  all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global created
    return created







