from flask import Flask,render_template,request,redirect,session
import mysql.connector,hashlib

app = Flask(__name__, static_folder="static")
app.secret_key="railway123"

# ---------- DATABASE CONNECTION ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ticket_system"
    )

# ---------- LOGIN ----------
@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        h=hashlib.sha256(p.encode()).hexdigest()

        db=get_db()
        cur=db.cursor(dictionary=True)
        cur.execute("SELECT * FROM credentials WHERE username=%s AND password_hash=%s",(u,h))
        user=cur.fetchone()

        if user:
            session["uid"]=user["id"]
            session["admin"]=user["is_admin"]

            if user["is_admin"]:
                return redirect("/admin")
            else:
                return redirect("/search")

    return render_template("login.html")

# ---------- ADMIN ----------
@app.route("/admin",methods=["GET","POST"])
def admin():
    db=get_db()
    cur=db.cursor(dictionary=True)

    if request.method=="POST":
        cur.execute("""
        REPLACE INTO trains
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """,(
            request.form["train_no"],
            request.form["train_name"],
            request.form["from_loc"],
            request.form["to_loc"],
            request.form["seats"],
            request.form["cost"],
            request.form["start"],
            request.form["end"]
        ))
        db.commit()

    cur.execute("SELECT * FROM trains")
    trains=cur.fetchall()
    return render_template("admin.html",trains=trains)

# ---------- SEARCH ----------
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="POST":
        f=request.form["from_loc"]
        t=request.form["to_loc"]
        d=request.form["date"]
        return redirect(f"/results?from={f}&to={t}&date={d}")
    return render_template("search.html")

# ---------- RESULTS ----------
@app.route("/results")
def results():
    f=request.args.get("from")
    t=request.args.get("to")
    d=request.args.get("date")

    db=get_db()
    cur=db.cursor(dictionary=True)
    cur.execute("""
        SELECT * FROM trains
        WHERE from_loc=%s AND to_loc=%s AND seats>0
    """,(f,t))
    trains=cur.fetchall()

    return render_template("results.html",trains=trains,date=d)

# ---------- BOOK TICKET ----------
@app.route("/book/<int:train_no>",methods=["GET","POST"])
def book(train_no):
    db=get_db()
    cur=db.cursor(dictionary=True)

    if request.method=="POST":
        count=int(request.form["count"])
        date=request.form["date"]

        cur.execute("SELECT * FROM trains WHERE train_no=%s",(train_no,))
        train=cur.fetchone()

        for i in range(count):
            name=request.form[f"name{i}"]

            cur.execute("""
            INSERT INTO tickets(user_id,train_no,passenger_name,from_loc,to_loc,travel_date)
            VALUES(%s,%s,%s,%s,%s,%s)
            """,(session["uid"],train_no,name,train["from_loc"],train["to_loc"],date))

        cur.execute("UPDATE trains SET seats=seats-%s WHERE train_no=%s",(count,train_no))
        db.commit()

        return redirect("/pay")

    return render_template("book.html",train_no=train_no)

# ---------- PAYMENT ----------
@app.route("/pay",methods=["GET","POST"])
def pay():
    db=get_db()
    cur=db.cursor(dictionary=True)

    cur.execute("SELECT MAX(ticket_id) AS tid FROM tickets WHERE user_id=%s",(session["uid"],))
    tid=cur.fetchone()["tid"]

    if request.method=="POST":
        method=request.form["method"]

        cur.execute("""
        INSERT INTO payments(ticket_id,amount,method,status)
        VALUES(%s,500,%s,'SUCCESS')
        """,(tid,method))
        db.commit()

        return redirect("/profile")

    return render_template("pay.html")

# ---------- PROFILE ----------
@app.route("/profile")
def profile():
    db=get_db()
    cur=db.cursor(dictionary=True)

    cur.execute("SELECT * FROM tickets WHERE user_id=%s",(session["uid"],))
    tickets=cur.fetchall()

    cur.execute("""
    SELECT payments.* FROM payments
    JOIN tickets ON payments.ticket_id=tickets.ticket_id
    WHERE tickets.user_id=%s
    """,(session["uid"],))
    payments=cur.fetchall()

    return render_template("profile.html",tickets=tickets,payments=payments)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- RUN ----------
if __name__=="__main__":
    app.run(debug=True)
