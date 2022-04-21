from flask import Flask, redirect, url_for, render_template
from flask_restful import  Api
from models import box, users, schedule, payments
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.secret_key = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRETKEY")

api.add_resource(users.UserLogin, "/autenticar") #mvp #Ok
api.add_resource(users.CreateUser, "/criar") #mvp #Ok
api.add_resource(users.TwoFactorLogin, "/codigo") #mvp #Ok
api.add_resource(box.ShowListBox, "/") #mvp #Ok
api.add_resource(box.CreateBox, "/box/create_box")#mvp #Ok
api.add_resource(schedule.ShowSchedule, "/meu_perfil/agendamentos") #mvp
api.add_resource(schedule.DeleteSchedule, "/meu_perfil/deletar_agendamento") #mvp
api.add_resource(schedule.UpdateSchedule, "/meu_perfil/atualizar_agendamento") #mvp
api.add_resource(schedule.GenerateSchedule, "/meu_perfil/criar_agendamento") #mvp
api.add_resource(users.Recover_Password_Email, "/recuperar_senha_email") #mvp #Ok
api.add_resource(users.Recover_Password_Code, "/recuperar_senha_codigo") #mvp #Ok
api.add_resource(users.NewPassword, "/nova_senha") #mvp #Ok
api.add_resource(payments.Payments, "/pagamento") #mvp #ok

if __name__ == "__main__":
    app.run(debug=True)
