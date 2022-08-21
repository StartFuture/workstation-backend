import logging
from datetime import datetime, timedelta, time

from flask_restful import Resource, reqparse
from . import dao as Bank
import defs_workstation as function

from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, verify_jwt_in_request

class GenerateSchedule(Resource):
    @jwt_required()
    def post(self):
        
        jwt_info = get_jwt()
        
        if 'two_auth' in jwt_info:
            if jwt_info['two_auth']:
                user_id = get_jwt_identity()

                argumentos = reqparse.RequestParser()
                
                argumentos.add_argument('date_schedule', required=True)

                argumentos.add_argument('array_schedule_times', type=list, required=True)

                argumentos.add_argument('id_box', required=True)
                
                dados = argumentos.parse_args()
                
                date_processed = function.date_conversor(dados['date_schedule'])
                
                list_invalid_times = []

                for schedule in dados['array_schedule_times']: # iter and verify if each time is avaible

                    diff_time = datetime.strptime(f'{date_processed} {schedule[:2]}', '%Y-%m-%d %H') - datetime.now()

                    if diff_time.total_seconds() / 60 / 60 < 1.16: # seconds / 60 > minutes / 60 > hours 
                        
                        return {
                            "msg": f"Schedule time in past",
                            "msg_error_custom": f"Periodo Invalido, no minimo 1 hora a partir de agora",
                            "unavailable_times": list_invalid_times
                        }, 410
                    
                    available = Bank.Scheduling.verify_scheduling(
                                                                id_box=dados['id_box'],
                                                                start_date=date_processed,
                                                                final_date=date_processed,
                                                                start_hour=schedule,
                                                                final_hour=schedule
                                                                )
                    if not available:
                        list_invalid_times.append(schedule)
                    
                if not list_invalid_times: # just persist if all times are available
                    for schedule in dados['array_schedule_times']:
                        Bank.Scheduling.save_scheduling(
                                                        id_box=dados['id_box'],
                                                        id_user=user_id,
                                                        start_date=date_processed,
                                                        final_date=date_processed,
                                                        start_hour=schedule,
                                                        final_hour=schedule
                        )

                
                if not list_invalid_times:
                    return {
                        'msg': 'Schedule created'
                    }, 200
                else:
                    return {
                        "msg": f"Schedule time unavailable",
                        "msg_error_custom" : "Periodo atualmente Indiponivel: ",
                        "unavailable_times": list_invalid_times
                    }, 400
            
            else:
                return {
                    'msg': 'Two auth is required'
                }, 401
        
        else:
            return {
                'msg': 'Two auth is required'
            }, 401

        
    
        
            

class ShowSchedule(Resource):
    @jwt_required()
    def get(self):
        jwt_info = get_jwt()
        
        if 'two_auth' in jwt_info:
            if jwt_info['two_auth']:
                user_id = get_jwt_identity()
        
                list_process_schedule = []
                infos = []
                
                schedule = Bank.Scheduling.show_scheduling_user(user_id)
                
                if schedule:
                    for scheduling in schedule:
                        
                        name_box = Bank.DataBaseBox.get_name_box_by_id(scheduling['id_box'])
                        # address = Bank.DataBaseBox.get_address_by_id(user_id)
                        
                        # list_process_schedule.append({
                        #     "data": str(scheduling['datainicio'].strftime('%d/%m/%Y')),
                        #     "datafim": str(scheduling['datafim'].strftime('%d/%m/%Y')),
                        #     "horainicio": str(scheduling['horainicio']),
                        #     "horafim": str(scheduling['horafim']),
                        #     "nome_box": name_box['nome'],
                        #     **address
                        # })

                        # list_all_times_raw = [item[:5] for item in )]

                        list_process_schedule.append({
                            "data": str(scheduling['data_schedule'].strftime('%d/%m/%Y')),
                            "used_times": eval(scheduling['times_schedules']),
                            "id_box": scheduling['id_box'],
                            "nome_box": name_box['nome']
                        })

                    return {
                        'msg': 'Sucess',
                        'list_schedules': list_process_schedule
                    }, 200

            else:
                return {
                    'msg': 'Two auth is required'
                }, 401
        
        else:
            return {
                'msg': 'Two auth is required'
            }, 401
    
class DeleteSchedule(Resource):
    @jwt_required()
    def delete(self):
        jwt_info = get_jwt()
        
        if 'two_auth' in jwt_info:
            if jwt_info['two_auth']:
                id_user = get_jwt_identity()

                argumentos = reqparse.RequestParser()
                
                argumentos.add_argument('id_box', required=True)
                argumentos.add_argument('list_schedules', type=list, required=True)
                argumentos.add_argument('date', required=True)
                
                dados = argumentos.parse_args()

                for time_schedule in dados['list_schedules']:
                    id_locacao = Bank.Scheduling.get_schedule_by_user_time_box(dados['date'], time_schedule, time_schedule, dados['date'], id_box=dados['id_box'], id_user=id_user)
                    Bank.Scheduling.delete_scheduling(id_locacao)
                    

                return {
                    'msg': 'delete with success'
                }, 200

            else:
                return {
                    'msg': 'Two auth is required'
                }, 401
        
        else:
            return {
                'msg': 'Two auth is required'
            }, 401
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
            
            