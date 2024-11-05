import os.path
import pymysql
import numpy
import shutil
import sqlite3
from backend.tables import TABLES
from backend import dynamicHTMLS
from backend.connection import connect_to_mysql
from backend.usr_Acess import pageApology, loginRequired, isAdmin, isAdminPage
from datetime import date, datetime
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_session import Session
from importlib import import_module
from werkzeug.utils import secure_filename
from colorama import Back, Style



app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'static/assets/upload'
Session(app)

config = {
    "user": 'root',
    "password": 'root',
    "database": 'medusrmain',
}

# Database connection
db = connect_to_mysql(config)

print(db)

dbcursor = db.cursor()


print(dbcursor)
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        dbcursor.execute(table_description)
    except pymysql.Error as err:
        print(err)
    else:
        print("OK")

def sSRec():
    print("Session is:", session["usr_id"])
    return 0

def dbRec():
    global db
    if (db.open == True):
        print(Back.GREEN + "MYSQL IS : CONNECTED" + Style.RESET_ALL)
        return
    else:
        print(Back.YELLOW + "MYSQL IS : CLOSED" + Style.RESET_ALL)
    try:
        print(Back.LIGHTGREEN_EX + "Attempting Reconnecction" + Style.RESET_ALL)
        db.ping(reconnect=True)
    except Exception as e:
        print(Back.RED +"DBREC ERROR: {}".format(e) + Style.RESET_ALL)
    finally:
        if (db.open != True):
            db = connect_to_mysql(config)
            print('MYSQL COULDNT RECCONECT, new connection has been created')
        return


def ytEMB(Ylink:str):
    if Ylink.startswith('https://www.youtube.com/watch?v=') == True or Ylink.startswith('youtube.com/watch?v=') == True:
        Ycode = Ylink.split('=')[1]
        newlink = 'https://www.youtube.com/embed/' + Ycode + '?'
        return newlink
    elif Ylink.startswith('https://www.youtube.com/live') == True or Ylink.startswith('youtube.com/live') == True:
        print('ITS A LIVESTREAM')
        Ycode = Ylink.split('live/')[1]
        newlink = 'https://www.youtube.com/embed/' + Ycode + '?'
        return newlink
    else:
        return Ylink


def from_module_get(module_name, attr):
    return getattr(import_module(module_name), attr)

# for finding files mostly img src | this is for jinja
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

@app.route("/aPages/<type>")
@isAdmin
def advPage(type):
    try:
        return render_template('{}.html'.format(type))
    except Exception as e:
        print(e)
        return redirect("/")

@app.route("/usrMainPage")
@isAdmin
@loginRequired
def usrMainPage():
    dbRec()
    dbcursor = db.cursor()
    print(Session)
    isAdmin = session.get("isAdmin", False)
    if isAdmin != True:
        # print("not admin")
        # print(isAdmin)
        dbcursor.execute("SELECT * FROM curso LEFT JOIN curso_check ON curso_check.cc_curs_id=curs_id WHERE cc_usr_id = %s", (session["usr_id"],))
        cursos = dbcursor.fetchall()
        # print(len(cursos))
        dbcursor.close()
        
        if len(cursos) > 0:
            return render_template("MainPageUsr.html", cursos=cursos)
        else:
            # print("No courses found")
            return render_template("MainPageUsr.html")
    else:
        print("ADMIN")
        dbcursor.execute("SELECT * FROM curso")
        cursos = dbcursor.fetchall()
        dbcursor.close()
        return render_template("MainPageUsr.html", cursos=cursos)

@app.route("/adminMainPage")
@loginRequired
@isAdminPage
def adminMainPage():
    return render_template("admPage.html")


## COURSE CREATION FUNCTIONS ##

