import hashlib
from flask import Flask, render_template, request, redirect, url_for, session
# import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "fasfafs"

# db_config = {
#     "host": "sql6.freemysqlhosting.net",
#     "user": "sql6641285",
#     "password": "MjvvFvMMnn",
#     "database": "sql6641285"
# }

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345678"
app.config["MYSQL_DB"] = "allinonedb"

mysql = MySQL(app)

first_login = True

def encrypt(dencrypt):
    encrypt = str(hashlib.md5(dencrypt.strip().encode("utf-8")).hexdigest())
    encrypt = str(hashlib.sha1(encrypt.strip().encode("utf-8")).hexdigest())
    encrypt = str(hashlib.sha1(encrypt.strip().encode("utf-8")).hexdigest())
    encrypt = str(hashlib.md5(encrypt.strip().encode("utf-8")).hexdigest())
    
    return encrypt

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    warning = False
    
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = str(request.form["username"])
        password = str(request.form["password"])
        
        password = encrypt(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password, ))
        user = cursor.fetchone()
        
        cursor.close()
        
        if user:
            
            if user["user_status_id"] == 1:
                session["loggedin"] = True
                session["name"] = user["name"]
                session["username"] = user["username"]
                session["user_role_id"] = user["user_role_id"]
                session["update_success"] = None
                if user["user_role_id"] == 1:
                    return redirect(url_for("admin"))
                    
                elif user["user_role_id"] == 2:
                    return redirect(url_for("member_index"))
                    
                elif user["user_role_id"] == 3:
                    return redirect(url_for("index"))
                    
            msg = "Tài khoản bị vô hiệu hóa!"
            warning=True
            return render_template("login.html", msg=msg, warning=warning)
            
        else:
            msg = "Nhập sai mật khẩu hoặc tài khoản"
            warning=True
            return render_template("login.html", msg=msg, warning=warning)

    elif request.method == "GET" and "loggedin" in session:
        session.pop("loggedin", None)
        session.pop("id", None)
        session.pop("username", None)
        session.pop("user_role_id", None)
        session.pop("update_success", None)
        msg = "Thoát tài khoản thành công!"
        return render_template("login.html", msg=msg, warning=warning)
    
    return render_template("login.html")


@app.route("/login/<username>/<password>", methods=["GET", "POST"])
def url_login(username, password):
    msg = ""
    warning = False
    
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT username FROM users")
        usernames = cursor.fetchall()
        username_bool = False
        encrypt_username = ""
        
        for dencrypt_username in usernames:
            dencrypt_username = str(dencrypt_username["username"])
            encrypt_username = str(hashlib.md5(dencrypt_username.strip().encode("utf-8")).hexdigest())
            encrypt_username = str(hashlib.sha1(encrypt_username.strip().encode("utf-8")).hexdigest())
            encrypt_username = str(hashlib.sha1(encrypt_username.strip().encode("utf-8")).hexdigest())
            encrypt_username = str(hashlib.md5(encrypt_username.strip().encode("utf-8")).hexdigest())
            
            if encrypt_username == username:
                username_bool = True
                break
            
        if username_bool:
            cursor.execute("SELECT u.username, u.name, u.user_role_id, u.user_status_id FROM users AS u WHERE u.username = %s AND u.password = %s", (dencrypt_username, str(password), ))
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                
                if user["user_status_id"] == 1:
                    session["loggedin"] = True
                    session["name"] = user["name"]
                    session["username"] = user["username"]
                    session["user_role_id"] = user["user_role_id"]
                    session["update_success"] = None
                if user["user_role_id"] == 1:
                    return redirect(url_for("admin"))
                    
                elif user["user_role_id"] == 2:
                    return redirect(url_for("member_index"))
                    
                elif user["user_role_id"] == 3:
                    return redirect(url_for("index"))
                    
                msg = "Tài khoản bị vô hiệu hóa!"
                warning=True
                return render_template("login.html", msg=msg, warning=warning)
            
            else:
                msg = "Nhập sai mật khẩu hoặc tài khoản"
                warning=True
                return render_template("login.html", msg=msg, warning=warning)
        
        return render_template("404.html")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    global first_login
    first_login = True
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    msg = ""
    warning = False
    global first_login
    
    if "loggedin" in session and session["user_role_id"] == 1:
        if first_login:
            msg = "Đăng nhập thành công! Chào, " + session["name"]
            first_login = False
        return render_template("admin/index.html", msg=msg, warning=warning)
        
    return redirect(url_for("logout"))

@app.route("/member_index")
def member_index():
    msg = ""
    warning = False
    global first_login
    
    if "loggedin" in session and session["user_role_id"] == 2:
        if first_login:
            msg = "Đăng nhập thành công! Chào, " + session["name"]
            first_login = False
        return render_template("member/index.html", msg=msg, warning=warning)
    
    return redirect(url_for("logout"))
    
@app.route("/index")
def index():
    msg = ""
    warning = False
    global first_login
    
    if "loggedin" in session and session["user_role_id"] == 3 : 
        if first_login:
            msg = "Đăng nhập thành công! Chào, " + session["name"]
            first_login = False
        return render_template("guest/index.html", msg=msg, warning=warning)
    
    return redirect(url_for("logout"))


