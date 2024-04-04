import os.path
import mysql.connector
import numpy # used for subtracting from array values
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_session import Session
from backend.usr_Acess import pageApology, loginRequired, isAdmin, isAdminPage
from datetime import date, datetime
import backend.dynamicHTMLS



app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Database connection
db = mysql.connector.connect(
    user='root',
    password='root',
    database='medusrmain',
    raise_on_warnings = True,
)

dbcursor = db.cursor(buffered=True)  

# for finding files mostly img src
@app.template_filter('find')
def find(haystack, needle):
    if not isinstance(haystack, str):
        return False
    return needle in haystack


## PAGE FUNCTIONS ##


# Main page
@app.route("/")
@isAdmin
def mainPage():
    sessionUID = session.get("usr_id")
    isAdmin = session.get("isAdmin", False) 
    if sessionUID is not None:
        print(isAdmin)
        print(session["usr_id"])
    return render_template("index.html", isAdmin=isAdmin)

@app.route("/usrMainPage")
@isAdmin
@loginRequired
def usrMainPage():
    isAdmin = session.get("isAdmin", False) 
    if isAdmin != True:
        # print("not admin")
        # print(isAdmin)
        dbcursor.execute("SELECT * FROM curso LEFT JOIN curso_check ON curso_check.cc_curs_id=curs_id WHERE cc_usr_id = %s", (session["usr_id"],))
        cursos = dbcursor.fetchall()
        # print(len(cursos))
        if len(cursos) > 0:
            return render_template("MainPageUsr.html", cursos=cursos)
        else:
            # print("No courses found")
            return render_template("MainPageUsr.html")
    else:
        print("ADMIN")
        dbcursor.execute("SELECT * FROM curso")
        cursos = dbcursor.fetchall()
        return render_template("MainPageUsr.html", cursos=cursos)

@app.route("/adminMainPage")
@loginRequired
@isAdminPage
def adminMainPage():
    return render_template("admPage.html")


## COURSE CREATION FUNCTIONS ##


@app.route("/coursMEdit", endpoint="cours_m_edit", methods=["POST"])
@loginRequired
@isAdminPage
def coursMEdit():
    CsrIds = request.form.get("id")
    newCrsNames = request.form['name']
    newCrsProfs = request.form['prof']
    newCrsPrices = request.form['price']
    # print('data: ' + CsrIds)

    dbcursor.execute("UPDATE curso SET cur_name = %s, prof = %s, curs_price = %s WHERE curs_id = %s", 
        (
            newCrsNames,
            newCrsProfs,
            newCrsPrices,
            CsrIds,
        )
    )
    db.commit()
    return redirect("/coursMList") 

@app.route("/coursMList", endpoint="cours_m_list", methods=["GET"])
@loginRequired
@isAdminPage
def coursMList():
    dbcursor.execute("SELECT * FROM curso")
    cursos = dbcursor.fetchall()
    dbcursor.execute("SELECT COUNT(*) FROM curso")
    cursoC = dbcursor.fetchall()
    return render_template("/cursos/coursPageCreate.html", cursos=cursos, cursoC=cursoC, cursoCs = 100 + int((cursoC[0][0]) * 2) )



@app.route("/coursMCreate", endpoint="cours_m_create", methods=["POST"])
@loginRequired
@isAdminPage
def coursMCreate():
    # Criar curso por function Sendo que Só admin pode criar
    # Ao mesmo tempo que vai criar o curso no databank tem que criar um html do curso
    # Tem que deixar eles editarem tudo sobre o curso tbm :/
    newCsrIds = request.form.getlist("NcrsId")
    newCrsNames = request.form.getlist("NcrsName")
    newCrsProfs = request.form.getlist("NcrsProf")
    newCrsPrices = request.form.getlist("NcrsPrice")

    if newCsrIds == None or newCsrIds == '':
        return pageApology("None type detection", 400)
    # print("New Course Rows:", newCrsNames, newCrsProfs, newCrsPrices)
    
    try:
        for i, name in enumerate(newCrsNames):
            checkF = os.path.isfile('templates/cursos/curpages/' +name+ '.html')
            if (checkF == False) :
                file = open('templates/cursos/curpages/'+name+'.html', 'x')
                file.write(backend.dynamicHTMLS.exHtml)
            else:
                print("Catch_Error[crsCreate]: {} html page exists already".format(name))
            # file = open('templates/cursos/curpages/'+name+'.html', 'r')
            # print(file.read())
            dbcursor.execute("SELECT * FROM curso WHERE cur_name=%s", (name,))
            chkCrsEx = dbcursor.fetchall()

            if (chkCrsEx is None or False):
                dbcursor.execute(
                    "INSERT INTO curso (curs_id, cur_name, prof, curs_price) VALUES(%s, %s, %s, %s)", 
                    (
                        newCsrIds[i],
                        name,
                        newCrsProfs[i],
                        newCrsPrices[i],
                        # all the amazing list array stuff hold on lemme do the html first
                    )
                )
                db.commit()
            else:
                print("Catch_ERROR[crsCreate]: {} already is registered as a course".format(name))
        # Now we need to do the same But this time we will be creating TABLES for the courses
        # Each TABLE will have Classes which hold the links to their courses content, god this sucks
        # now we are gonna need to remake that file system to also make folders each for a course that gets added
        # maybe i should look into how other courses do this i really do not wanna mess this up cuz its one mistake
        # and then i gotta do it all over again.
        # Dont forget the deleteCourse function will need to go over everything else too!
    except TypeError as e:
        print(e)
        print("commit failure check Course creation function.")
    return redirect("/coursMList")


