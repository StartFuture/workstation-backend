from flask_restful import Resource, reqparse
from . import dao as Bank

from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, verify_jwt_in_request

class GenerateSchedule(Resource):
    @jwt_required()
    def post(self):
        
        jwt_info = get_jwt()
        
        if 'two_auth' in jwt_info:
            if jwt_info['two_auth']:
                user_id = get_jwt_identity()

                argumentos = reqparse.RequestParser()
                
                argumentos.add_argument('date_schedule')

                argumentos.add_argument('array_schedule_times')

                argumentos.add_argument('id_box')
                
                dados = argumentos.parse_args()

                print(dados)
                print(user_id)
            
                return {
                    'msg': 'Schedule created'
                }, 200
            
            else:
                return {
                    'msg': 'Two auth is required'
                }, 400
                
        return {
            'msg': 'Two auth is required'
        }, 400

        
    
        # available = Bank.Scheduling.verify_scheduling(start_date=dados['data_inicio'],
        #                                            id_box=dados['id_box'],
        #                                            final_date=dados['data_fim'],
        #                                            start_hour=dados['hora_inicio'],
        #                                            final_hour=dados['hora_fim'])
        # if available:
        #     Bank.Scheduling.save_scheduling(dados['data_inicio'],
        #                                     dados['hora_inicio'],
        #                                     dados['hora_fim'],
        #                                     dados['data_fim'],
        #                                     dados['id_user'],
        #                                     dados['id_box'])
        #     return {
        #         "msg": "sucessfull"
        #     }
        # else:
        #     return {
        #         "msg": "agendamento indispinível"
        #     }
            

class ShowSchedule(Resource):
    
    def get(self):
        
        list_process_schedule = []
        infos = []
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('id_user')
        
        dados = argumentos.parse_args()
        
        schedule = Bank.Scheduling.show_scheduling_user(dados['id_user'])
        
        if schedule:
            for scheduling in schedule:
                
                name_box = Bank.DataBaseBox.get_name_box_by_id(scheduling['id_box'])
                address = Bank.DataBaseBox.get_address_by_id(scheduling['id_user'])
                
                list_process_schedule.append({
                    "datainicio": scheduling['datainicio'],
                    "datafim": scheduling['datafim'],
                    "horainicio": scheduling['horainicio'],
                    "horafim": scheduling['horafim'],
                    "nome_box": name_box,
                    "local_agendado": address
                }) 
                
            return list_process_schedule
    
class DeleteSchedule(Resource):
    
    def delete(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('id_locacao')
        
        dados = argumentos.parse_args()
        try:
            Bank.Scheduling.delete_scheduling(dados['id_locacao'])
        except Exception as erro:
            return erro
        else:
            return{
                "msg": "Sucessfull"
            }
    
class UpdateSchedule(Resource):
    
    def update(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('novo_data_inicio')
        argumentos.add_argument('novo_hora_inicio')
        argumentos.add_argument('novo_hora_fim')
        argumentos.add_argument('novo_data_fim')
        argumentos.add_argument('id_locacao')
        
        dados = argumentos.parse_args()
        
        available = Bank.Scheduling.verify_scheduling(start_date=dados['novo_data_inicio'],
                                                   id_box=dados['id_box'],
                                                   final_date=dados['novo_data_fim'],
                                                   start_hour=dados['novo_hora_inicio'],
                                                   final_hour=dados['novo_hora_fim'])
        if available:
            Bank.Scheduling.update_scheduling(id_scheduling=dados['id_locacao'],
                                              new_start_date=dados['novo_data_inicio'],
                                              new_final_date=dados['novo_data_fim'],
                                              new_final_hour=dados['novo_hora_fim'],
                                              new_start_hour=dados['novo_hora_inicio'])
        else:
            return {
                "msg": "alteração indisponível"
            }
            
            