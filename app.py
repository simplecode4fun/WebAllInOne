import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import mysql.connector
from  flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import requests


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

def get_user_ip():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    return data.get('ip', 'Unknown')

def select_user_log(cursor):
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM users;"
    cursor.execute(query)
    user_log = cursor.fetchall()
    
    # cursor.close()
    return user_log

def insert_user_log():
    username = session["username"]
    current_datetime = datetime.now()  
    log_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    user_ip = get_user_ip()
    description = None

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "INSERT INTO user_log VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (username, log_datetime, user_ip, description, ))
    mysql.connection.commit()
    
    cursor.close()


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
                session["username"] = user["username"]
                session["name"] = user["name"]
                session["user_role_id"] = user["user_role_id"]
                session["count_user_option"] = "ALL"
                session["update_success"] = None

                insert_user_log()
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
        session.pop("name", None)
        session.pop("username", None)
        session.pop("user_role_id", None)
        session.pop("update_success", None)
        session.pop("count_user_option", None)
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
                    session["count_user_option"] = "ALL"
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
        return render_template("member/index.html", msg=msg, warning=warning, name=session["name"])
        
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
        return render_template("member/index.html", msg=msg, warning=warning, name=session["name"])
    
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
        return render_template("member/index.html", msg=msg, warning=warning, name=session["name"])
    
    return redirect(url_for("logout"))


@app.route("/create-login-url/<username>/<password>", methods=["GET", "POST"])
def create_login_url(username, password):
    msg = ""
    count_users = ""
    warning = False
    users = []
    limit = "ALL"
    column = ""
    order = ""
    url = None
    
    if "loggedin" in session and session["user_role_id"] == 1:
        if "count_user_option" in request.form:
            session["count_user_option"] = str(request.form["count_user_option"])
            
        if "count_user_option" in session:
            limit = session["count_user_option"]
        else:
            limit = "ALL"
        
        offset = 1

        encrypt_username = str(hashlib.md5(username.strip().encode("utf-8")).hexdigest())
        encrypt_username = str(hashlib.sha1(encrypt_username.strip().encode("utf-8")).hexdigest())
        encrypt_username = str(hashlib.sha1(encrypt_username.strip().encode("utf-8")).hexdigest())
        encrypt_username = str(hashlib.md5(encrypt_username.strip().encode("utf-8")).hexdigest())
        
        base_url = request.base_url
        url = base_url.replace("create-login-url/" + username + "/" + password, "login/") + encrypt_username + "/" + password
    
        return url, session
        
    return url, render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)

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
                session["count_user_option"] = str(request.form["count_user_option"])
                
        if "count_user_option" in session:
            limit = session["count_user_option"]
        else:
            limit = "ALL"
            
        offset = 0
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) AS count_users FROM users;"
        cursor.execute(query)
        count_users = cursor.fetchone()	
        
        if limit == "ALL":
            query = "SELECT u.username, u.password, u.name, ur.name AS 'user_role', us.name AS 'user_status', u.add_date, u.description FROM users AS u, user_roles AS ur, user_status AS us WHERE u.user_role_id = ur.id AND u.user_status_id = us.id ORDER BY u.add_date DESC;"
            cursor.execute(query)
        else:
            query = "SELECT u.username, u.password, u.name, ur.name AS 'user_role', us.name AS 'user_status', u.add_date, u.description FROM users AS u, user_roles AS ur, user_status AS us WHERE u.user_role_id = ur.id AND u.user_status_id = us.id ORDER BY u.add_date DESC LIMIT %s, %s;"
            cursor.execute(query, (offset, int(limit) - 1, ))
        users = cursor.fetchall()
        
        # user_log = select_user_log(cursor)
        query = "SELECT * FROM users;"
        cursor.execute(query)
        user_log = cursor.fetchall()
        
        return render_template("admin/users.html", msg=msg, warning=warning, name=session["name"],  users=users, user_log=user_log, count_users=count_users, count_user_option=limit)
    
    return redirect(url_for("logout"))

@app.route("/edit-user/<key>/<username>/<value>", methods=["POST", "GET"])
def edit_user(key, username, value):
    msg = ""
    count_users = ""
    warning = False
    users = []
    session["update_success"] = None
    
    if "loggedin" in session and session["user_role_id"] == 1:
        if request.method == "POST":
            if "count_user_option" in request.form:
                session["count_user_option"] = str(request.form["count_user_option"])
                
        if "count_user_option" in session:
            limit = session["count_user_option"]
        else:
            limit = "ALL"
            
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

