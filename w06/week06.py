from flask import Flask #載入Flask
from flask import request  #載入request物件
from flask import render_template #載入render_template
from flask import redirect
from flask import session
app=Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)
app.secret_key="any string but secret"

##前置作業與資料庫連線創建資料庫跟表

import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bb0970662139"
)
##如果還沒創建DATABASE就立刻創建
mycursor=mydb.cursor()
sql="CREATE DATABASE IF NOT EXISTS signin"
mycursor.execute(sql)
##立刻使用資料庫signin
sql="USE signin"
mycursor.execute(sql)
##如果還沒創建帳號TABLE就立刻創建
sql="CREATE TABLE IF NOT EXISTS accounts(name VARCHAR(20),account VARCHAR(20),password VARCHAR(20))"
mycursor.execute(sql)
##如果還沒創建留言TABLE就立刻創建
sql="CREATE TABLE IF NOT EXISTS messageTable(id INT PRIMARY KEY AUTO_INCREMENT,name VARCHAR(20),message VARCHAR(200))"
mycursor.execute(sql)



#1.導引至前端主頁面
#使用GET方法，處理路徑/的對應函式
@app.route("/")
def index():
    return render_template("indexW06.html")


#2.接收前端回傳的註冊資訊
#使用POST方法，處理路徑/signup 的對應函式
@app.route("/signup", methods=["POST"])
def signup():
    #接收 POST 方法的 Query String
    account=request.form["account"]
    password=request.form["password"]
    name=request.form["name"]
    print("註冊姓名",name)
    print("註冊帳號",account)
    print("註冊密碼",password)


    #3.連線資料庫判定是否註冊過
    mycursor=mydb.cursor()
    ##姓名重複或者帳號密碼同時重複都不要
    #傳統搜尋法--------------------------------------------------------------------------------------------------------------
    # sql="SELECT *FROM accounts WHERE (account='"+account+"' and password='"+password+"') or name='"+name+"'"
    # mycursor.execute(sql)
    #佔位符號填入搜尋
    sql="SELECT *FROM accounts WHERE (account=%s and password=%s) or name=%s"
    adr=(account,password,name)
    mycursor.execute(sql,adr)
    myresult=mycursor.fetchall()
    print("搜尋的結果",myresult)

    #3.1帳號密碼在資料庫中找不到，註冊成功，導向登入頁面member
    if myresult == [] and (name!="" and account!="" and password!=""):
        print("未註冊過，完成註冊導回主頁面")#導回註冊頁面重新註冊
        ##3.11註冊-將資料填入資料庫
        sql="INSERT INTO accounts(name,account,password) VALUES(%s,%s,%s)"
        val=(name,account,password)
        mycursor.execute(sql,val)
        mydb.commit()
        print(mycursor.rowcount,"record inserted.")##光標動作執行了幾個row
        return redirect("http://127.0.0.1:3000/")

    elif myresult == [] and (name=="" or account=="" or password==""):
        print("註冊資料不全，導向錯誤頁面")#導回註冊頁面重新註冊
        return redirect("http://127.0.0.1:3000/error?message=資料不全請重新填寫")
    
    #3.2否則為已註冊過導向錯誤頁面
    else:
        print("已註冊過，導向錯誤頁面")
        return redirect("http://127.0.0.1:3000/error?message=暱稱重複或同組帳號"+'、'+"密碼已經被註冊")
        

#利用要求字串(Query String)提供彈性:/error?message=自訂文字  
@app.route("/error", methods=["GET"])
def error():
    customize=request.args.get("message","帳號、或密碼錯誤")
    # print(str(customize))
    # return "error"
    return render_template("errorW06.html",content=str(customize))



