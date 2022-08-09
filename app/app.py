import os
import logging

import datetime

from models import box, users, schedule, payments, adress
from flask import Flask, redirect, url_for, render_template
from flask_restful import  Resource, Api, reqparse

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt

import parameters

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.secret_key = parameters.APP_SECRET_KEY
app.config["JWT_SECRET_KEY"] = parameters.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=parameters.JWT_EXPIRE_TOKEN)

class HealthCheck(Resource):
    
    def get(self):
        
        return {'status': 'ok'}
    
class VerifyJwtInfos(Resource):
    
    @jwt_required()
    def get(self):
        
        user_id = get_jwt_identity()
        jwt_infos = get_jwt()
        
        if 'two_auth' in jwt_infos:
            two_auth = jwt_infos['two_auth']
        else:
            two_auth = False
        
        if 'recover_passwd' in jwt_infos:
            recover_passwd = jwt_infos['recover_passwd']
        else:
            recover_passwd = False
            
        return {'status': 'ok', 'user': user_id, 'two_auth': two_auth, 'recover_passwd': recover_passwd}, 200


api.add_resource(HealthCheck, '/health')
api.add_resource(VerifyJwtInfos, '/verify_jwt_infos')

api.add_resource(users.UserLogin, "/login")
api.add_resource(users.CreateUser, "/signup ")
api.add_resource(users.TwoFactorLogin, "/two_factor")
api.add_resource(users.GetUserInfo, "/user_info")
api.add_resource(users.Recover_Password_Request_Email, "/password_reset")
api.add_resource(users.Recover_Password, "/new_password")

api.add_resource(box.ShowListBox, "/")
api.add_resource(box.CreateBox, "/box/create_box")

api.add_resource(schedule.ShowSchedule, "/meu_perfil/agendamentos") #mvp
api.add_resource(schedule.DeleteSchedule, "/meu_perfil/deletar_agendamento") #mvp
api.add_resource(schedule.UpdateSchedule, "/meu_perfil/atualizar_agendamento") #mvp
api.add_resource(schedule.GenerateSchedule, "/meu_perfil/criar_agendamento") #mvp

api.add_resource(payments.Payments, "/pagamento")

api.add_resource(adress.Create_adress, "/criar_endereco")

if __name__ == "__main__":
    if parameters.FLASK_ENV == "development":
        logging.basicConfig(level=logging.DEBUG)
    app.run(debug=parameters.FLASK_DEBUG, port=parameters.FLASK_RUN_PORT)
