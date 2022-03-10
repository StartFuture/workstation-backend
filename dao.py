import mysql.connector
import defs_workstation as Function

NAME = 'root'
PASSWORD = ''
NAME_DB = 'workstation'
HOST = 'localhost'


def open_db(user, password, host, database):
    try:
        db = mysql.connector.connect(user=user, password=password,
                                     host=host, database=database)
        cursor = db.cursor(dictionary=True)
    except:
        return None, None
    else:
        return db, cursor


def search(cpf, email):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(
            f"""select * from usuario where cpf = '{cpf}' or email = '{email}'""")
        if has := cursor.fetchall():
            return True
        return False
    db.close()


def save_user(name, sobrenome, email, cpf, telefone, data_nasc, senha):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""insert into usuarios 
        values (default, '{name}','{sobrenome}','{cpf}', '{data_nasc}', '{telefone}','{email}', '{senha}');""")
        db.commit()
        db.close()


def search_pj(cnpj, email):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(
            f"""select * from usuario where cpf = '{cnpj}' or email = '{email}';""")
        if has := cursor.fetchall():
            return True
        return False
    db.close()


def save_user_pj(name, sobrenome, telefone, email, cnpj, data_nasc, senha):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""insert into usuarios 
        values (default, '{name}','{sobrenome}','{cnpj}', '{data_nasc}', '{telefone}','{email}', '{senha}');""")
        db.commit()
        db.close()


def query_exist_email(email):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""select * from usuario where email = '{email}'""")
        if not (list_user := cursor.fetchall()):
            return None, None
        for info in list_user:
            password = info['senha']
            name = info['nome']
            return password, name


def query_exist_cpf(cpf):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""select * from usuario where cpf = '{cpf}'""")
        if not (list_user := cursor.fetchall()):
            return None, None
        for info in list_user:
            password = info['senha']
            name = info['nome']
            email = info['email']
            return password, name, email


def query_exist_cnpj(cnpj):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""select * from usuario where cnpj = '{cnpj}'""")
        if not (list_user := cursor.fetchall()):
            return None, None
        for info in list_user:
            password = info['senha']
            name = info['nome']
            email = info['email']
            return password, name, email


def verify_scheduling(start_date, start_hour, final_hour, final_date, id_box):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)

    if db:
        cursor.execute(f"""so elect * from locaca
where {start_date} >= datainicio and {final_date} <= datafim 
and {start_hour} >= horainicio or {final_hour} <= horafim
and id_box = '{id_box}';""")
    return not cursor.fetchall()


def save_scheduling(start_date, start_hour, final_hour, final_date, id_user, id_box):

    start_date, final_date = Function.date_conversor(start_date, final_date)

    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)

    if db:
        cursor.execute(f"""insert into locacao 
        values (default, {start_date},{start_hour},{final_hour},{final_date},{id_user},{id_box});""")


def show_all_scheduling():
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute('select * from locacao')
        return cursor.fetchall()
    return False


def show_scheduling_box(id_box):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"select * from locacao where id_box = '{id_box}'")
        return cursor.fetchall()
    return False


def show_scheduling_user(id_user):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f'select * from locacao where id_user = "{id_user}"')
        return cursor.fetchall()
    return False


def delete_scheduling(id_scheduling):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        delete from locacao where id_locacao = '{id_scheduling}'         
        """)
        db.commit()
        db.close()


def update_scheduling(id_scheduling, new_start_date, new_start_hour, new_final_hour, new_final_date):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        update locacao set datainicio = '{new_start_date}', horainicio = '{new_start_hour}',
        horafim = '{new_final_hour}', datafim = '{new_final_date}' where id_locaco = '{id_scheduling}';
        """)
        db.commit()
        db.close()


def delete_user(id_user):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        delete from usuario where id_user = '{id_user}';               
        """)
        db.commit()
        db.close()


