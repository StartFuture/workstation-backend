import mysql.connector
import defs_workstation as Function
import logging
import os
import re
from parameters import NAME, PASSWORD, HOST, NAME_DB

class DataBase:
    
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
    def __enter__(self):
        try:
            self.db = mysql.connector.connect(user=self.user, password=self.password,
                                        host=self.host)
            self.cursor = self.db.cursor(dictionary=True)
            self.cursor.execute(f'use {self.database}')
        except Exception as erro:
            logging.critical(erro)
        else:
            return self.cursor

    def __exit__(self, *args):
        try:
            self.db.commit()
            self.db.close()
        except Exception as erro:
            logging.critical(erro)
            
class DataBaseUser:                
            
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
    
    def get_user_info(user_id):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                select usuarios.id_user as id, info_user_cpf.cpf, nome, sobrenome, sexo, data_nascimento, telefone, email from usuarios
                left join info_user_cpf
                on info_user_cpf.id_user = usuarios.id_user
                where usuarios.id_user = {user_id};
                """
                cursor.execute(query)
                return cursor.fetchone()
    
    def get_email_id_by_user_id(user_id):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                            select email from usuarios where id_user = '{user_id}';
                            """
                
                cursor.execute(query)
                
                value = cursor.fetchone()

                if value:
                    
                    value = value['email']
                else:
                    value = None
                    
                return value

    def save_user_infos(name, last_name, email, cellphone, birthdate, sex, password):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query_user = f"""
                insert into usuarios(nome,sobrenome,sexo,data_nascimento,telefone,email,senha)
                values 
                ('{name}', '{last_name}', '{sex}','{birthdate}', '{cellphone}','{email}', '{password}');
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
            else:
                raise Exception('error in identity')
            
            cursor.execute(query_identity)
                

    def save_user(name, last_name, email, cellphone, birthdate, password, identity, sex):
        # Save Basic infos
        try:
            DataBaseUser.save_user_infos(name, last_name, email, cellphone, birthdate, sex, password)
        except Exception as erro:
            logging.critical(erro)
            return False
        else:
            # Get id_user
            id_user = DataBaseUser.get_user_id_by_email(email)
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
                
    def insert_two_factor(id_user, hash_code, type_code : int):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                insert into two_auth(id_user, cod_two_factor, type_code)
                values ({id_user}, '{hash_code}', {type_code});
                """
                cursor.execute(query)
    
    def delete_two_factor(id_user, type_code : int):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                delete from two_auth
                where
                id_user = {id_user}
                and
                type_code = {type_code};
                """
                cursor.execute(query)
    
    def query_two_factor(id_user, type_code : int):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                query = f"""
                select cod_two_factor as hash_code from two_auth
                where 
                id_user = {id_user}
                and
                TIME_TO_SEC((TIMEDIFF(now(), `date_register`))) <= 120
                and type_code = {type_code}
                order by date_register desc
                limit 1
                ;
                """
                cursor.execute(query)
                value = cursor.fetchone()
                if value:
                    return value['hash_code']
                else:
                    return None
                

class DataBaseBox:
    

    def get_name_box_by_id(id_box):
        
        query = f"""
        select nome from box 
        where id_box = '{id_box}';
        """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                values = cursor.fetchall()
                if values:
                    return values

    def show_all_boxes():
        query = """
        select * from box;
        """
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                values = cursor.fetchall()
                if values:
                    return values
        
    def add_box(id_address, name, price_hour, description, zone, width, heigth, depth, activated='Y'):
        query = f"""
        insert into box
        values(default, '{id_address}', '{name}', 
        '{price_hour}', '{description}',
        '{activated}', '{heigth}', '{width}', 
        '{depth}', '{zone}');
        """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
            

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

    def show_address():
        query = """
        select * from endereco;
        """
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                values = cursor.fetchall()
                if values:
                    return values
    
    def get_address_by_id(id_address):
        query = f"""
        select * from endereco 
        where id_endereco = '{id_address}';
        """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                values = cursor.fetchall()
                if values:
                    return values
        
                
    def get_id_address_by_cep(cep):
        query = f"""
        select id_endereco 
        from endereco 
        where cep = '{cep}';
        """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                values = cursor.fetchall()
                if values:
                    for value in values:
                        return value['id_endereco']
    

    def add_address(cep, street, number, complement, district, city, state):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""insert into endereco values (default, '{cep}', '{street}', '{number}',
                '{complement}', '{district}', '{city}', '{state}')""")


    def delete_address(id_address):
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""
                delete from usuarios where id_locacao = '{id_address}';               
                """)


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


class Scheduling():
    
    @staticmethod
    def get_id_scheduling_by_id_user(id_user):
        query = f"""
        select id_locacao from locacao 
        where id_user = '{id_user}';
        """

        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                id_scheduling = cursor.fech
    
    @staticmethod
    def verify_scheduling(start_date, start_hour, final_hour, final_date, id_box):
        query = f"""
                select * from locacao
                where {start_date} >= datainicio and {final_date} <= datafim 
                and {start_hour} >= horainicio or {final_hour} <= horafim
                and id_box = '{id_box}';
                """
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                schedule = cursor.fetchall()

                return not schedule
            
                

    @staticmethod
    def save_scheduling(start_date, start_hour, final_hour, final_date, id_user, id_box):

        start_date, final_date = Function.date_conversor(start_date, final_date)
        
        query = f"""insert into locacao 
                    values (default, {start_date},
                    {start_hour},{final_hour},
                    {final_date},{id_user},
                    {id_box});
                    """
                    
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                


    @staticmethod
    def show_all_scheduling():
        
        query = "select * from locacao;"
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
        
                return cursor.fetchall()
        

    @staticmethod
    def show_scheduling_box(id_box):
        
        query = f"""
        select * from locacao 
        where id_box = '{id_box}';
        """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                return cursor.fetchall()
        

    @staticmethod
    def show_scheduling_user(id_user):
        
        query = f'select * from locacao where id_user = "{id_user}"'
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def delete_scheduling(id_scheduling):
        
        query = f"""
                delete from locacao 
                where id_locacao = '{id_scheduling}';         
                """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
            

    @staticmethod
    def update_scheduling(id_scheduling, new_start_date, new_start_hour, new_final_hour, new_final_date):
        
        query = f"""
                update locacao set datainicio = '{new_start_date}', horainicio = '{new_start_hour}',
                horafim = '{new_final_hour}', datafim = '{new_final_date}' where id_locaco = '{id_scheduling}';
                """
        
        with DataBase(NAME, PASSWORD, HOST, NAME_DB) as cursor:
            if cursor:
                cursor.execute(query)
        
    

