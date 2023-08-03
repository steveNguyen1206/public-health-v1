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

def get_all_persons():
    with engine.connect() as conn:
        data = conn.execute(text("select * from person")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        # print(users)
        return res
    
def get_all_families():
    with engine.connect() as conn:
        data = conn.execute(text("select * from family")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        print(res)
        return res
    
def get_dist_person_num(dist):
    with engine.connect() as conn:
        query = text("select addr2, count(*) from family f, person p where f.id = p.family_id and f.addr2 = :dist")
        data = conn.execute(query,
                            [{"dist": dist}]).all()
        res = []
        for row in data:
            res.append(row2dict(row))
        print(res)
        return res

def add_family_person(data):
    with engine.connect() as conn:
        insert_family_query = text("insert into family(hhsize, addr1,addr2,addr3) values (:hhsize, :addr1, :addr2, :addr3)")
        get_last_id_query = text("SELECT LAST_INSERT_ID()")
        insert_person_query = text("INSERT INTO person (family_id, birth_year, gender, occupation) VALUES (:famID, :birth_year, :gender, :occupation)")

        hhsize = data['household-size']
        addr1 = data['province']
        addr2 = data['district']
        addr3 = data['wards']
        conn.execute(insert_family_query, 
                     [
                         {"hhsize": hhsize, "addr1": addr1, "addr2": addr2, "addr3": addr3}
                     ])

        last_id = conn.execute(get_last_id_query).all()[0].__getitem__(0)
        print(last_id)
        for i in range (1, int(hhsize)+1):
            gender = data[f"gender_{i}"]
            birth_year = data[f"birth-year_{i}"]
            occupation = data[f"occupation_{i}"]
            conn.execute(insert_person_query,
                        [
                            {"famID": last_id, "birth_year": birth_year, "gender":gender, "occupation": occupation}
                        ])
        conn.commit()

# get_all_families()

    