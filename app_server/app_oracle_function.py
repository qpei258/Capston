import cx_Oracle

def commit():
    sql = 'commit'
    cursor.execute(sql)
    # o

def insert_user(id, pw, name, phone, gender, agency, admin):
    sql = "insert into users values (:1, :2, :3, label_seq.nextval, :4, :5, :6, :7)"
    cursor.execute(sql, (id, pw, name, phone, gender, agency, admin))
    # o



def entrance_records_return():
    sql = "select id, name, to_char(enterdate , 'YY/MM/DD hh24:mi:ss') from records"
    cursor.execute(sql)
    return cursor
# o

def select_count_records():
    sql = "select count(*) from records"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]
# o

def select_pw_where_id(id):
    sql = "select * from users where id = '" + id + "'"
    cursor.execute(sql)
    result = cursor.fetchone();
    return result
# o


def select_all_where_id(id):
    sql = "select * from users where id = '" + id + "'"
    cursor.execute(sql)
    result = cursor.fetchone();
    return result
# o


def update_where_id(name, phone, agency, id) :
    sql = "update users set name= :1, phone= :2, agency= :3 where id = :4"
    cursor.execute(sql, (name, phone, agency, id))
# o


dsn = cx_Oracle.makedsn("localhost", 1521)
db = cx_Oracle.connect("server", "1234", dsn)
cursor = db.cursor()

