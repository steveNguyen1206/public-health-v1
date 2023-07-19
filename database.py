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
    for name in row._fields:
        d[name] = row.name
    return d

def get_all_users():
    with engine.connect() as conn:
        data = conn.execute(text("select * from user"))
        users = []
        for row in data.all():
            users.append(row2dict(row))
        # print(users)
        return users

def add_user(user):
    with engine.connect() as conn:
        query = text("INSERT INTO user (name, email, age) VALUES (:name, :email, :age)")
        conn.execute(query,
                    [{"name": user['name'], "email":user['email'], "age":user['age']}],
                    )
        conn.commit()
        # print(insert(user))

# add_user("")
    