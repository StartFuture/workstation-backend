import re
from flask_restful import Resource, reqparse
import defs_workstation as function
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from . import dao as Bank

from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt



class User(Resource):
    
    def __init__(self, name, lastname, birthday, sex, phone, email, password, identity):
        
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.sex = sex
        self.phone = phone
        self.email = email
        self.password = password
        self.identity = identity
        
    
class CreateUser(Resource):
    
    def post(self):  
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('nome')
        argumentos.add_argument('sobrenome')
        argumentos.add_argument('data_aniversario')
        argumentos.add_argument('sexo')
        argumentos.add_argument('telefone')
        argumentos.add_argument('email')
        argumentos.add_argument('senha')
        argumentos.add_argument('cpf_cnpj')
        
        dados = argumentos.parse_args()
        
        if Bank.DataBaseUser.verify_user_exist(dados['cpf_cnpj'], dados['email'], dados['telefone']):
        
            return {
                'msg': 'User alredy exist'
            }, 400
        
        else:
            user = User(dados['nome'], dados['sobrenome'], 
                        dados['data_aniversario'],dados['sexo'] ,dados['telefone'], 
                        dados['email'], generate_password_hash(dados['senha']),
                        dados['cpf_cnpj'])
            
            create = Bank.DataBaseUser.save_user(
                name=user.name,
                last_name=user.lastname,
                email=user.email,
                cellphone=user.phone,
                birthdate=user.birthday,
                password=user.password,
                identity=user.identity,
                sex=user.sex,
            )
            
            
            if create:
                return {'msg': 'User create'}, 200
            else:
                return {'msg': 'Db Problem'}, 400
        
        
        
class UserLogin(Resource):
    
    def post(self):
                
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('user_login')
        argumentos.add_argument('password_user')
        
        dados = argumentos.parse_args()
        
        user_login = dados['user_login']
        password_user = dados['password_user']
        
        is_email = function.check(user_login)
        
        if is_email:
            
            db_password, db_email = Bank.DataBaseUser.query_exist_email(user_login)
            
            if db_email and db_password:
                
                if check_password_hash(db_password, password_user):
                    id_user = Bank.DataBaseUser.get_user_id_by_email(email=user_login)
            
                    if id_user:

                        access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False})

                
                        return {
                            'access_token': access_token
                        }, 200
                    
                else:
                    
                    return {
                    'msg': 'incorrect email or password1'
                }, 400 

            else:
                
                return {
                    'msg': 'incorrect email or password2'
                }, 400

        else:
            
            is_cpf = function.is_cpf(dados['user_login'])
            
            if is_cpf:
                
                password, name, email = Bank.DataBaseUser.query_exist_cpf(dados['user_login'])
                
                if password and name and email:
                    
                    if check_password_hash(password, dados['password_user']):

                        id_user = Bank.DataBaseUser.get_user_id_by_email(email=email)
            
                        if id_user:
                            access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False})
                    
                            return {
                                'access_token': access_token
                            }, 200

                        
                    else:
                        
                        return {
                        'msg': 'incorrect email or password'
                                }, 400 
                        
                return {
                        'msg': 'incorrect email or password'
                                }, 400 
            else:
                
                password, name, email = Bank.DataBaseUser.query_exist_cnpj(dados['user_login'])
                
                if password and name and email:
                    if check_password_hash(password, dados['password_user']):
                        id_user = Bank.DataBaseUser.get_user_id_by_email(email=email)
            
                        if id_user:
                            access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False})
                    
                            return {
                                'access_token': access_token
                            }, 200
                        
                    else:
                        
                        return {
                        'msg': 'incorrect email or password'
                                }, 400 
                        
                return {
                        'msg': 'incorrect email or password'
                                }, 400
        
        
class TwoFactorLogin(Resource):
    
    @jwt_required()
    def get(self): #? maybe is supposed to be post
        two_auth = get_jwt()['two_auth']
        
        if two_auth: # verify if user has two factor authentication active
            return {
                'msg': 'Two factor already activated'
            }, 400
        

        else:
            # try:
            from random import randint
            
            cod = randint(111111, 9999999)
            cod_hash = generate_password_hash(str(cod))
            
            user_id = get_jwt_identity()
            
            email = Bank.DataBaseUser.get_email_id_by_user_id(user_id)
            
            logging.warning(f'cod: {cod}')
            # function.send_email(email, cod)
            
            if Bank.DataBaseUser.query_two_factor(user_id):
                Bank.DataBaseUser.delete_two_factor(user_id)
            
            Bank.DataBaseUser.insert_two_factor(user_id, cod_hash)
            
            return {
                'msg': 'Two factor code send to your email',
            }, 200
                
            # except Exception as e:
            #     logging.error(e)
            #     return {
            #         'msg': 'Error occurred while sending two factor email, try again'
            #     }, 400
    
    @jwt_required()
    def post(self):
        two_auth = get_jwt()['two_auth']
        
        if two_auth: # verify if user has two factor authentication active
            return {
                'msg': 'Two factor already activated'
            }, 400

        
        # try:
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('cod_user')
        
        dados = argumentos.parse_args()
        
        
        cod_user = function.convert_cod_int(dados['cod_user'])
        
        user_id = get_jwt_identity()
        
        cod = Bank.DataBaseUser.query_two_factor(user_id)
        
        if cod:
        
            if cod_user >= 111111 and cod_user <= 9999999:

                if check_password_hash(cod, str(cod_user)):
                    
                    
                    access_token = create_access_token(identity=user_id, additional_claims={'two_auth': True})

                    return {
                        'access_token': access_token
                    }                    
                    
                else: # wrong code
                    return{
                        'msg': 'Invalid code'
                    }, 400
                    
            else: # if code is not between 111111 and 9999999
                return {
                    'msg': 'Invalid code'
                }, 400
        
        else: # if cod is not in database
            return {
                'msg': 'Code Expired'
            }, 400
                
        # except Exception as e:
        #     return {
        #             'msg': 'Error occurred while processing two factor code, try again'
        #         }, 400
            
class Recover_Password_Email(Resource):
    
    def post(self):
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument("email")
        
        dados = argumentos.parse_args()
        
        email_user = dados['email']
        
        if Bank.DataBaseUser.query_exist_email(email_user):
            global cod2 
            from random import randint
            cod2 = randint(111111, 9999999)
            function.send_email(email_user, cod)
            return {
                "msg": "send code",
                "email": email_user
            }
            
    
class Recover_Password_Code(Resource):
    
    def post(self):
        argumentos = reqparse.RequestParser()

        argumentos.add_argument("cod_user_recover")
        argumentos.add_argument("email_user")

        dados = argumentos.parse_args()

        cod_user_recover = dados['cod_user_recover']
        if cod_user_recover == cod2:
            email_user = dados['email_user']


            return {
                "msg": "sucessfull",
                "email": email_user
            }
    
class NewPassword(Resource):
    
    def post(self):
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument("nova_senha")
        argumentos.add_argument("email_user")
        
        dados = argumentos.parse_args()
        
        new_password = dados['nova_senha']
        email_user = dados['email_user']
        
        id_user = Bank.DataBaseUser.get_user_id_by_email(email_user)
        
        
        Bank.DataBaseUser.new_password(id_user, generate_password_hash(new_password))