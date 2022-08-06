import re
import logging
from datetime import timedelta

from flask_restful import Resource, reqparse
import defs_workstation as function
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from . import dao as Bank

from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, verify_jwt_in_request

import parameters


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
            # logging.warning()
            
            # function.send_email(email, layout_email = parameters.CONTENT_EMAIL_CODE_TEMPLATE.format(cod=cod)))
            
            
            if Bank.DataBaseUser.query_two_factor(user_id, type_code=parameters.ID_CODE_TWO_FACTOR):
                Bank.DataBaseUser.delete_two_factor(user_id, type_code=parameters.ID_CODE_TWO_FACTOR)
            
            Bank.DataBaseUser.insert_two_factor(user_id, cod_hash, type_code=parameters.ID_CODE_TWO_FACTOR)
            
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
        
        cod = Bank.DataBaseUser.query_two_factor(user_id, type_code=parameters.ID_CODE_TWO_FACTOR)
        
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
            
class Recover_Password_Request_Email(Resource):
    
    def post(self):
        
        if verify_jwt_in_request(optional=True):
            return {
                'msg': 'You already have a token'
            }
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument("email")
        
        dados = argumentos.parse_args()
        
        email_user = dados['email']
        
        if Bank.DataBaseUser.query_exist_email(email_user):
            
            
            user_id = Bank.DataBaseUser.get_user_id_by_email(email_user)
            
            if Bank.DataBaseUser.query_two_factor(user_id, type_code=parameters.ID_CODE_RESET_PASSWORD):
                Bank.DataBaseUser.delete_two_factor(user_id, type_code=parameters.ID_CODE_RESET_PASSWORD)
            
            token = create_access_token(identity=user_id, additional_claims={'recover_passwd': True})
            
            url_reset_password = f'{parameters.URL_FRONTEND}/reset_password?token={token}'
            
            print(token)
            
            # function.send_email(email_user, layout_email = parameters.CONTENT_EMAIL_RECOVER_PASSWORD.format(token=token))
            
            return {
                "msg": "Email to reset password sent"
            }
            
    
class Recover_Password(Resource):
    #? front end is supposed to receive and process the jwt token
    
    @jwt_required()
    def post(self):
        
        jwt_data = get_jwt()
        
        if 'recover_passwd' not in jwt_data:
            return {
                'msg': 'Your Token is not for this operation'
            }

        elif not jwt_data['recover_passwd']:
            return {
                'msg': 'Your Token is not for this operation'
            }   
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('password', type=str, required=True)

        dados = argumentos.parse_args()
        
        password = dados['password']
        
        if len(password) >= 6:
            
            password_hash = generate_password_hash(password)
            user_id = get_jwt_identity()
            
            #? Before reset password, revoke the token
            
            Bank.DataBaseUser.new_password(user_id, password_hash)
            
        
            return {
                'msg': 'Password changed'
            }, 200
        
        else: # if cod is not in database
            return {
                'msg': 'Password must be at least 6 characters'
            }, 400