# @app.route("/add-user/<username>/<password>/<name>/<user_role_id>/<user_status_id>/<description>", methods=["POST", "GET"])
# def add_user(username, password, name, user_role_id, user_status_id, description):
@app.route("/add-user", methods=["POST", "GET"])
def add_user():
    msg = ""
    count_users = ""
    warning = False
    users = []
    session["update_success"] = None
    limit = "ALL" 

    # username = user["username"]
    # password = user["password"]
    # name = user["name"]
    # user_role_id = user["user_role_id"]
    # user_status_id = user["user_status_id"]
    # description = user["description"]
    # data = request.json  # Lấy dữ liệu từ request body
    # username = data["username"]
    # password = data["password"]
    # name = data["name"]
    # user_role_id = data["user_role_id"]
    # user_status_id = data["user_status_id"]
    # description = data["description"]
    
   
    if "loggedin" in session and session["user_role_id"] == 1:
        if request.method == "POST" and "username" in request.form and "password" in request.form and "name" in request.form and "user-role" in request.form:

            

            username = str(request.form["username"])
            password = str(request.form["password"])
            name = str(request.form["name"])
            user_role_id = str(request.form["user-role"])
            user_status_id = 1
            
            
            if "description" in request.form:
                description = str(request.form["description"])
                if description == "":
                    description = None
            
            current_datetime = datetime.now()   
            add_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            if "count_user_option" in request.form:
                session["count_user_option"] = str(request.form["count_user_option"])
                
            if "count_user_option" in session:
                limit = session["count_user_option"]
            else:
                limit = "ALL"    
            offset = 1
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT COUNT(*) AS count_users FROM users;"
            cursor.execute(query)
            count_users = cursor.fetchone()	
            
            if limit == "ALL":
                query = "SELECT u.username, u.password, u.name, ur.name AS 'user_role', us.name AS 'user_status', u.description, u.add_date FROM users AS u, user_roles AS ur, user_status AS us WHERE u.user_role_id = ur.id AND u.user_status_id = us.id;"
                cursor.execute(query)
            else:
                query = "SELECT u.username, u.password, u.name, ur.name AS 'user_role', us.name AS 'user_status', u.description, u.add_date FROM users AS u, user_roles AS ur, user_status AS us WHERE u.user_role_id = ur.id AND u.user_status_id = us.id LIMIT %s, %s;"
                cursor.execute(query, (offset, int(limit - 1), ))
            users = cursor.fetchall()
            
            query = "SELECT u.username FROM users AS u WHERE u.username = %s;"
            cursor.execute(query, (username, ))
            find_username = cursor.fetchone()	
            
            if find_username:
                msg = "Username đã tồn tại!!!"
                warning = True
                return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)
            else:
                query = "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (username, password, name, user_role_id, user_status_id, add_date, description, ))
                mysql.connection.commit()
            
                msg = "Đã tạo user " + username

                return redirect(url_for('get_users'))
                
                # return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)

        msg = "Nhập đầy đủ thông tin để tạo user!!!"
        warning = True
        return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)
    
    session["update_success"] = False
    msg = "Không có quyền truy cập!!!"
    warning = True
    return render_template("admin/users.html", msg=msg, warning=warning, users=users, count_users=count_users, count_user_option=limit)