@app.route("/classMCreate", endpoint="class_m_create", methods=["POST"])
@loginRequired
@isAdminPage
def classMCreate():
    dbRec()
    dbcursor = db.cursor()
    # New Class / Document
    clssTyp = request.form.get('type')

    if int(clssTyp) == 1: # 1 = Document/File
        clssNmb = request.form.get('classN')
        course = request.form.get('course')
        clssFile = request.files['docF']

        print(clssNmb)
        print(clssFile)
        print(clssFile.filename)

        #SQL
        dbcursor.execute("SELECT cur_name FROM curso WHERE curs_id = %s", (course,))
        crsNM = dbcursor.fetchone()
        crsNM = crsNM[0]

        crsNMB = crsNM.replace(' ', '_')

        dbcursor.execute("SELECT id FROM classes WHERE a_curs_id=%s AND c_a_id=%s", (course, clssNmb))
        clssMn = dbcursor.fetchone()
        clssMn = clssMn[0]

        # Sudden folder switch
        app.config['UPLOAD_FOLDER'] = 'static/assets/upload/cursos/{}'.format(crsNMB)
        filename = secure_filename(clssFile.filename)
        clssFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        objname = 'Mclass_{}'.format(clssMn)

        #con = sqlite3.connect("static/assets/upload/cursos/classL.db")
        #print('CON IS: {}'.format(con))
        #concur = con.cursor()

        #concur.execute("CREATE TABLE ?(numID integer primary key, file boolean, content, doc)", crsNM)
        dbcursor.close()
        

        """
        with open('static/assets/upload/cursos/{}/{}.py'.format(crsNMB, crsNMB), "r+") as file:
            fileR = file.readlines(0)
            file.seek(0)
            for i in fileR:
                if objname not in i:
                    print('NOT IN I')
                    print('obj: \n', objname)
                    print('I: \n', i)
                    file.write(i)
                elif objname in i:
                    iNew = i.replace("False", "True")
                    iNew = iNew[:-1]
                    iNew = iNew + ', "{}")'.format(filename)
                    print('LINE OLD:', i)
                    print('LINE NEW:', iNew)
                    file.write(iNew)
            file.truncate()
        """
        return redirect("/coursePgRdr/{}/1".format(course))

    elif int(clssTyp) == 0: # 0 = Link
        course = request.form.get('course')
        clssLink = request.form.get('link')
        clssTitle = request.form.get('classtitle0')
        clssFile = request.files['docF']

        print(clssLink)
        clssLink = ytEMB(clssLink)

        print(clssLink)
        print(clssTitle)


        #SQL

        dbcursor.execute("SELECT cur_name FROM curso WHERE curs_id = %s", (course,))
        crsNM = dbcursor.fetchone()
        crsNM = crsNM[0]

        crsNMB = crsNM.replace(' ', '_')

        dbcursor.execute("SELECT COUNT(a_id) FROM classes")
        a_idC = dbcursor.fetchone()
        a_idC = int(a_idC[0])

        print(a_idC)

        dbcursor.execute("SELECT COUNT(c_a_id) FROM classes WHERE a_curs_id = %s", (course,))
        c_a_idC = dbcursor.fetchone()
        c_a_idC = int(c_a_idC[0])

        dbcursor.execute(
            "INSERT INTO classes (a_id, c_a_id, cntnt, a_name, a_curs_id) VALUES(%s, %s, %s, %s, %s)",
            (
                a_idC + 1,
                c_a_idC + 1,
                ('{}'.format(crsNMB)),
                clssTitle,
                course,
            )
        )
        db.commit()

        dbcursor.execute(
            "SELECT * FROM classes WHERE a_id=%s", (a_idC + 1,)
        )
        idenC = dbcursor.fetchall()
        idenC = idenC[0]

        filename = secure_filename(clssFile.filename)
        print('YOURE LOOKING FOR ME:', filename)

        if (filename == None or filename == ''):
            file = open("static/assets/upload/cursos/{}/{}.py".format(crsNMB, crsNMB), "a")
            file.write('\nMclass_{} = ClssCnt(False, "{}")'.format(idenC[0], clssLink))
            file.close()
        else:
            clssFile.save(os.path.join('static/assets/upload/cursos/{}'.format(crsNMB), filename))

            file = open("static/assets/upload/cursos/{}/{}.py".format(crsNMB, crsNMB), "a")
            file.write('\n\nMclass_{} = ClssCnt(True, "{}", "{}")'.format(idenC[0], clssLink, filename))
        
        dbcursor.close()
        
        return redirect("/coursePgRdr/{}/1".format(course))
    
    else:
        dbcursor.close()
        db.close
        return '????'