#4.接收前端回傳的註冊資訊處理登入功能
#使用POST方法，處理路徑/signin 的對應函式
@app.route("/signin", methods=["POST"])
def signin():
    #接收 POST 方法的 Query String
    account=request.form["account"]
    password=request.form["password"]
    print("登入者帳號",account)
    print("登入者密碼",password)

    
    #5.連線資料庫判定能否登入
    ##搜尋資料表
    mycursor=mydb.cursor()
    #傳統搜尋法--------------------------------------------------------------------------------------------------------------
    # sql="SELECT *FROM accounts WHERE account='"+account+"' and password='"+password+"'"
    # mycursor.execute(sql)
    #佔位符號填入搜尋
    sql="SELECT *FROM accounts WHERE account=%s and password=%s"
    adr=(account,password)
    mycursor.execute(sql,adr)

    myresult=mycursor.fetchall()
    print("以帳號密碼搜尋的結果",myresult)
    #5.1帳號密碼在資料表中找不到，導向錯誤頁面
    if myresult == [] or (account=="" and password==""):
        print("帳號密碼錯誤，導入錯誤頁面")
        return redirect("http://127.0.0.1:3000/error")

    #5.2否則帳號密碼正確，導向登入頁面member
    else:
        print("帳號密碼正確")
        ##5.3篩出姓名--------------------------------------------------------------------------------------------------
        # #一般搜尋
        # sql="SELECT name FROM accounts WHERE account='"+account+"' and password='"+password+"'"
        # mycursor.execute(sql)
        #佔位符號填入搜尋
        sql="SELECT name FROM accounts WHERE account=%s and password=%s"
        adr=(account,password)
        mycursor.execute(sql,adr)
        myresult=mycursor.fetchall()
        print(myresult)
        nameNow=str(myresult[0]).replace("(","").replace(")","").replace("'","").replace(",","")
        ##5.4紀錄帳號密碼
        session["keyFlag"]="open"
        session["name"]=nameNow
        print("當前登入者是: ",session["name"])
        return redirect("/member")


###登入頁面後端
@app.route("/member")
def member():
    if session["keyFlag"]=="open":
        nameNow=session["name"]
        

# ##-----大改1-1 目標登入成功後的頁面要秀出歷史訊息
        #首先創建一個用來記錄的session
        session["record"]={
            "peopleNow":nameNow,
            "history":""
        }

        # ##連結資料庫把歷史資料抓出來
        mycursor=mydb.cursor()
        #取出所有留言的list
        mycursor.execute("SELECT * FROM messageTable")
        myresult=mycursor.fetchall()
        print("登入時的messageTable: ",myresult)
        ##存入session["record"]的history
        # print(type(session["record"]["history"]))
        session["record"]["history"]=myresult
        # #如果有資料
        if session["record"]["history"] !=[]:
            print("當前字典紀錄內容",session["record"]["history"][0][2])

        ##----大改1-2 改回傳字典形式資料到前端
        return render_template("memberw06.html",record_name=session["record"]["peopleNow"],record_message=session["record"]["history"])
   
    #沒登錄過就回首頁
    else:
        return redirect("/")


@app.route("/signout")
def signout():
    session["keyFlag"]=""
    session["name"]=""
    return redirect("/")


@app.route("/message", methods=["POST"])
def message():
    name=session["name"]
    messagecontent=request.form["message"]

    # 如果留言不為空才寫入
    mycursor=mydb.cursor()
    if messagecontent !="":
        ##將這則留言填入資料庫
        sql="INSERT INTO messageTable(name,message) VALUES(%s,%s)"
        val=(name,messagecontent)
        mycursor.execute(sql,val)
        mydb.commit()
        print(mycursor.rowcount,"record inserted.")##光標動作執行了幾個row
        print("寫入內容: 編號*",name,messagecontent)

    ##取出所有留言的list
    mycursor.execute("SELECT * FROM messageTable")
    myresult=mycursor.fetchall()
    print(myresult)
    session["record"]["history"]=myresult
    print(session["record"]["history"])
    # print(1234)
    if session["record"]["history"] !=[]:
        print("當前字典紀錄內容",session["record"]["history"][0][2])
    return render_template("memberw06.html",record_name=session["record"]["peopleNow"],record_message=session["record"]["history"])


#啟動網站伺服器，可透過port參數指定埠號
# if __name__=="__main__":
#     app.run(port=3000,debug=True)
app.run(port=3000)