@app.route("/deleteCourse", endpoint="cours_single_delete", methods=["POST"])
@loginRequired  
@isAdminPage
def deleteCourse():
    id = request.form.get("id")
    dbcursor.execute("DELETE FROM curso_check WHERE cc_curs_id = %s", ((id, )))
    db.commit()
    dbcursor.execute("DELETE FROM curso WHERE curs_id = %s", ((id,)))
    db.commit()
    # decrement ids bigger than deleted id
    dbcursor.execute("UPDATE curso SET curs_id = curs_id - 1 WHERE curs_id > %s", ((id,)))
    db.commit()
    return redirect("/coursMList")

@app.route("/coursePgRdr/<course>", endpoint="cours_redir_pg", methods=["GET"])
@loginRequired
def coursePgRdr(course):
    # crs = request.form['course']
    dbcursor.execute("SELECT cur_name FROM curso WHERE curs_id = %s", ((course,))) # originally crs
    crsName = dbcursor.fetchone()
    crsName = str(crsName[0])
    print(crsName)
    checkF = os.path.isfile('templates/cursos/curpages/' + crsName + '.html')
    print(checkF) # always getting false
    if (checkF):
        #return render_template("/cursos/curpages/DefaultCurTMP.html", crsName=crsName)
        return render_template("/cursos/curpages/{}.html".format(crsName), crsName=crsName)
    else:
        return ("#0")
        


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Variables for making it easier to type
        f_password = request.form.get("password")
        f_email = request.form.get("email")


        if not f_email:
            return pageApology("Falta Email", 400)
        elif not f_password:
            return pageApology("Falta Senha", 400)
        
        # Check if Account Exists
        d_current_status = dbcursor.execute(
            "SELECT user_email FROM user WHERE user_email = %s", (
                (f_email,)
                )
        )
        row = dbcursor.fetchone()
        if row is None or len(row) == 0:
                return pageApology("Conta Não Existe")


        # Check account activity
        d_current_status = dbcursor.execute(
            "SELECT active_status FROM user WHERE user_email = %s", (
                (f_email,)
                )
        )
        row = dbcursor.fetchone()
        d_current_status = row[0]
        if not d_current_status or d_current_status == 0:
            return pageApology("Conta Desativada", 400)
        else:
            d_current_status = dbcursor.execute(
            "SELECT * FROM user WHERE user_email = %s", (
                (f_email,)
                )
            )
            rows = dbcursor.fetchall()
            row = rows[0]

            if len(rows) != 1 or not row[3] == f_password:
                return pageApology("invalid username and/or password", 400)
            else:
                pass
            
            # Remember user
            session["usr_id"] = row[0]

            return redirect("/")
        

    else:
        return render_template("login.html")
    
## ADMIN REGISTER EDIT USER FUNCTIONS ##
    
@app.route("/usrMList", endpoint="usr_m_list", methods=["GET"])
@loginRequired
@isAdminPage
def usrMList():

    dbcursor.execute("SELECT * FROM user")
    alunos = dbcursor.fetchall()
    dbcursor.execute("SELECT COUNT(*) FROM user")
    alunoC = dbcursor.fetchall()
    dbcursor.execute("SELECT cur_name, curs_id FROM curso")
    cursosN = dbcursor.fetchall()
    dbcursor.execute("SELECT * FROM curso_check ORDER BY cc_curs_id")
    varDCC = dbcursor.fetchall()
    # dbcursor.execute("SELECT curso.cur_name, user.usr_id FROM curso LEFT JOIN curso_check ON curso.curs_id=curso_check.cc_curs_id INNER JOIN user ON curso_check.cc_usr_id=user.usr_id WHERE curso_check.cc_usr_id = user.usr_id")
    # acursos = dbcursor.fetchall()
    return render_template("alunoGrnc.html", alunos=alunos, alunoC=alunoC, cursosN=cursosN, varDCC=varDCC)