@app.route("/classMDel", endpoint="class_m_del", methods=["POST"])
@loginRequired
@isAdminPage
def classMDel():
    dbRec()
    dbcursor = db.cursor()
    classI = request.form['id']
    # List
    # 1 - DELETE MYSQL ROW
    dbcursor.execute("SELECT * FROM classes WHERE id=%s", (classI,))
    idE = dbcursor.fetchone()
    idE_ac = idE[2]
    print(len(idE))

    if len(idE) > 0:
        dbcursor.execute("DELETE FROM classes WHERE id=%s", (classI,))
    # 2 - REALIGN ROWS
        dbcursor.execute("UPDATE classes SET a_id = a_id - 1 WHERE a_id > %s", (idE_ac,))
        dbcursor.execute("UPDATE classes SET c_a_id = c_a_id - 1 WHERE c_a_id > %s", (idE_ac,))
        db.commit()
        dbcursor.close()
        
    # 3 - DELETE FILES ?
        idE_cN = str(idE[3][:-3])

        module_name = "static.assets.upload.cursos.{}.{}".format(idE_cN, idE_cN)
        objname = 'Mclass_{}'.format(idE[0])
        module = from_module_get(module_name, objname)

        if module.file == True:
            fileC = os.path.isfile('static/assets/upload/cursos/{}/{}'.format(idE_cN, module.doc))
            if fileC == True:
                os.remove('static/assets/upload/cursos/{}/{}'.format(idE_cN, module.doc))
            else:
                return "File Deletion Failed : {}, {}, {}".format(objname, module.file, module.doc)

    # 4 - DELETE FROM PY FILE
        with open('static/assets/upload/cursos/{}/{}.py'.format(idE_cN, idE_cN), "r+") as file:
            fileR = file.readlines(0)
            file.seek(0)
            hasF = False # So we dont have blank spaces in the course py file // Frontend now finally
            for i in fileR:
                if hasF == False:
                    if objname not in i:
                        file.write(i)
                    else:
                        hasF = True
                else:
                    hasF = False
            file.truncate()
    return "OK"

@app.route("/coursMEdit", endpoint="cours_m_edit", methods=["POST"])
@loginRequired
@isAdminPage
def coursMEdit():
    dbRec()
    dbcursor = db.cursor()
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
    dbcursor.close()
    
    return redirect("/coursMList")

@app.route("/coursMList", endpoint="cours_m_list", methods=["GET"])
@loginRequired
@isAdminPage
def coursMList():
    dbRec()

    dbcursor = db.cursor()

    dbcursor.execute("SELECT * FROM curso")
    cursos = dbcursor.fetchall()
    print("CURSOS: {}".format(cursos))

    dbcursor.execute("SELECT COUNT(*) FROM curso")
    cursoC = dbcursor.fetchone()
    print("CURSOS COUNT : {}".format(cursoC))

    dbcursor.close()

    return render_template("/cursos/coursPageCreate.html", cursos=cursos, cursoC=cursoC, cursoCs = 100 + int((cursoC[0]) * 2) )


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
    if newCrsNames == None or newCrsNames == '':
        return pageApology("None type detection", 400)
    print("New Course Rows:", newCrsNames, newCrsProfs, newCrsPrices)

    dbRec()
    dbcursor = db.cursor()
    try:
        for i, name in enumerate(newCrsNames):
            if (name == ''):
                break
            else:
                # Take out extra spaces accidentaly typed
                name = name.strip()
                nameB = name.replace(' ', '_')

                checkF = os.path.isdir('templates/cursos/curpages/{}'.format(nameB))
                checkF1 = os.path.isdir('static/assets/upload/cursos/{}'.format(nameB))

                

                dbcursor.execute("SELECT cur_name FROM curso WHERE cur_name=%s", (name,))
                chkCrsEx = dbcursor.fetchone()

                if (chkCrsEx is None) or (len(chkCrsEx) < 1):
                    print("VALUES ABOUT TO BE INSERTED")
                    print(newCsrIds[i])
                    print(name)
                    print(newCrsProfs[i])
                    print(newCrsPrices[i])

                    dbcursor.execute(
                        "INSERT INTO curso (curs_id, cur_name, prof, curs_price) VALUES(%s, %s, %s, %s)",
                        (
                            newCsrIds[i],
                            name,
                            newCrsProfs[i],
                            newCrsPrices[i],
                        )
                    )

                    db.commit()
                    
                else:
                    print("Catch_ERROR[crsCreate]: {} already is registered as a course".format(name))
                
                # Better to do this after so if the database injection fails we dont create unecessary files
                if (checkF == False):
                    break
                    os.mkdir('templates/cursos/curpages/{}'.format(nameB))
                    file = open('templates/cursos/curpages/{}/{}.html'.format(nameB, nameB), 'x')
                    file.write(dynamicHTMLS.exHtml)
                if (checkF1 == False):
                    break
                    os.mkdir('static/assets/upload/cursos/{}'.format(nameB))
    except Exception as e:
        dbcursor.ping(reconnect=True)
        print(Back.YELLOW + 'coursMCREATE EXCEPTION : {}'.format(e))
        print("coursMCREATE commit failure attempting reconnection." + Style.re)
    finally:
        dbcursor.close()
        return redirect("/coursMList")


