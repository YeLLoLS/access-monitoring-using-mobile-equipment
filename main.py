from flask import Flask, render_template, request, url_for, session, redirect, flash
from funct import *
from rpi_stuff import *
import requests
from datetime import date, time, datetime
from passlib.hash import sha256_crypt

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
        user = login_info(form_username)
        if user is None:
            flash('Datele introduse sunt incorecte!')
            return redirect(url_for('login'))
        else:
            db_pass = user[3]
            if sha256_crypt.verify(form_password, db_pass):
                acc_status = user[7]
                if acc_status == 'activ':
                    session['idUser'] = user[0]
                    session['username'] = user[2]
                    session['name'] = user[1]
                    session['tip_user'] = user[6]

                    return redirect(url_for('profil', tip_user=session['tip_user']))
                elif acc_status == 'inactiv':
                    flash('Cont dezactivat!')
                    return redirect(url_for('logout'))
            flash('Datele introduse sunt incorecte!')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/adauga_acces', methods=["GET", "POST"])
def adauga_acces():
    if 'username' in session and session['tip_user'] == 'profesor':
        info_salii = get_sali()
        if request.method == 'POST':
            form_numeUser = request.form['numeUser']
            idUser = get_idUser(form_numeUser)
            form_idSala = request.form.get('idSala')
            form_ziAcces = request.form.get('ziAcces')
            form_intervalOrar = request.form.get('intervalOrar')
            interval_split = form_intervalOrar.split('-')
            verificare_acces = get_acces_info(int(idUser), form_idSala, form_ziAcces, interval_split[0],
                                              interval_split[1])
            if verificare_acces is None:
                sala_selectata = []
                for el in info_salii:
                    sala_selectata.append(str(el[0]))
                if form_idSala not in sala_selectata:
                    flash('Sala selecata este invalida!')
                    return redirect(url_for('adauga_acces'))
                else:
                    add_acces(int(idUser), form_idSala, form_ziAcces, interval_split[0], interval_split[1])
                    flash('Acces adaugat cu succes!')
                    return redirect(url_for('adauga_acces'))
            else:
                flash('Acces existent!')
                return redirect(url_for('adauga_acces'))
        return render_template('adauga_acces.html', tip_user=session['tip_user'], name=session['name'], info_sali=info_salii)
    return redirect(url_for('logout'))


@app.route('/adauga_student', methods=["GET", "POST"])
def adauga_student():
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            form_username = request.form['usernameValue']
            user = add_user_info(form_username)
            if user is None:
                form_name = request.form['nameValue']
                form_password = sha256_crypt.hash(request.form['passwordValue'])
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
            form_email = request.form['emailValue']
            form_tipUser = request.form.get('userTypeValue')
            update_user(form_name, form_email, form_tipUser, idUser)
            flash('Utilizatorul a fost modificat!')
            return redirect(url_for('utilizatori'))
        return render_template('edit_user.html', tip_user=session['tip_user'], name=session['name'], user=user)
    return redirect(url_for('logout'))