@app.route("/aUsrReg", endpoint="ausr_reg", methods=["POST"])
@loginRequired
@isAdminPage
def aUsrReg():
    newUsrIds = request.form.getlist("NusrId")
    newUsrNames = request.form.getlist("NusrName")
    newUsrEmail = request.form.getlist("NusrEmail")
    newUsrPass = request.form.getlist("NusrPass")
    newUsrCPF = request.form.getlist("NusrCPF")
    newUsrNum = request.form.getlist("NusrNum")

    if newUsrIds == None or newUsrIds == '':
        return pageApology("None type detection", 400)
    # print("New Course Rows:", newCrsNames, newCrsProfs, newCrsPrices)
    
    try:
        for i, name in enumerate(newUsrNames):
            print("newIDS : {}".format(newUsrIds[i]))
            dbcursor.execute(
                "INSERT INTO user (usr_id, username, user_email, password, cpf, contact_number, reg_date, reg_time, active_status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (
                    newUsrIds[i],
                    name,
                    newUsrEmail[i],
                    newUsrPass[i],
                    newUsrCPF[i],
                    newUsrNum[i],
                    date.today().strftime("%d/%m/%Y"),
                    datetime.now().strftime("%H:%M:%S"),
                    True,
                    # all the amazing list array stuff hold on lemme do the html first
                )
            )
        db.commit()
    except Exception as e:
        print(e)
        print("commit.")
    return redirect("/usrMList")



@app.route("/usrCRSreg", endpoint="usr_C_reg", methods=["POST"])
@loginRequired
@isAdmin
@isAdminPage
def usrCRSreg():
    id = request.form.get('id').split(',')
    detN = request.form['detNmb']
    if int(detN) == 1:
        
        # print("curs = " + (id[0]))
        # print("usr = " + (id[1]))
    
        # print("ADD USR_CRS REQUEST BY USER " + str(session["usr_id"]))

        dbcursor.execute("SELECT COUNT(*) FROM curso_check WHERE cc_curs_id=%s AND cc_usr_id=%s", 
            (id[0], id[1])
        )
        checkCRSreg = dbcursor.fetchone()[0]
        if checkCRSreg >= 1:
            print("usr registered?")
            print(checkCRSreg)
            return ("user already registered into course (HOW???????????)")
        
        dbcursor.execute("INSERT INTO curso_check (cc_curs_id, cc_usr_id) VALUES(%s, %s)", 
            (id[0], id[1])
        )
        db.commit()
    else:

        # print("DEL USR_CRS REQUEST BY USER " + str(session["usr_id"]))

        dbcursor.execute("SELECT COUNT(*) FROM curso_check WHERE cc_curs_id=%s AND cc_usr_id=%s", 
            (id[0], id[1])
        )
        checkCRSreg = dbcursor.fetchone()[0]
        if checkCRSreg < 1:
            print("usr not registered?")
            print(checkCRSreg)
            return ("user not registered into course (HOW???????????)")
        
        dbcursor.execute("DELETE FROM curso_check WHERE cc_curs_id = %s AND cc_usr_id = %s", 
            (id[0], id[1])
        )
        db.commit()
    return ("request...")

@app.route("/deleteUser", endpoint="usr_del_reg", methods=["POST"])
@loginRequired
@isAdmin
@isAdminPage
def deleteUser():
    detN = int(request.form['detNmb'])
    if detN == 0:
        id = request.form.get("id")
        #sndLgtRq(id)
        dbcursor.execute("DELETE FROM curso_check WHERE cc_usr_id = %s", ((id,)))
        db.commit()
        dbcursor.execute("DELETE FROM user WHERE usr_id = %s", ((id,)))
        db.commit()

        # decrement ids bigger than deleted id
        dbcursor.execute("UPDATE user SET usr_id = usr_id - 1 WHERE usr_id > %s", ((id,)))
        db.commit()
        return redirect("/usrMList")

    elif detN == 1:
        id = request.form.get("id")
        # sndLgtRq(id, detnmb = True)
        idray = list(map(int, id.split(',')))
        idray.sort()
        for i, number in enumerate(idray):
            print("(/deleteUser/Multiple) ids to be deleted : {} ".format(idray))
            dbcursor.execute("DELETE FROM curso_check WHERE cc_usr_id = %s", (( number,)))
            db.commit()
            dbcursor.execute("DELETE FROM user WHERE usr_id = %s", (( number,)))
            db.commit()
        dbcursor.execute("SELECT COUNT(*) FROM user")
        curcount = dbcursor.fetchone()
        curcount = int(curcount[0])
        dbcursor.execute("SELECT MAX(usr_id) FROM user")
        curlast = dbcursor.fetchone()
        curlast = int(curlast[0])
        # print(idray[0])
        while (int(curlast) != int(curcount)):
            # print("curlast: {}".format(curlast))
            # print("curcount: {}".format(curcount))
            dbcursor.execute("UPDATE user SET usr_id = usr_id - 1 WHERE usr_id >= %s", (( int(idray[0]),)))
            db.commit()
            curcount += 1
        return redirect("/usrMList")
    