@app.route("/deleteCourse", endpoint="cours_single_delete", methods=["POST"])
@loginRequired
@isAdminPage
def deleteCourse():
    dbRec()
    dbcursor = db.cursor()
    id = request.form.get("id")

    dbcursor.execute("SELECT * FROM classes WHERE a_curs_id=%s", (id,))
    clsEX = dbcursor.fetchone()

    dbcursor.execute("DELETE FROM classes WHERE a_curs_id=%s", (id,))
    db.commit()

    dbcursor.execute("SELECT cur_name FROM curso WHERE curs_id = %s", (id,))
    curNM = dbcursor.fetchone()
    curNM = curNM[0]

    curNMB = curNM.replace(' ', '_')

    dbcursor.execute("DELETE FROM curso_check WHERE cc_curs_id = %s", ((id, )))
    db.commit()

    dbcursor.execute("DELETE FROM curso WHERE curs_id = %s", ((id,)))
    db.commit()

    # decrement ids bigger than deleted id
    dbcursor.execute("UPDATE curso SET curs_id = curs_id - 1 WHERE curs_id > %s", ((id,)))
    db.commit()

    checkF = os.path.isdir('templates/cursos/curpages/{}'.format(curNMB))
    if (checkF == True):
        shutil.rmtree('templates/cursos/curpages/{}'.format(curNMB), ignore_errors=True)

    checkF = os.path.isdir('static/assets/upload/cursos/{}'.format(curNMB))
    if (checkF == True):
        shutil.rmtree('static/assets/upload/cursos/{}'.format(curNMB), ignore_errors=True)
    
    dbcursor.close()
    
    return redirect("/coursMList")


@app.route("/coursePgRdr/<course>/<clss>", endpoint="cours_redir_pg", methods=["GET"])
@loginRequired
def coursePgRdr(course, clss:1):
    dbRec()
    dbcursor = db.cursor()
    if session["isAdmin"] == False:
        dbcursor.execute("SELECT * FROM curso_check WHERE cc_curs_id=%s AND cc_usr_id=%s", (course, session["usr_id"]))
        chkU = dbcursor.fetchone()
        chkU = chkU # Check later if its necessary but just to avoid mysql delaying stuff
        if chkU is None:
            dbcursor.close()
            
            return redirect("/usrMainPage")

    dbcursor.execute("SELECT cur_name FROM curso WHERE curs_id = %s", ((course,))) # originally crs
    crsName = dbcursor.fetchone()
    crsName = str(crsName[0])

    crsNameB = crsName.replace(' ', '_')

    dbcursor.execute("SELECT * FROM classes WHERE a_curs_id=%s AND c_a_id=%s", (course, clss))
    clssCNT = dbcursor.fetchall()

    checkF = os.path.isfile('templates/cursos/curpages/{}/{}.html'.format(crsNameB, crsNameB))
    if (checkF):
        dbcursor.execute("SELECT * FROM classes WHERE a_curs_id = %s", ((course, )))
        aulas = dbcursor.fetchall()
        aulas = aulas # fixes the bug for deleted classes still appearing

        dbcursor.close()
        

        if (len(clssCNT) > 0):
            clssCNT = clssCNT[0]

            module_name = "static.assets.upload.cursos.{}.{}".format(crsNameB, crsNameB)
            objname = 'Mclass_{}'.format(clssCNT[0])

            module = from_module_get(module_name, objname)

            fPath = '/static/assets/upload/cursos/{}/{}'.format(crsNameB, module.doc)

            
            if (module.file == True):
                return render_template("/cursos/curpages/{}/{}.html".format(crsNameB, crsNameB), crsName=crsName, aulas=aulas, course=course, clss=clss, isFile=module.file, cPath=module.content, fPath=fPath, noClasses=False)
            else:
                return render_template("/cursos/curpages/{}/{}.html".format(crsNameB, crsNameB), crsName=crsName, aulas=aulas, course=course, clss=clss, isFile=module.file, cPath=module.content, noClasses=False)
        else:
            return render_template("/cursos/curpages/{}/{}.html".format(crsNameB, crsNameB), crsName=crsName,isFile=False, aulas=aulas, course=course, noClasses=True)
    else:
        dbcursor.close()
        
        return render_template("/cursos/curpages/curNoN.html")



# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    dbRec()
    dbcursor = db.cursor()
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
            session["email"] = row[2]

            dbcursor.close()
            

            return redirect("/")
    else:
        dbcursor.close()
        
        return render_template("login.html")

## ADMIN REGISTER EDIT USER FUNCTIONS ##

@app.route("/usrMList", endpoint="usr_m_list", methods=["GET"])
@loginRequired
@isAdminPage
def usrMList():
    dbRec()
    dbcursor = db.cursor()
    dbcursor.execute("SELECT * FROM user")
    alunos = dbcursor.fetchall()
    dbcursor.execute("SELECT COUNT(*) FROM user")
    alunoC = dbcursor.fetchall()
    dbcursor.execute("SELECT cur_name, curs_id FROM curso")
    cursosN = dbcursor.fetchall()
    dbcursor.execute("SELECT * FROM curso_check ORDER BY cc_curs_id")
    varDCC = dbcursor.fetchall()

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

    print("New Course Rows: ", newUsrNames)

    dbRec()
    dbcursor = db.cursor()
    db.autocommit = False
    try:
        for i, ids in enumerate(newUsrIds):
            if (newUsrNames[i] == None or newUsrNames[i] == ''):
                newUsrNames[i] = 'NULL'
            print('649 newIDS : {}'.format(newUsrIds[i]))
            print('650 newNames: {}'.format({newUsrNames[i]}))
            print('651 newEMAILS: {}'.format({newUsrEmail[i]}))
            dbcursor.execute(
                "INSERT INTO user (usr_id, username, user_email, password, cpf, contact_number, reg_date, reg_time, active_status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    ids,
                    newUsrNames[i],
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
    except Exception as e:
        print('674 EXCEPTION ' + e)
        print("675 commit failure attempting reconnection.")
        db.ping(reconnect=True)
        if db.is_connected() == False:
            print(" 678 Reconnection failed.")
        else:
            print("680 Database RECONECTED now to the cursor")
    finally:
        db.commit()
        db.autocommit = True
        dbcursor.close()
        
        
        return redirect("/usrMList")


@app.route("/usrCRSreg", endpoint="usr_C_reg", methods=["POST"])
@loginRequired
@isAdmin
@isAdminPage
def usrCRSreg():
    dbRec()
    dbcursor = db.cursor()
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
    dbcursor.close()
    
    return ("request...")

@app.route("/deleteUser", endpoint="usr_del_reg", methods=["POST"])
@loginRequired
@isAdmin
@isAdminPage
def deleteUser():
    dbRec()
    dbcursor = db.cursor()
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
        dbcursor.close()
        

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
        if session["usr_id"] in idray:
            session.clear()
        else:
            print("session is not in idray")
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
        dbcursor.close()
        
    return redirect("/usrMList")


# NOT DONE supposed to log out users who have been deleted to avoid further errors in database
# and also avoid stuff like people logging into old ids (scary)
@loginRequired
def sndLogoutRq(id, detnmb = False):
    dbRec()
    dbcursor = db.cursor()
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
    dbRec()
    dbcursor = db.cursor()
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
    dbcursor.close()
    
    return redirect("/usrMList")



## USER LOGIN FUNCTIONS ##


# Register
@app.route("/register", methods=["GET", "POST"])
def register():   
    dbRec()
    dbcursor = db.cursor() 
    if request.method == "POST":
        dbcursor.execute("SELECT COUNT(usr_id) FROM user")
        uCnt = dbcursor.fetchone()
        uCnt = uCnt[0]
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
        

        #elif not f_CPF or f_CPF.isalpha():
        #   return pageApology("Providencie CPF válido", 400)

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
                        "INSERT INTO user (usr_id, username, password, cpf, user_email, contact_number, reg_date, reg_time, active_status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (
                                uCnt + 1,
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
                    dbcursor.close()
                    
                    return redirect("/")
    # GET
    else:
        dbcursor.close()
        
        return render_template("register.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/") 