@app.route('/schimba_parola', methods=["GET", "POST"])
def schimba_parola():
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            form_username = request.form['username']
            form_password = sha256_crypt.hash(request.form['password'])
            change_password(form_username, form_password)
            flash('Parola schimbata cu succes!')
            return redirect(url_for('schimba_parola'))
        return render_template('schimba_parola.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('logout'))


@app.route('/delete_user/<int:idUser>', methods=["POST"])
def delete_user(idUser):
    if 'username' in session and session['tip_user'] == 'profesor':
        if idUser == 2:
            flash('Interzisa stergerea acestui cont!!!')
            return redirect(url_for('utilizatori'))
        elif request.method == 'POST':

            delete_access(idUser)
            delete_responsabil(idUser)
            delete_usr(idUser)
            flash('Utilizatorul a fost sters!')
            return redirect(url_for('utilizatori'))
    return redirect(url_for('logout'))


@app.route('/disable_user/<int:idUser>', methods=["POST"])
def disable_user(idUser):
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            disable_acc(idUser)
            flash('Utilizator dezactivat cu succes!')
            return redirect(url_for('utilizatori_activi'))
    return redirect(url_for('logout'))


@app.route('/activate_user/<int:idUser>', methods=["POST"])
def activate_user(idUser):
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            activate_acc(idUser)
            flash('Utilizator dezactivat cu succes!')
            return redirect(url_for('utilizatori_inactivi'))
    return redirect(url_for('logout'))


@app.route('/utilizatori_activi', methods=["GET", "POST"])
def utilizatori_activi():
    if 'username' in session and session['tip_user'] == 'profesor':
        users = get_active_users()
        if users is None:
            flash('Nu exista utilizatori!')
            return redirect(url_for('utilizatori_activi'))
        else:
            return render_template('utilizatori_activi.html', tip_user=session['tip_user'], name=session['name'],
                                   users=users)
    return redirect(url_for('logout'))


@app.route('/utilizatori_inactivi', methods=["GET", "POST"])
def utilizatori_inactivi():
    if 'username' in session and session['tip_user'] == 'profesor':
        users = get_inactive_users()
        if users is None:
            flash('Nu exista utilizatori!')
            return redirect(url_for('utilizatori_inactivi'))
        else:
            return render_template('utilizatori_inactivi.html', tip_user=session['tip_user'], name=session['name'],
                                   users=users)
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
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'POST':
            delete_access(idUser)
            flash('Accesul a fost sters!')
            return redirect(url_for('acces_sali'))
    return redirect(url_for('logout'))


@app.route('/profil')
def profil():
    if 'username' in session:
        timp_start = "00:00"
        timp_end = "12:00"
        timp_start1 = "12:00"
        timp_end1 = "00:00"
        checkOra1 = time_in_range(timp_start, timp_end)
        checkOra2 = time_in_range(timp_start1, timp_end1)

        if checkOra1 is True:
            info = list(test(2, get_date(), timp_start1, timp_end1))
            list_id = []
            for el in info:
                list_id.append(el['idSala'])
            return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                   idSala=list_id)
        elif checkOra2 is True:
            info = list(test(2, get_date(), timp_start1, timp_end1))
            list_id = []
            for el in info:
                list_id.append(el['idSala'])
            return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                   idSala=list_id)
    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])


"""@app.route('/profil')
def profil():
    if 'username' in session:
        info = get_acces_for_button(session['idUser'])
        info2 = get_acces_for_button1(session['idUser'])
        if len(info2) == 0:
            return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])
        elif len(info2) == 1 and info[0][0] == 6:
            zi_acces = info[0][1]
            zi_curenta = get_date()
            if zi_acces == zi_curenta:
                ora_start = info[0][2]
                ora_end = info[0][3]
                checkOra = time_in_range(ora_start, ora_end)
                if checkOra is True:
                    b206 = [info[0][0]]
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                           idSala=b206)
                else:
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])
            else:
                return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])
        elif len(info2) == 1 and info[0][0] == 7:
            zi_acces = info[0][1]
            zi_curenta = get_date()
            if zi_acces == zi_curenta:
                ora_start = info[0][2]
                ora_end = info[0][3]
                checkOra = time_in_range(ora_start, ora_end)
                if checkOra is True:
                    b207 = [info[0][0]]
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                           idSala=b207)
                else:
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])
            else:
                return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])
        elif len(info2) == 2:
            zi_acces1 = info[0][1]
            zi_acces2 = info[1][1]
            zi_curenta = get_date()
            if zi_acces1 == zi_acces2 == zi_curenta:
                ora_start1 = info[0][2]
                ora_end1 = info[0][3]
                ora_start2 = info[1][2]
                ora_end2 = info[1][3]

                checkOra = time_in_range(ora_start1, ora_end1)
                checkOra2 = time_in_range(ora_start2, ora_end2)
                if checkOra == checkOra2:
                    idSala = [info[0][0], info[1][0]]
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                           idSala=idSala)
                elif checkOra is True:
                    idSala = [info[0][0]]
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                           idSala=idSala)
                elif checkOra2 is True:
                    idSala = [info[1][0]]
                    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                           idSala=idSala)
            else:
                if zi_acces1 == zi_curenta:
                    ora_start = info[0][2]
                    ora_end = info[0][3]
                    checkOra = time_in_range(ora_start, ora_end)
                    if checkOra is True:
                        idSala = [info[0][0]]
                        return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                               idSala=idSala)
                elif zi_acces2 == zi_curenta:
                    ora_start = info[1][2]
                    ora_end = info[1][3]
                    checkOra = time_in_range(ora_start, ora_end)
                    if checkOra is True:
                        idSala = [info[1][0]]
                        return render_template('profil.html', tip_user=session['tip_user'], name=session['name'],
                                               idSala=idSala)

    return render_template('profil.html', tip_user=session['tip_user'], name=session['name'])"""