@app.route("/productss")
def get_productss():
    msg = ""
    count_products = ""
    warning = False
    users = []
    column = ""
    order = ""
    session["update_success"] = None
    
    if "loggedin" in session and session["user_role_id"] == 1:
        
        if request.method == "POST":
            if "count_product_option" in request.form:
                session["count_product_option"] = str(request.form["count_product_option"])
                
        if "count_product_option" in session:
            limit = session["count_product_option"]
        else:
            limit = "ALL"
            
        offset = 0
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) AS count_products FROM products;"
        cursor.execute(query)
        count_products = cursor.fetchone()	
        
        if limit == "ALL":
            # Set group_concat_max_len
            # set_group_concat = "SET SESSION group_concat_max_len = 1000000;"
            # cursor.execute(set_group_concat)

            # # Get pivot columns
            # get_pivot_cols = """
            #     SELECT GROUP_CONCAT(DISTINCT CONCAT('MAX(CASE WHEN c.name = ', QUOTE(c.name), ' THEN c.class END) AS ', QUOTE(REPLACE(c.name, ' ', '_'))) ) AS pivot_cols
            #     FROM classes c;
            # """
            # cursor.execute(get_pivot_cols)
            # pivot_cols_result = cursor.fetchone()
            
            # pivot_cols = pivot_cols_result['pivot_cols'] if pivot_cols_result else ""

            # Construct and execute main query
            # main_query = """
            #     SELECT GROUP_CONCAT(
            #         DISTINCT CONCAT('`', c.name, '`')
            #     ) AS pivot_cols 
            #     FROM classes c;
            # """

            # cursor.execute(main_query)
            # pivot_cols_result = cursor.fetchone()
            # pivot_cols = pivot_cols_result["pivot_cols"]

            # pivot_select_query = """
            #     SELECT GROUP_CONCAT(
            #         DISTINCT CONCAT(
            #             'MAX(CASE WHEN c.name = ''', c.name, ''' THEN c.class END) AS `', REPLACE(c.name, ' ', '_'), '`'
            #         )
            #     ) AS pivot_select
            #     FROM classes c;
            # """

            # cursor.execute(pivot_select_query)
            # pivot_select_result = cursor.fetchone()
            # pivot_select = pivot_select_result["pivot_select"]

            # query = f"""
            #     SELECT p.id, cat.name AS category, p.name AS product, p.price, p.shop_price, p.quantity, p.image_link, p.link, s.name AS shop, p.purchase_date, p.receipt_date, p.description,
            #     {pivot_select}
            #     FROM products p, categories cat, classes c, shops s 
            #     WHERE p.category_id = cat.id AND p.id = c.product_id AND p.shop_id = s.id 
                
            #     ORDER BY p.id DESC;
            # """

            query = '''
                SELECT
                    p.id,
                    cat.name AS category,
                    p.name AS product,
                    p.price,
                    p.shop_price,
                    p.quantity,
                    p.image_link,
                    p.link,
                    s.name AS shop,
                    s.link AS shop_link,
                    p.purchase_date,
                    p.receipt_date,
                    p.description,
                    IFNULL(
                        (
                            SELECT GROUP_CONCAT(
                                DISTINCT CONCAT(c.name, ': ', c.class)
                                SEPARATOR ' - '
                            )
                            FROM classes c
                            WHERE c.product_id = p.id
                        ),
                        NULL
                    ) AS class
                FROM
                    products p
                LEFT JOIN
                    categories cat ON p.category_id = cat.id
                LEFT JOIN
                    shops s ON p.shop_id = s.id
                GROUP BY
                    p.id
                ORDER BY
                    p.id DESC;

            '''
            cursor.execute(query)
            products = cursor.fetchall()
            print(products)
        else:
            query = "SET SESSION group_concat_max_len = 1000000; SELECT GROUP_CONCAT(DISTINCT CONCAT( 'MAX(CASE WHEN c.name = ''', c.name, ''' THEN c.class END) AS ', REPLACE(c.name, ' ', '_') ) ) INTO @pivot_cols FROM classes c; SET @query = CONCAT( 'SELECT p.id, cat.name AS category_name, p.name AS product_name, ', @pivot_cols, ', p.price, p.shop_price, p.quantity, p.image_link, p.link, s.name AS shop_name, p.purchase_date, p.receipt_date,  p.description FROM products p LEFT JOIN categories cat ON p.category_id = cat.id LEFT JOIN classes c ON p.id = c.product_id LEFT JOIN shops s ON p.shop_id = s.id GROUP BY p.id ORDER BY p.id DESC LIMIT %s, %s;' ); PREPARE stmt FROM @query; EXECUTE stmt; DEALLOCATE PREPARE stmt;"
            cursor.execute(query, (offset, int(limit) - 1, ))
        # products = cursor.fetchall()
        # print(products)
        
        # user_log = select_user_log(cursor)
        # query = "SELECT * FROM users;"
        # cursor.execute(query)
        # user_log = cursor.fetchall()
        response = {
            'products': products,
            'count_products': count_products,
            'count_product_option': limit
        }
        
        return jsonify(response)
        # count_products=count_products
        # count_product_option=limit
        # return jsonify(products, count_products, count_product_option)
        
    #     return render_template("products.html",name=session["name"], products=products, count_products=count_products, count_product_option=limit)
    
    # return render_template("products.html",name=session["name"], products=products, count_products=count_products, count_product_option=limit)


