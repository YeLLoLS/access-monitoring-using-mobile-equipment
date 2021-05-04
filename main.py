from flask import Flask, render_template, request, url_for, session, redirect, flash
from funct import login_info, add_user_info, add_user, get_users, get_single_user, update_user, delete_usr, get_acces, \
    delete_access, get_acces_info, add_acces

app = Flask(__name__)

app.secret_key = 'haida'


@app.route("/")
def index():
    return redirect(url_for('profil'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        form_username = request.form['usernameValue']
        form_password = request.form['passwordValue']
        user = login_info(form_username, form_password)
        if user is None:
            flash('Datele introduse sunt incorecte!')
            return redirect(url_for('login'))
        else:
            acc_status = user[7]
            if acc_status == 'activ':
                name = user[1]
                username = user[2]
                tip_user = user[6]
                session['username'] = username
                session['name'] = name
                session['tip_user'] = tip_user

                return redirect(url_for('profil', tip_user=session['tip_user']))
            elif acc_status == 'inactiv':
                flash('Cont dezactivat!')
                return redirect(url_for('logout'))

    return render_template('login.html')


@app.route('/adauga_acces', methods=["GET", "POST"])
def adauga_acces():
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            form_idUser = request.form['idUser']
            form_idSala = request.form.get('idSala')
            print(form_idUser)
            print(form_idSala)
            verificare_acces = get_acces_info(form_idUser, form_idSala)
            print(verificare_acces)
            if verificare_acces is None:
                sala_selecata = {'6', '7'}
                if form_idSala not in sala_selecata:
                    flash('Sala selecata este invalida!')
                    return redirect(url_for('adauga_acces'))
                else:
                    add_acces(form_idUser, form_idSala)
                    flash('Acces adaugat cu succes!')
                    return redirect(url_for('adauga_acces'))
            else:
                flash('Acces existent!')
                return redirect(url_for('adauga_acces'))
        return render_template('adauga_acces.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('logout'))


@app.route('/adauga_student', methods=["GET", "POST"])
def adauga_student():
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            form_username = request.form['usernameValue']
            user = add_user_info(form_username)
            if user is None:
                form_name = request.form['nameValue']
                form_password = request.form['passwordValue']
                form_email = request.form['emailValue']
                form_tip_user = request.form.get('selected_acc_type')
                tip_cont_acceptat = {'student', 'profesor'}
                if form_tip_user not in tip_cont_acceptat:
                    flash('Tipul contului selectat este invalid!')
                    return redirect(url_for('adauga_student'))
                else:
                    add_user(form_name, form_username, form_password, form_email, form_tip_user)
                    flash('Student adaugat cu success!')
                    return redirect(url_for('adauga_student'))
            else:
                flash('Student existent!')
                return redirect(url_for('adauga_student'))

        return render_template('adauga_student.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('logout'))


@app.route('/edit_user/<int:idUser>', methods=["GET", "POST"])
def edit_user(idUser):
    if 'username' in session and session['tip_user'] == 'profesor':
        user = get_single_user(idUser)
        if request.method == 'POST':
            form_name = request.form['nameValue']
            form_username = request.form['usernameValue']
            form_password = request.form['passwordValue']
            form_email = request.form['emailValue']
            form_tipUser = request.form['userTypeValue']
            form_accStatus = request.form['accStatusValue']
            update_user(form_name, form_username, form_password, form_email, form_tipUser, form_accStatus, idUser)
            flash('Utilizatorul a fost modificat!')
            return redirect(url_for('utilizatori'))
        return render_template('edit_user.html', tip_user=session['tip_user'], name=session['name'], user=user)
    return redirect(url_for('logout'))


@app.route('/delete_user/<int:idUser>', methods=["POST"])
def delete_user(idUser):
    if 'username' in session and session['tip_user'] == 'profesor':
        if idUser == 2:
            flash('Interzisa stergerea acestui cont!!!')
            return redirect(url_for('utilizatori'))
        elif request.method == 'POST':
            delete_usr(idUser)
            flash('Utilizatorul a fost sters!')
            return redirect(url_for('utilizatori'))
    return redirect(url_for('logout'))


@app.route('/utilizatori', methods=["GET", "POST"])
def utilizatori():
    if 'username' in session and session['tip_user'] == 'profesor':
        users = get_users()
        if users is None:
            flash('Nu exista utilizatori!')
            return redirect(url_for('utilizatori'))
        else:
            return render_template('utilizatori.html', tip_user=session['tip_user'], name=session['name'], users=users)
    return redirect(url_for('logout'))


@app.route('/acces_sali', methods=["GET", "POST"])
def acces_sali():
    if 'username' in session and session['tip_user'] == 'profesor':
        acceses = get_acces()
        if acceses is None:
            flash('Nu exista accese!')
            return redirect(url_for('acces_sali'))
        else:
            return render_template('acces_sali.html', tip_user=session['tip_user'], name=session['name'],
                                   acceses=acceses)
    return redirect(url_for('logout'))


@app.route('/delete_acces/<int:idUser>', methods=["POST"])
def delete_acces(idUser):
    print(idUser)
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            delete_access(idUser)
            flash('Accesul a fost sters!')
            return redirect(url_for('acces_sali'))
    return redirect(url_for('logout'))


@app.route('/profil')
def profil():
    if 'username' in session:
        return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('logout'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='127.0.0.1')