@app.route('/deschide_usa', methods=["GET", "POST"])
def deschide_usa():
    if 'username' in session and session['tip_user'] == 'profesor':
        if request.method == 'GET':
            return redirect(url_for('profil')), req(session['name'])
        else:
            return "Error!!!"
    return redirect(url_for('logout'))


@app.route('/adauga_sali', methods=["GET", "POST"])
def adauga_sali():
    if 'username' in session and session['tip_user'] == 'profesor':
        info_responsabili = get_responsabili()
        if request.method == 'POST':
            form_numeSala = request.form['numeSala']
            form_numarLocuri = request.form.get('numarLocuri')
            form_responsabil = int(request.form.get('idResponsabil'))
            lista_responsabili = []
            a = get_responsabili()
            for el in a:
                lista_responsabili.append(int(el[0]))
            if form_responsabil not in lista_responsabili:
                flash('Resposanbil selectat gresit!')
                return redirect(url_for('adauga_sali'))
            else:
                form_cladire = request.form.get('cladire')
                val_cladire_acceptate = {'UPT_ELECTRO: A', 'UPT_ELECTRO: B', 'UPT_ELECTRO: C', 'UPT_ELECTRO: D'}
                if form_cladire not in val_cladire_acceptate:
                    flash('Cladire invalida!')
                    return redirect(url_for('adauga_sali'))
                else:
                    form_tip_sala = request.form.get('tip_sala')
                    val_tipSala_acceptate = {'laborator', 'seminar', 'curs'}
                    if form_tip_sala not in val_tipSala_acceptate:
                        flash('Tip sala invalid!')
                        return redirect(url_for('adauga_sali'))
                    else:
                        add = adauga_sala(form_numeSala, form_cladire, form_responsabil, form_numarLocuri,
                                          form_tip_sala)
                        if add == 'OK':
                            flash('Sala adaugata cu succes!')
                            return redirect(url_for('adauga_sali'))
                        elif add == 'Exista deja aceasta sala!':
                            flash('Exista deja aceasta sala!')
                            return redirect(url_for('adauga_sali'))

        return render_template('adauga_sali.html', tip_user=session['tip_user'], name=session['name'],
                               info_responsabili=info_responsabili)
    return redirect(url_for('logout'))


@app.route('/adauga_unitate', methods=["GET", "POST"])
def adauga_unitate():
    if 'username' in session and session['tip_user'] == 'profesor':
        info_sali = get_sali_notInUnitatiSali()
        if request.method == 'POST':
            form_numeUnitate = request.form['numeUnitate']
            form_idSala = request.form.get('idSala')
            add = adauga_unitate_unitateSala(form_numeUnitate, int(form_idSala))
            if add == 'OK':
                flash('Adaugat cu succes!')
                return redirect(url_for('adauga_unitate'))
            elif add == 'Exista deja o unitate cu acest nume!':
                flash('Exista deja o unitate cu acest nume!')
                return redirect(url_for('adauga_unitate'))
        return render_template('adauga_unitate.html', tip_user=session['tip_user'], name=session['name'],
                               info_sali=info_sali)
    return redirect(url_for('logout'))


@app.route('/administrare_utilizatori', methods=["GET", "POST"])
def administrare_utilizatori():
    if 'username' in session and session['tip_user'] == 'profesor':
        return render_template('administrare_utilizatori.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('login'))


@app.route('/administrare_accese', methods=["GET", "POST"])
def administrare_accese():
    if 'username' in session and session['tip_user'] == 'profesor':
        return render_template('administrare_accese.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('login'))


@app.route('/administrare_unitati_fizice', methods=["GET", "POST"])
def administrare_unitati_fizice():
    if 'username' in session and session['tip_user'] == 'profesor':
        return render_template('administrare_unitati_fizice.html', tip_user=session['tip_user'], name=session['name'])
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='127.0.0.1')
