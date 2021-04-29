from flask import Flask, render_template, request, url_for, session, redirect, flash
from funct import login_info, add_user_info, add_user, get_users, get_single_user, update_user, delete_usr

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
                    flash('Student adaugat cu success!')
                    return redirect(url_for('adauga_student')), add_user(form_name,
                                                                         form_username,
                                                                         form_password,
                                                                         form_email,
                                                                         form_tip_user)
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
        if idUser == 13:
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
