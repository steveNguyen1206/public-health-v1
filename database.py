from sqlalchemy import create_engine, text, insert
from dotenv.main import load_dotenv
import os

load_dotenv()
db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)

def row2dict(row):
    d = {}
    fields = row._fields
    for i in range(len(fields)):
        d[fields[i]] = row.__getitem__(i)
    # print(d)
    return d

def get_all_users():
    with engine.connect() as conn:
        data = conn.execute(text("select * from user")).all()
        users = []
        # print(data[0].__getitem__(0))
        for row in data:
            users.append(row2dict(row))
        # print(users)
        return users
    
def get_num_of_district():
    with engine.connect() as conn:
        data = conn.execute(text("select * from user group by dictrict")).all()
        users = []
        # print(data[0].__getitem__(0))
        for row in data:
            users.append(row2dict(row))
        # print(users)
        return users

def add_user(user):
    with engine.connect() as conn:
        query = text("INSERT INTO user (name, email, age, gender) VALUES (:name, :email, :age, :gender)")
        conn.execute(query,
                    [{"name": user['name'], "email":user['email'], "age":user['age'], "gender":user['gender']}],
                    )
        conn.commit()
        # print(insert(user))

get_all_users()
    
