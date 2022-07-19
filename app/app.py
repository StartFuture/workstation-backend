import os
import logging

from models import box, users, schedule, payments, adress
from flask import Flask, redirect, url_for, render_template
from flask_restful import  Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt

import parameters

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.secret_key = parameters.APP_SECRET_KEY
app.config["JWT_SECRET_KEY"] = parameters.JWT_SECRET_KEY


class HealthCheck(Resource):
    
    def get(self):
        return {'status': 'ok'}
    
class Protected(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        two_auth = get_jwt()['two_auth']
        return {'status': 'ok', 'user': user_id, 'two_auth': two_auth}
    
# Test endpoints
api.add_resource(HealthCheck, '/health')
api.add_resource(Protected, '/protected')

api.add_resource(users.UserLogin, "/autenticar") #mvp #Ok
api.add_resource(users.CreateUser, "/criar") #mvp #Ok
api.add_resource(users.TwoFactorLogin, "/codigo") #mvp #Ok
api.add_resource(users.Recover_Password_Email, "/recuperar_senha_email") #mvp #Ok
api.add_resource(users.Recover_Password_Code, "/recuperar_senha_codigo") #mvp #Ok
api.add_resource(users.NewPassword, "/nova_senha") #mvp #Ok

api.add_resource(box.ShowListBox, "/") #mvp #Ok
api.add_resource(box.CreateBox, "/box/create_box")#mvp #Ok

api.add_resource(schedule.ShowSchedule, "/meu_perfil/agendamentos") #mvp
api.add_resource(schedule.DeleteSchedule, "/meu_perfil/deletar_agendamento") #mvp
api.add_resource(schedule.UpdateSchedule, "/meu_perfil/atualizar_agendamento") #mvp
api.add_resource(schedule.GenerateSchedule, "/meu_perfil/criar_agendamento") #mvp

api.add_resource(payments.Payments, "/pagamento") #mvp #ok

api.add_resource(adress.Create_adress, "/criar_endereco")

if __name__ == "__main__":
    app.run(debug=parameters.FLASK_DEBUG, port=parameters.FLASK_RUN_PORT)

# 