# NOT DONE supposed to log out users who have been deleted to avoid further errors in database
# and also avoid stuff like people logging into old ids (scary)
@loginRequired
def sndLogoutRq(id, detnmb = False):
    if detnmb == False:
        for i, ids in enumerate(id):
            if session["usr_id"] == ids:
                session.pop(ids)
    elif detnmb == True:
        for i, ids in enumerate(id):
            print(ids)
            print(session.get(ids))
            dbcursor.execute("SELECT * FROM user WHERE usr_id=%s AND active_status=1", ((ids,)))
            usr = dbcursor.fetchall()        
            print('logging {} out'.format(ids))
            session.get(ids)

@app.route("/AuserEdit", endpoint="user_edit", methods=["POST"])
@loginRequired
@isAdminPage
def AuserMEdit():
    CsrIds = request.form.get("id")
    newCrsNames = request.form['name']
    newCrsEmail = request.form['email']
    newCrsPass = request.form['pass']
    newCrsCPF = request.form['cpf']
    newCrsnums = request.form['num']
    # print('data: ' + CsrIds)

    dbcursor.execute("UPDATE user SET username = %s, user_email = %s, password = %s, cpf = %s, contact_number = %s WHERE usr_id = %s", 
        (
            newCrsNames,
            newCrsEmail,
            newCrsPass,
            newCrsCPF,
            newCrsnums,
            CsrIds,
        )
    )
    db.commit()
    return redirect("/usrMList") 



## USER LOGIN FUNCTIONS ##


# Register
@app.route("/register", methods=["GET", "POST"])
def register():    
    if request.method == "POST":

        # Variables for making it easier to type
        f_username = request.form.get("username")
        f_password = request.form.get("password")
        f_email = request.form.get("email")
        f_CPF = request.form.get("CPF")
        f_password_chk = request.form.get("confirmation")
        f_contact_number = request.form.get("contact-phone")

        # CHECK USERNAME
        print(f_username.replace(" ", "").isalpha()) 
        if f_username.isalpha():
            return pageApology("Nome Inválido", 400)
        elif not f_username or len(f_username.split()) < 2:
            print(f_username)
            return pageApology("Providencie Nome Completo", 400)
        
        elif not f_email:
            return pageApology("Providencie Email válido", 400)
        
        elif not f_CPF or f_CPF.isalpha():
            return pageApology("Providencie CPF válido", 400)

        # CHECK PASSWORD 
        elif not f_password:
            return pageApology("Providencie Senha", 400)
        elif not f_password_chk:
            return pageApology("Senhas Não Correspondem", 400)
        elif f_password_chk != f_password:
            return pageApology("Senhas Não Correspondem", 400)
        
        # Check if User already exists on database [ Check by CPF since its unique anyways ]
        dbcursor.execute(
            "SELECT cpf FROM user WHERE cpf = %s", (f_CPF,)
        )
        rows = dbcursor.fetchall()
        print(rows)

        if rows is not None:
            if len(rows) == 1:
                return pageApology("user already exists [matching CPF found]", 400)
            else:
                # Start storing User into database (db)
                    dbcursor.execute(
                        "INSERT INTO user (username, password, cpf, user_email, contact_number, reg_date, reg_time, active_status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                            (
                                f_username,
                                f_password,
                                f_CPF,
                                f_email,
                                f_contact_number,
                                date.today().strftime("%d/%m/%Y"),
                                datetime.now().strftime("%H:%M:%S"),
                                True,
                            )
                        )
                    db.commit()
                    return redirect("/")

    
    # GET
    else:
        return render_template("register.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# AFTEREND
# Funções para quando eu tiver pouco tempo para manusear o site / oportunidade melhor surgir
# Muito difícil implementar agr + leva tempo




