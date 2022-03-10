import dao as Bank
# agenda workstation
from datetime import datetime
from datetime import timedelta
# validando e salvando agendamentos

start_date = request.form['data_inicio']  # aaaa/mm/dd
start_hour = request.form["hora_inicio"]  # hh:mm:ss
final_hour = request.form["hora_fim"]  # hh:mm:ss
final_date = request.form["data_final"]  # aaaa/mm/dd
id_user = request.form["id_user"]
id_box = request.form["id_box"]

if Bank.verify_scheduling(start_date, start_hour, final_hour, final_date, id_box):
    Bank.save_scheduling(start_date, start_hour, final_hour,
    final_date, id_user, id_box)
else:
    print('Agendamento inválido')
# mandando todas datas usadas para o front

list_locations = Bank.show_all_scheduling()

if list_locations:
    for dict_locations in list_locations:
        start_date = dict_locations['datainicio']
        final_date = dict_locations['datafim']
        
        start_day = start_date.day
        start_month = start_date.month
        start_year = start_date.year
        
        final_day = final_date.day
        final_month = final_date.month
        final_year = final_date.year
        
        
        list_days = [days for days in range(start_day, final_day+1)]
        list_dates = [f'{days}/{start_month}/{start_year}' for days in list_days]
                
        print(list_dates)