@app.route("/products", methods=["GET", "POST"])
def get_products():
    msg = ""
    count_products = ""
    warning = False
    users = []
    column = ""
    order = ""
    session["update_success"] = None
    
    if "loggedin" in session and (session["user_role_id"] == 1 or session["user_role_id"] == 2):
        
        # if request.method == "POST":
        #     if "count_product_option" in request.form:
        #         session["count_product_option"] = str(request.form["count_product_option"])
                
        # if "count_product_option" in session:
        #     limit = session["count_product_option"]
        # else:
        #     limit = "ALL"
            
        # offset = 0
        
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # query = "SELECT COUNT(*) AS count_products FROM products;"
        # cursor.execute(query)
        # count_products = cursor.fetchone()	
        
        # if limit == "ALL":
        #     # Set group_concat_max_len
        #     # set_group_concat = "SET SESSION group_concat_max_len = 1000000;"
        #     # cursor.execute(set_group_concat)

        #     # # Get pivot columns
        #     # get_pivot_cols = """
        #     #     SELECT GROUP_CONCAT(DISTINCT CONCAT('MAX(CASE WHEN c.name = ', QUOTE(c.name), ' THEN c.class END) AS ', QUOTE(REPLACE(c.name, ' ', '_'))) ) AS pivot_cols
        #     #     FROM classes c;
        #     # """
        #     # cursor.execute(get_pivot_cols)
        #     # pivot_cols_result = cursor.fetchone()
            
        #     # pivot_cols = pivot_cols_result['pivot_cols'] if pivot_cols_result else ""

        #     # Construct and execute main query
        #     main_query = """
        #         SELECT GROUP_CONCAT(
        #             DISTINCT CONCAT('`', c.name, '`')
        #         ) AS pivot_cols 
        #         FROM classes c;
        #     """

        #     cursor.execute(main_query)
        #     pivot_cols_result = cursor.fetchone()
        #     pivot_cols = pivot_cols_result["pivot_cols"]

        #     pivot_select_query = """
        #         SELECT GROUP_CONCAT(
        #             DISTINCT CONCAT(
        #                 'MAX(CASE WHEN c.name = ''', c.name, ''' THEN c.class END) AS `', REPLACE(c.name, ' ', '_'), '`'
        #             )
        #         ) AS pivot_select
        #         FROM classes c;
        #     """

        #     cursor.execute(pivot_select_query)
        #     pivot_select_result = cursor.fetchone()
        #     pivot_select = pivot_select_result["pivot_select"]

        #     query = f"""
        #         SELECT p.id, cat.name AS category, p.name AS product, p.price, p.shop_price, p.quantity, p.image_link, p.link, s.name AS shop, p.purchase_date, p.receipt_date, p.description,
        #         {pivot_select}
        #         FROM products p, categories cat, classes c, shops s 
        #         WHERE p.category_id = cat.id AND p.id = c.product_id AND p.shop_id = s.id 
        #         GROUP BY p.id 
        #         ORDER BY p.id DESC;
        #     """

        #     cursor.execute(query)
        #     products = cursor.fetchall()
        #     print(products)
        # else:
        #     query = "SET SESSION group_concat_max_len = 1000000; SELECT GROUP_CONCAT(DISTINCT CONCAT( 'MAX(CASE WHEN c.name = ''', c.name, ''' THEN c.class END) AS ', REPLACE(c.name, ' ', '_') ) ) INTO @pivot_cols FROM classes c; SET @query = CONCAT( 'SELECT p.id, cat.name AS category_name, p.name AS product_name, ', @pivot_cols, ', p.price, p.shop_price, p.quantity, p.image_link, p.link, s.name AS shop_name, p.purchase_date, p.receipt_date,  p.description FROM products p LEFT JOIN categories cat ON p.category_id = cat.id LEFT JOIN classes c ON p.id = c.product_id LEFT JOIN shops s ON p.shop_id = s.id GROUP BY p.id ORDER BY p.id DESC LIMIT %s, %s;' ); PREPARE stmt FROM @query; EXECUTE stmt; DEALLOCATE PREPARE stmt;"
        #     cursor.execute(query, (offset, int(limit) - 1, ))
        # # products = cursor.fetchall()
        # # print(products)
        
        # # user_log = select_user_log(cursor)
        # # query = "SELECT * FROM users;"
        # # cursor.execute(query)
        # # user_log = cursor.fetchall()
        
        return render_template("products.html")
    
    return render_template("products.html")


if __name__ == "__main__":
    app.run(debug=True)
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # print(select_user_log(cursor))