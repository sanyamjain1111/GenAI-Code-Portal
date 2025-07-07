from flask import Flask, render_template, request, session, redirect, url_for,send_file
from config.config import Config
from models.database import db, Query
from oauth.google_auth import auth_bp, init_oauth
from ai.ai_helper import get_ai_solution
from sqlalchemy import text
from fpdf import FPDF
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(auth_bp)
init_oauth(app)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("dashboard.html")

    prompt1 = request.form.get("user-input", "").strip()
    if not prompt1:
        return "Invalid input"
    result=db.session.execute(text("select * from query"))
    column_names=result.keys()
    querries = [dict(zip(column_names, row)) for row in result.fetchall()]
    for query1 in querries:
        if prompt1 in query1["prompt"]:
            response= query1["response"]
            return response

    responseforcode = get_ai_solution(prompt1 + " Is this a code or sentence? Reply Yes for code and No for sentence.").strip().lower()
    responseforproblem = get_ai_solution(prompt1 + " Is this a code problem? Just reply Yes or No").strip().lower()

    print(responseforcode, responseforproblem)

    if responseforcode == "yes":
        response = get_ai_solution(prompt1 + " Check if the code is working and provide an optimized, correct solution if no code provided directly give solution in python.")
    elif responseforproblem == "yes":
        response = get_ai_solution(prompt1 + " Provide the solution in Python if language not mentioned.")
    else:
        response = "Not a code problem. " + get_ai_solution(prompt1)

    query = Query(user_id=session["user"]["email"], prompt=prompt1, response=response)
    db.session.add(query)
    db.session.commit()

    return response  
@app.route("/pastcodes", methods=["GET","POST"])
def pastcodes():
     if "user" not in session:
        return redirect(url_for("auth.login"))
     result=db.session.execute(text("select * from query"))
     column_names=result.keys()
     querries = [dict(zip(column_names, row)) for row in result.fetchall()]
     return render_template("pastcodes.html",codes=querries)
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))  
    user_info = session["user"] 
    return render_template("profile.html", user=user_info)
@app.route("/download-pdf")
def download_pdf():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    user_email = session["user"]["email"]
    queries = Query.query.filter_by(user_id=user_email).all()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Stored Code Queries", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for query in queries:
        pdf.multi_cell(0, 10, f"Query:\n{query.prompt}", border=1)
        pdf.ln(2)
        pdf.multi_cell(0, 10, f"Response:\n{query.response}", border=1)
        pdf.ln(5)

    pdf_path = os.path.join("static", "stored_codes.pdf")
    pdf.output(pdf_path)

    return send_file(pdf_path, as_attachment=True)
@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect(f"/")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