def update_user(id_user, new_name, new_lastname, new_cpf, new_birth_date, new_cell, new_email):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        update usuario set nome = '{new_name}', sobrenome = '{new_lastname}', cpf = '{new_cpf}',
        data_nascimento = '{new_birth_date}', telefone = '{new_cell}', email = '{new_email}'
        where id_user = '{id_user}';        
        """)
        db.commit()
        db.close()
        

def new_password(id_user, newpassword):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""update usuario set senha = '{newpassword}' where id_user = '{id_user}';""")
        db.commit()
        db.close()
    
    
def add_box(id_address, name, size, price_hour, description, activated='Y'):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        insert into usuario values 
        (default, {id_address}, {name}, {size}, {price_hour}, {description}, {activated})               
        """)
        db.commit()
        db.close()
        

def ativate_box(id_box):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        update box set ativo = 'Y' where id_box = '{id_box}'
        """)
        db.commit()
        db.close()
    

def desativate_box(id_box):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        update box set ativo = 'N' where id_box = '{id_box}'
        """)
        db.commit()
        db.close()


def update_box(id_box, id_address, name, size, price_hour, description, activated='Y'):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""update box 
        set id_endereco = '{id_address}', nome = '{name}', tamanho = '{size}',
        preco_hora = '{price_hour}', descricao = '{description}', ativo = '{activated}'
        where id_box = '{id_box}'""")
        db.commit()
        db.close()


def add_address(cep, street, number, complement, district, city, state):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""insert into endereco values (default, '{cep}', '{street}', '{number}',
        '{complement}', '{district}', '{city}', '{state}')""")
        db.commit()
        db.close()


def delete_address(id_address):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""
        delete from usuario where id_locacao = '{id_address}';               
        """)
        db.commit()
        db.close()


def update_address(id_address, cep, street, number, complement, district, city, state):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""update endereco set cep = '{cep}', rua = '{street}', numero = '{number}',
        complemento = '{complement}', bairro = '{district}', cidade = '{city}', estado = '{state}'
        where id_endereco = '{id_address}';
        """)
        db.commit()
        db.close()


def add_furniture(name):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""insert into tipo_mobilia values (default, '{name}');""")
        db.commit()
        db.close()


def delete_furniture(id_fourniture):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""delete from tipo_mobilia where id_mobilia = '{id_fourniture}';""")
        db.commit()
        db.close()


def update_furniture(id_fourniture, new_name):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""update tipo_mobilia ser nome = '{new_name}' 
        where id_mobilia = '{id_fourniture}';""")
        db.commit()
        db.close()


def add_resource(name):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""insert into tipo_recurso values (default, '{name}');""")
        db.commit()
        db.close()



def delete_resource(id_resource):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""delete from tipo_recurso where id_recurso = '{id_resource}';""")
        db.commit()
        db.close()


def update_resource(id_resource, new_name):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""update tipo_recurso ser nome = '{new_name}' 
        where id_recurso = '{id_resource}';""")
        db.commit()
        db.close()


def extra_hour(user_date_scheduling_id, how_many_hours):
    db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
    if db:
        cursor.execute(f"""select * from locacao 
        where id_locacao = '{user_date_scheduling_id}';""")
        list_location = cursor.fetchall()
        for dict_location in list_location:
            start_date = dict_location['datainicio']
            start_hour = dict_location['horainicio']
            final_hour = dict_location['horafim']
            final_date = dict_location['datafim']
            cursor.execute(f"""select * from locacao 
            where {start_date} >= datainicio and {final_date} <= datafim 
            and {start_hour} >= horainicio or {final_hour} <= horafim;""")
            list_location = cursor.fetchall()
            if len(list_location) >= 2:
                return False
            dict_location['horafim'] += how_many_hours
            cursor.execute(f"""update locacao set horafim = '{dict_location['horafim']}'
            where id_locacao = '{user_date_scheduling_id}';""")
            db.commit()
            db.close()
            return True