@app.route("/create-login-url/<username>/<password>", methods=["GET", "POST"])
def create_login_url(username, password):
    msg = ""
    count_users = ""
    warning = False
    users = []
    limit = 10
    column = ""
    order = ""
    url = None
    
    if "loggedin" in session and session["user_role_id"] == 1:
        if "count_user_option" in request.form:
            session["count_user_option"] = int(request.form["count_user_option"])
            
        if "count_user_option" in session:
            limit = session["count_user_option"]
        else:
            limit = 10
        
        offset = 1

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        encrypt_username = str(hashlib.md5(username.strip().encode("utf-8")).hexdigest())
        encrypt_username = str(hashlib.sha1(encrypt_username.strip().encode("utf-8")).hexdigest())
        encrypt_username = str(hashlib.sha1(encrypt_username.strip().encode("utf-8")).hexdigest())
        encrypt_username = str(hashlib.md5(encrypt_username.strip().encode("utf-8")).hexdigest())
        
        base_url = request.base_url
        url = base_url.replace("create-login-url/" + username + "/" + password, "login/") + encrypt_username + "/" + password
    
        return url, session
        
    return url, render_template("users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)

@app.route("/users", methods=["GET", "POST"])
def get_users():
	msg = ""
	count_users = ""
	warning = False
	users = []
	column = ""
	order = ""
	session["update_success"] = None
	


	if "loggedin" in session and session["user_role_id"] == 1:

		if request.method == "POST":
			if "count_user_option" in request.form:
				session["count_user_option"] = int(request.form["count_user_option"])
			
		if "count_user_option" in session:
			limit = session["count_user_option"]
		else:
			limit = 10
		
		offset = 1

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT COUNT(*) AS count_users FROM users;"
		cursor.execute(query)
		count_users = cursor.fetchone()	

		query = "SELECT u.username, u.password, u.name, ur.name AS 'user_role', us.name AS 'user_status', u.description FROM users AS u, user_roles AS ur, user_status AS us WHERE u.user_role_id = ur.id AND u.user_status_id = us.id LIMIT %s, %s;"
		cursor.execute(query, (offset, limit, ))
		users = cursor.fetchall()
        
		return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)

	return redirect(url_for("logout"))

@app.route("/edit-user/<key>/<username>/<value>", methods=["POST"])
def edit_user(key, username, value):
    msg = ""
    count_users = ""
    warning = False
    users = []
    session["update_success"] = None
    
    if "loggedin" in session and session["user_role_id"] == 1:
        if request.method == "POST":
            if "count_user_option" in request.form:
                session["count_user_option"] = int(request.form["count_user_option"])
                
        if "count_user_option" in session:
            limit = session["count_user_option"]
        else:
            limit = 10
            
        offset = 1
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) AS count_users FROM users;"
        cursor.execute(query)
        count_users = cursor.fetchone()	
        
        query = "SELECT u.username, u.password, u.name, ur.name AS 'user_role', us.name AS 'user_status', u.description FROM users AS u, user_roles AS ur, user_status AS us WHERE u.user_role_id = ur.id AND u.user_status_id = us.id LIMIT %s, %s;"
        cursor.execute(query, (offset, limit, ))
        users = cursor.fetchall()
        
        if key == "user_status":
            query = "SELECT us.id FROM user_status AS us WHERE us.name = %s;"
            cursor.execute(query, (value, ))
            new_user_status_id = cursor.fetchone()	
            
            query = "UPDATE users SET user_status_id = %s WHERE username = %s;"
            cursor.execute(query , (new_user_status_id['id'], username, ))
            mysql.connection.commit()
            
            msg = "Đã cập nhật user status!"
            session["update_success"] = True
            
        elif key == "name":
            query = "UPDATE users SET name = %s WHERE username = %s;"
            cursor.execute(query , (value, username, ))
            mysql.connection.commit()
            
            msg = "Đã cập nhật name!"
            session["update_success"] = True
            
        elif key == "user_role":
            query = "SELECT ur.id FROM user_roles AS ur WHERE ur.name = %s;"
            cursor.execute(query, (value, ))
            new_user_role_id = cursor.fetchone()	
            
            query = "UPDATE users SET user_role_id = %s WHERE username = %s;"
            cursor.execute(query , (new_user_role_id['id'], username, ))
            mysql.connection.commit()
            
            msg = "Đã cập nhật user role!"
            session["update_success"] = True
            
        elif key == "description":
            if value == "None":
                value = None
            query = "UPDATE users SET description = %s WHERE username = %s;"
            cursor.execute(query , (value, username, ))
            mysql.connection.commit()
            
            msg = "Đã cập nhật description!"
            session["update_success"] = True
            
        cursor.close()
        return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)
    
    session["update_success"] = False
    msg = "Không có quyền truy cập!!!"
    warning = True
    return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)

# if __name__ == "__main__":
#     app.run(debug=True)