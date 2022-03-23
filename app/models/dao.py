import mysql.connector
import defs_workstation as Function
import logging
import os
import re
from dotenv import load_dotenv

load_dotenv()
NAME = os.environ.get("NAME")
PASSWORD = ""
NAME_DB = os.environ.get("NAME_DB")
HOST = os.environ.get("HOST")

class DataBase:
    
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
    def __enter__(self):
        try:
            self.db = mysql.connector.connect(user=self.user, password=self.password,
                                        host=self.host, database=self.database)
            self.cursor = self.db.cursor(dictionary=True)
        except Exception as erro:
            print(erro)
        else:
            return self.cursor

    def __exit__(self, *args):
        try:
            self.db.commit()
            self.db.close()
        except Exception as erro:
            print(erro)
            
class DataBaseUser:        
    
    def search_by_cpf_or_email(cpf, email):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query_search = f"""
                select * from usuarios
                where cpf = '{cpf}' 
                or 
                email = '{email}';
                """
                cursor.execute(query_search)
                if cursor.fetchone():
                    return True
                return False
        
            
    def verify_user_exist(cpf, email, telefone):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query_search = f"""
                SELECT email, cpf, telefone
                FROM usuarios
                LEFT JOIN info_user_cpf
                ON usuarios.id_user = info_user_cpf.id_user
                where cpf = '{cpf}' or email = '{email}' or telefone = '{telefone}';  
                """
                cursor.execute(query_search)
                if cursor.fetchone():
                    return True
                return False
    
    
    def get_user_id_by_email(email):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                               select id_user from usuarios where email = '{email}';
                               """
                
                cursor.execute(query)
                
                value = cursor.fetchone()

                if value:
                    
                    value = value['id_user']
                else:
                    value = None
                    
                return value

    def save_user_infos(name, last_name, email, cellphone, birthdate, sex, password):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query_user = f"""
                insert into usuarios
                values 
                (default,'{name}', '{last_name}', '{sex}','{birthdate}', '{cellphone}','{email}', '{password}');
                """
                try:
                    cursor.execute(query_user)
                except Exception as erro:
                    logging.error(erro)
    
    def save_user_identification(id_user, identity):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if len(identity) == 11 or re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", identity):
                query_identity = f"""
                insert into info_user_cpf(cpf, id_user)
                values
                ('{identity}', '{id_user}')
                """
            elif len(identity) == 14 or re.match(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$", identity):
                query_identity = f"""
                insert into info_user_cnpj(cnpj, id_user)
                values
                ('{identity}', '{id_user}')
                """
                print('cnpj')
                
            else:
                raise Exception('error in identity')
            
            cursor.execute(query_identity)
                


    def save_user(name, last_name, email, cellphone, birthdate, password, identity, sex):
        # Save Basic infos
        try:
            DataBaseUser.save_user_infos(name, last_name, email, cellphone, birthdate, sex, password)
        except Exception as erro:
            return False
        else:
            # Get id_user
            id_user = DataBaseUser.get_user_id_by_email(email)
            print(id_user)
            # Save identification
            DataBaseUser.save_user_identification(id_user, identity)
            return True

    def search_pj(cnpj, email):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                select * from usuarios 
                where cpf = '{cnpj}' or email = '{email}';
                """
                cursor.execute(query)
                if cursor.fetchall():
                    return True
                return False


    def save_user_pj(name, sobrenome, telefone, email, cnpj, data_nasc, senha):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query =f"""
                insert into usuarios 
                values (default, '{name}','{sobrenome}',
                '{cnpj}', '{data_nasc}', '{telefone}',
                '{email}', '{senha}');
                """
                cursor.execute(query)
                


    def query_exist_email(email):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                select * from usuarios 
                where email = '{email}'
                """
                cursor.execute(query)
                if not (list_user := cursor.fetchall()):
                    return None, None
                for info in list_user:
                    password = info['senha']
                    name = info['email']
                    return password, name


    def query_exist_cpf(cpf):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query_ = f"""
                select * from info_user_cpf
                where cpf = '{cpf}'
                """
                cursor.execute(query)
                cpf = cursor.fetchall()
                if cpf:
                    for value in cpf:
                        id_user = value['id_user']

                    cursor.execute(f"""select * from usuarios where id_user = '{id_user}' """)
                    values = cursor.fetchall()
                    for value in values:
                        senha = value['senha']
                        nome = value['nome']
                        email = value['email']
                    return senha, nome, email 

    def query_exist_cnpj(cnpj):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""select * from info_user_cnpj where cnpj = '{cnpj}'""")
                cnpj = cursor.fetchall()
                if cnpj:
                    for value in cnpj:
                        id_user = value['id_user']

                    cursor.execute(f"""select * from usuarios where id_user = '{id_user}' """)
                    values = cursor.fetchall()
                    for value in values:
                        senha = value['senha']
                        nome = value['nome']
                        email = value['email']
                    return senha, nome, email

    def delete_user(id_user):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""
                delete from usuarios where id_user = '{id_user}';               
                """)


    def update_user(id_user, new_name, new_lastname, new_cpf, new_birth_date, new_cell, new_email):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""
                update usuarios set nome = '{new_name}', sobrenome = '{new_lastname}', cpf = '{new_cpf}',
                data_nascimento = '{new_birth_date}', telefone = '{new_cell}', email = '{new_email}'
                where id_user = '{id_user}';        
                """)
            

    def new_password(id_user, newpassword):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                update usuarios 
                set senha = '{newpassword}' 
                where id_user = '{id_user}';
                """
                cursor.execute(query)
                

class DataBaseBox:

    def verify_scheduling(start_date, start_hour, final_hour, final_date, id_box):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)

        if db and cursor:
            cursor.execute(f"""select * from locacao
    where {start_date} >= datainicio and {final_date} <= datafim 
    and {start_hour} >= horainicio or {final_hour} <= horafim
    and id_box = '{id_box}';""")
        if cursor:
            return not cursor.fetchall()


    def save_scheduling(start_date, start_hour, final_hour, final_date, id_user, id_box):

        start_date, final_date = Function.date_conversor(start_date, final_date)

        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)

        if db and cursor:
            cursor.execute(f"""insert into locacao 
            values (default, {start_date},{start_hour},{final_hour},{final_date},{id_user},{id_box});""")


    def show_all_scheduling():
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute('select * from locacao')
            return cursor.fetchall()
        return False


    def show_scheduling_box(id_box):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"select * from locacao where id_box = '{id_box}'")
            return cursor.fetchall()
        return False


    def show_scheduling_user(id_user):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f'select * from locacao where id_user = "{id_user}"')
            return cursor.fetchall()
        return False


    def delete_scheduling(id_scheduling):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""
            delete from locacao where id_locacao = '{id_scheduling}'         
            """)
            db.commit()
            db.close()


    def update_scheduling(id_scheduling, new_start_date, new_start_hour, new_final_hour, new_final_date):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""
            update locacao set datainicio = '{new_start_date}', horainicio = '{new_start_hour}',
            horafim = '{new_final_hour}', datafim = '{new_final_date}' where id_locaco = '{id_scheduling}';
            """)
            db.commit()
            db.close()


    
        
        
    def add_box(id_address, name, size, price_hour, description, activated='Y'):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""
            insert into usuarios values 
            (default, {id_address}, {name}, {size}, {price_hour}, {description}, {activated})               
            """)
            db.commit()
            db.close()
            

    def ativate_box(id_box):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""
            update box set ativo = 'Y' where id_box = '{id_box}'
            """)
            db.commit()
            db.close()
        

    def desativate_box(id_box):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""
            update box set ativo = 'N' where id_box = '{id_box}'
            """)
            db.commit()
            db.close()


    def update_box(id_box, id_address, name, size, price_hour, description, activated='Y'):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""update box 
            set id_endereco = '{id_address}', nome = '{name}', tamanho = '{size}',
            preco_hora = '{price_hour}', descricao = '{description}', ativo = '{activated}'
            where id_box = '{id_box}'""")
            db.commit()
            db.close()


    def add_address(cep, street, number, complement, district, city, state):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""insert into endereco values (default, '{cep}', '{street}', '{number}',
            '{complement}', '{district}', '{city}', '{state}')""")
            db.commit()
            db.close()


    def delete_address(id_address):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""
            delete from usuarios where id_locacao = '{id_address}';               
            """)
            db.commit()
            db.close()


    def update_address(id_address, cep, street, number, complement, district, city, state):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""update endereco set cep = '{cep}', rua = '{street}', numero = '{number}',
            complemento = '{complement}', bairro = '{district}', cidade = '{city}', estado = '{state}'
            where id_endereco = '{id_address}';
            """)
            db.commit()
            db.close()


    def add_furniture(name):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""insert into tipo_mobilia values (default, '{name}');""")
            db.commit()
            db.close()


    def delete_furniture(id_fourniture):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""delete from tipo_mobilia where id_mobilia = '{id_fourniture}';""")
            db.commit()
            db.close()


    def update_furniture(id_fourniture, new_name):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""update tipo_mobilia ser nome = '{new_name}' 
            where id_mobilia = '{id_fourniture}';""")
            db.commit()
            db.close()


    def add_resource(name):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""insert into tipo_recurso values (default, '{name}');""")
            db.commit()
            db.close()



    def delete_resource(id_resource):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""delete from tipo_recurso where id_recurso = '{id_resource}';""")
            db.commit()
            db.close()


    def update_resource(id_resource, new_name):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
            cursor.execute(f"""update tipo_recurso ser nome = '{new_name}' 
            where id_recurso = '{id_resource}';""")
            db.commit()
            db.close()


    def extra_hour(user_date_scheduling_id, how_many_hours):
        db, cursor = open_db(NAME, PASSWORD, HOST, NAME_DB)
        if db and cursor:
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



DataBaseUser.get_user_id_by_email('mateustoni04@gmail.com')

# select id_user from usuarios where email = 'mateustoni04@gmail.com';