from flask_restful import Resource, reqparse
from . import dao as Bank


class GenerateSchedule(Resource):
    
    def post(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('data_inicio')
        argumentos.add_argument('hora_inicio')
        argumentos.add_argument('hora_fim')
        argumentos.add_argument('data_fim')
        argumentos.add_argument('id_box')
        argumentos.add_argument('id_user')
        
        dados = argumentos.parse_args()
    
        available = Bank.Scheduling.verify_scheduling(start_date=dados['data_inicio'],
                                                   id_box=dados['id_box'],
                                                   final_date=dados['data_fim'],
                                                   start_hour=dados['hora_inicio'],
                                                   final_hour=dados['hora_fim'])
        if available:
            Bank.Scheduling.save_scheduling(dados['data_inicio'],
                                            dados['hora_inicio'],
                                            dados['hora_fim'],
                                            dados['data_fim'],
                                            dados['id_user'],
                                            dados['id_box'])
            return {
                "msg": "sucessfull"
            }
        else:
            return {
                "msg": "agendamento indispinível"
            }
            

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
            
            