from sqlalchemy import create_engine, text, insert
from dotenv.main import load_dotenv
from itertools import groupby
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
    
def get_num_persons_of_districts():
    with engine.connect() as conn:
        data = conn.execute(text("select addr1, addr2,count(*) from family,person where family.id=person.family_id group by addr1, addr2")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        # print(res)
        return res
    
def get_num_persons_of_provinces():
    with engine.connect() as conn:
        data = conn.execute(text("select addr1,count(*) from family,person where family.id=person.family_id group by addr1")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        print(res)
        return res

def get_num_persons_of_family():
    with engine.connect() as conn:
        data = conn.execute(text("select hhsize,count(*) from family group by hhsize")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        print(res)
        return res

def get_age_groups():
    with engine.connect() as conn:
        data = conn.execute(text("select case when (YEAR(NOW()) - birth_year) >= 0 and (YEAR(NOW()) - birth_year) <= 1 then '0-1 tuổi' when (YEAR(NOW()) - birth_year) > 1 and (YEAR(NOW()) - birth_year) <= 12 then '1-12 tuổi' when (YEAR(NOW()) - birth_year) > 12 and (YEAR(NOW()) - birth_year) <= 17 then '12-17 tuổi' when (YEAR(NOW()) - birth_year) > 17 and (YEAR(NOW()) - birth_year) <= 65 then '17-65 tuổi' else 'trên 65 tuổi' end as age_group, count(*) as count from family,person where family.id=person.family_id group by age_group; ")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        print(res)
        return res

def get_gender():
    with engine.connect() as conn:
        data = conn.execute(text("select gender,count(*) from person group by gender")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        # print(users)
        return res

def get_occupation():
    with engine.connect() as conn:
        data = conn.execute(text("select occupation,count(*) from person group by occupation")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        # print(users)
        return res

def get_population():
    with engine.connect() as conn:
        data = conn.execute(text("select id,family_id,gender,(YEAR(NOW()) - birth_year) as age from person order by id")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))
        print(res)
        return res
    
def key_func(k):
    return k['family_id']

def get_household():
    with engine.connect() as conn:
        data = conn.execute(text("select p.family_id, p.id from person p where p.in_house = 1 order by family_id")).all()
        res = []
        # print(data[0].__getitem__(0))
        for row in data:
            res.append(row2dict(row))

        hh_dict = {}
        for key, value in groupby(res, key_func):
            hh_dict[key - 1] =  [item['id'] - 1 for item in list(value)]

        print(hh_dict)
        return hh_dict

def add_family_person(data):
    with engine.connect() as conn:
        insert_family_query = text("insert into family(hhsize, addr1,addr2,addr3) values (:hhsize, :addr1, :addr2, :addr3)")
        get_last_id_query = text("SELECT LAST_INSERT_ID()")
        insert_person_query = text("INSERT INTO person (family_id, birth_year, gender, occupation, p_addr1, p_addr2, p_addr3, in_house) VALUES (:famID, :birth_year, :gender, :occupation, :p_addr1, :p_addr2, :p_addr3, :in_house)")

        hhsize = data['household-size']
        addr = data['family-addr']
        addr_list = addr.strip().split(',')
        addr1 = addr_list[0]
        addr2 = addr_list[1]
        addr3 = addr_list[2]
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

            p_addr = data[f"addr_{i}"]
            p_addr_list = p_addr.strip().split(',')
            p_addr1 = p_addr_list[0]
            p_addr2 = p_addr_list[1]
            p_addr3 = p_addr_list[2]
            if p_addr1 == addr1 and p_addr2 == addr2 and p_addr3 == addr3:
                in_house = 1
            else:
                in_house = 0
            conn.execute(insert_person_query,
                        [
                            {"famID": last_id, 
                             "birth_year": birth_year, 
                             "gender":gender, 
                             "occupation": occupation,
                             "p_addr1": p_addr1,
                             "p_addr2": p_addr2,
                             "p_addr3": p_addr3,
                             "in_house": in_house}
                        ])
        conn.commit()

# get_all_families()
# get_all_persons()
# get_all_families()
# get_population()

    