import dao as Bank
import defs_workstation as function
from flask import Flask, redirect, url_for, session, render_template, request
import random

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/autenticate", methods=['POST'])
def autenticar():
    if is_email := function.check(request.form['user']):

        email = request.form['user']
        password = request.form['senha']

        password_bank, name_bank = Bank.query_exist_email(email)

        if name_bank:

            if password == password_bank:
                cod = random.randint(111111,999999)
                function.send_email(email, cod)
                cod_user = request.form['cod_user']
                if cod_user == cod:
                    session['usuario_logado'] = name_bank
                    return redirect(url_for("home"))
                else:
                    return redirect(url_for("login"))
                
            return redirect(url_for("login"))

        return redirect(url_for("login"))

    else:

        if is_cpf := function.is_cpf(request.form['user']):

            cpf = request.form['user']
            password = request.form['senha']

            password_bank, name_bank, email_bank = Bank.query_exist_cpf(cpf)

            if name_bank:

                if password == password_bank:
                    cod = random.randint(111111,999999)
                    function.send_email(email_bank, cod)
                    cod_user = request.form['cod_user']
                    if cod_user == cod:
                        session['usuario_logado'] = name_bank
                        return redirect(url_for("home"))
                    else:
                        return redirect(url_for("login"))
                    
                return redirect(url_for("login"))

            return redirect(url_for("login"))

        else:

            cnpj = request.form['user']
            password = request.form['senha']

            password_bank, name_bank, email_bank = Bank.query_exist_cnpj(cnpj)

            if name_bank:

                if password == password_bank:
                    cod = random.randint(111111,999999)
                    function.send_email(email_bank, cod)
                    cod_user = request.form['cod_user']
                    if cod_user == cod:
                        session['usuario_logado'] = name_bank
                        return redirect(url_for("home"))
                    else:
                        return redirect(url_for("login"))
                    
                return redirect(url_for("login"))

            return redirect(url_for("login"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=['POST'])
def create():
    name = request.form['nome']
    last_name = request.form['sobrenome']
    email = request.form['email']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    data_nasc = request.form['data_nasc']
    senha = request.form['senha']

    if valid := function.validates(email, cpf, data_nasc):
        if has := Bank.search(cpf, email):
            Bank.save_user(name, last_name, email, cpf,
                           telefone, data_nasc, senha)
            return redirect(url_for("login"))
        return redirect(url_for('cadastro'))
    return redirect(url_for('cadastro'))


@app.route("/createpj", methods=['POST'])
def create_pj():
    name = request.form['nome']
    last_name = request.form['sobrenome']
    email = request.form['email']
    cnpj = request.form['cpf']
    telefone = request.form['telefone']
    data_nasc = request.form['data_nasc']
    senha = request.form['senha']
    if valid := function.validates_pj(email, cnpj, data_nasc):
        if has := Bank.search_pj(cnpj, email):
            Bank.save_user(name, last_name, email, cnpj,
                           telefone, data_nasc, senha)
            return redirect(url_for("login"))
        return redirect(url_for('cadastro'))
    return redirect(url_for('cadastro'))


@app.route("/update", methods=['POST'])
def update_user():
    id_user = request.form['id_user']
    name = request.form['nome']
    last_name = request.form['sobrenome']
    email = request.form['email']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    data_nasc = request.form['data_nasc']

    Bank.update_user(id_user, name, last_name, cpf, data_nasc, telefone, email)


if __name__ == "__main__":
    app.run(debug=True)
