from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Sample hospital patient data
PATIENTS = [
    {"id": "P001", "name": "Ramesh Kumar",    "age": 45, "gender": "Male",   "ward": "Cardiology",   "doctor": "Dr. Suresh",   "status": "Admitted",   "days": 3,  "fee": 12000},
    {"id": "P002", "name": "Geetha Lakshmi",  "age": 32, "gender": "Female", "ward": "Maternity",    "doctor": "Dr. Priya",    "status": "Admitted",   "days": 2,  "fee": 8500},
    {"id": "P003", "name": "Arjun Sharma",    "age": 60, "gender": "Male",   "ward": "Orthopedics",  "doctor": "Dr. Raj",      "status": "Discharged", "days": 7,  "fee": 32000},
    {"id": "P004", "name": "Meena Devi",      "age": 28, "gender": "Female", "ward": "General",      "doctor": "Dr. Kavitha",  "status": "Admitted",   "days": 1,  "fee": 4200},
    {"id": "P005", "name": "Suresh Babu",     "age": 55, "gender": "Male",   "ward": "Neurology",    "doctor": "Dr. Anand",    "status": "Critical",   "days": 5,  "fee": 48000},
    {"id": "P006", "name": "Lakshmi Priya",   "age": 40, "gender": "Female", "ward": "Oncology",     "doctor": "Dr. Nithya",   "status": "Admitted",   "days": 10, "fee": 75000},
    {"id": "P007", "name": "Karthik Rajan",   "age": 22, "gender": "Male",   "ward": "General",      "doctor": "Dr. Kavitha",  "status": "Discharged", "days": 2,  "fee": 5500},
    {"id": "P008", "name": "Vijaya Bharathi", "age": 67, "gender": "Female", "ward": "Cardiology",   "doctor": "Dr. Suresh",   "status": "Critical",   "days": 8,  "fee": 62000},
    {"id": "P009", "name": "Dinesh Patel",    "age": 35, "gender": "Male",   "ward": "Dermatology",  "doctor": "Dr. Mala",     "status": "Admitted",   "days": 1,  "fee": 3800},
    {"id": "P010", "name": "Anitha Raj",      "age": 50, "gender": "Female", "ward": "Orthopedics",  "doctor": "Dr. Raj",      "status": "Discharged", "days": 4,  "fee": 18000},
]

DOCTORS = [
    {"name": "Dr. Suresh",  "specialty": "Cardiology",  "patients": 2, "available": True},
    {"name": "Dr. Priya",   "specialty": "Maternity",   "patients": 1, "available": True},
    {"name": "Dr. Raj",     "specialty": "Orthopedics", "patients": 2, "available": False},
    {"name": "Dr. Kavitha", "specialty": "General",     "patients": 2, "available": True},
    {"name": "Dr. Anand",   "specialty": "Neurology",   "patients": 1, "available": True},
    {"name": "Dr. Nithya",  "specialty": "Oncology",    "patients": 1, "available": False},
    {"name": "Dr. Mala",    "specialty": "Dermatology", "patients": 1, "available": True},
]

@app.route("/")
def index():
    admitted   = [p for p in PATIENTS if p["status"] == "Admitted"]
    critical   = [p for p in PATIENTS if p["status"] == "Critical"]
    discharged = [p for p in PATIENTS if p["status"] == "Discharged"]
    total_revenue = sum(p["fee"] for p in PATIENTS)
    return render_template("index.html",
        patients=PATIENTS, admitted=admitted,
        critical=critical, discharged=discharged,
        total_revenue=total_revenue, doctors=DOCTORS)

@app.route("/patient/<pid>")
def patient_detail(pid):
    patient = next((p for p in PATIENTS if p["id"] == pid), None)
    if not patient:
        return "Patient not found", 404
    return render_template("detail.html", patient=patient)

@app.route("/doctors")
def doctors():
    return render_template("doctors.html", doctors=DOCTORS)

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    patients = [p for p in PATIENTS if query in p["name"].lower()
                or query in p["id"].lower()
                or query in p["ward"].lower()
                or query in p["doctor"].lower()]
    admitted   = [p for p in patients if p["status"] == "Admitted"]
    critical   = [p for p in patients if p["status"] == "Critical"]
    discharged = [p for p in patients if p["status"] == "Discharged"]
    total_revenue = sum(p["fee"] for p in patients)
    return render_template("index.html",
        patients=patients, admitted=admitted,
        critical=critical, discharged=discharged,
        total_revenue=total_revenue, doctors=DOCTORS, query=query)

@app.route("/health")
def health():
    return {"status": "ok", "service": "hospital-management-portal"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
