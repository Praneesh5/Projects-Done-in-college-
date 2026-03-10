from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = "medpulse_secure_key_2026"


# ---------------- DATABASE CONNECTION ----------------
def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medpulse_pro"
    )


# ---------------- DOCTOR LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hashlib.sha256(
            request.form["password"].encode()
        ).hexdigest()

        con = db()
        cur = con.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM doctor WHERE username=%s AND password_hash=%s",
            (username, password)
        )
        doctor = cur.fetchone()
        con.close()

        if doctor:
            session["doctor_id"] = doctor["id"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "doctor_id" not in session:
        return redirect("/")
    return render_template("dashboard.html")


# ---------------- PATIENT LIST ----------------
@app.route("/patients")
def patients():
    if "doctor_id" not in session:
        return redirect("/")

    con = db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
    data = cur.fetchall()
    con.close()

    return render_template("patients.html", patients=data)


# ---------------- ADD PATIENT ----------------
@app.route("/patients/add", methods=["GET", "POST"])
def add_patient():
    if "doctor_id" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        location = request.form["location"]

        token = secrets.token_hex(16)

        con = db()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO patients (name, age, location, api_token)
            VALUES (%s, %s, %s, %s)
        """, (name, age, location, token))

        con.commit()
        con.close()

        return redirect("/patients")

    return render_template("add_patient.html")


# ---------------- PATIENT PROFILE ----------------
@app.route("/patient/<int:pid>")
def patient_profile(pid):
    if "doctor_id" not in session:
        return redirect("/")

    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
    patient = cur.fetchone()

    con.close()

    return render_template("patient_profile.html", patient=patient)


# ---------------- UPDATE NOTES ----------------
@app.route("/patient/<int:pid>/update", methods=["POST"])
def update_notes(pid):
    if "doctor_id" not in session:
        return redirect("/")

    notes = request.form["notes"]

    con = db()
    cur = con.cursor()
    cur.execute(
        "UPDATE patients SET medical_notes=%s WHERE id=%s",
        (notes, pid)
    )

    con.commit()
    con.close()

    return redirect(f"/patient/{pid}")


# ---------------- LIVE GRAPH DATA (Patients Page) ----------------
@app.route("/api/v1/live/<int:pid>")
def live_data(pid):
    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT bpm, ecg_value, status, recorded_at
        FROM heart_data
        WHERE patient_id=%s
        ORDER BY recorded_at DESC
        LIMIT 30
    """, (pid,))

    data = cur.fetchall()
    con.close()

    return jsonify(data)


# ---------------- DASHBOARD LATEST DATA ----------------
@app.route("/api/latest-data")
def latest_data():

    if "doctor_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    con = db()
    cur = con.cursor(dictionary=True)

    # 1️⃣ Get latest patient
    cur.execute("""
        SELECT id
        FROM patients
        ORDER BY created_at DESC
        LIMIT 1
    """)
    patient = cur.fetchone()

    if not patient:
        con.close()
        return jsonify({"bpm": 0, "ecg": 0})

    # 2️⃣ Get latest heart data of that patient
    cur.execute("""
        SELECT bpm, ecg_value
        FROM heart_data
        WHERE patient_id=%s
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (patient["id"],))

    result = cur.fetchone()
    con.close()

    if result:
        return jsonify({
            "bpm": int(result["bpm"]),
            "ecg": int(result["ecg_value"]) if result["ecg_value"] else 0
        })
    else:
        return jsonify({
            "bpm": 0,
            "ecg": 0
        })


# ---------------- ESP RECEIVE DATA ----------------
@app.route("/api/v1/bpm", methods=["POST"])
def receive_bpm():

    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()

    token = data.get("token")
    bpm = data.get("bpm")
    ecg = data.get("ecg")

    if not token or bpm is None:
        return jsonify({"error": "Invalid Data"}), 400

    try:
        bpm = int(bpm)
        ecg = int(ecg) if ecg is not None else 0
    except:
        return jsonify({"error": "Invalid Number Format"}), 400

    con = db()
    cur = con.cursor(dictionary=True)

    # Find patient using token
    cur.execute("SELECT id FROM patients WHERE api_token=%s", (token,))
    patient = cur.fetchone()

    if not patient:
        con.close()
        return jsonify({"error": "Unauthorized"}), 401

    status = "CRITICAL" if bpm < 60 or bpm > 120 else "NORMAL"

    cur = con.cursor()
    cur.execute("""
        INSERT INTO heart_data (patient_id, bpm, ecg_value, status)
        VALUES (%s, %s, %s, %s)
    """, (patient["id"], bpm, ecg, status))

    con.commit()
    con.close()

    return jsonify({"message": "Data Stored Successfully"}), 200


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)