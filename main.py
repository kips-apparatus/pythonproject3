from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__, static_folder="html", static_url_path="")
CORS(app)

# =========================================================
# Data Storage (JSON files)
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "reminders": os.path.join(DATA_DIR, "reminders.json"),
    "medicines": os.path.join(DATA_DIR, "medicines.json"),
    "prescriptions": os.path.join(DATA_DIR, "prescriptions.json"),
}


def read_data(key):
    try:
        path = FILES[key]
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def write_data(key, data):
    with open(FILES[key], "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =========================================================
# Serve HTML Pages
# =========================================================

@app.route("/")
def home():
    return send_from_directory("html", "homepage123.html")


@app.route("/reminders")
def reminders_page():
    return send_from_directory("html", "dose.html")


@app.route("/medicines")
def medicines_page():
    return send_from_directory("html", "medicine.html")


@app.route("/scanner")
def scanner_page():
    return send_from_directory("html", "scanner.html")


@app.route("/login")
def login_page():
    return send_from_directory("html", "loginpage.html")


# =========================================================
# API: Reminders
# =========================================================

@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    return jsonify(read_data("reminders"))


@app.route("/api/reminders", methods=["POST"])
def add_reminder():
    data = request.get_json(silent=True) or {}
    item = {
        "id": str(uuid.uuid4()),
        "medicineName": data.get("medicineName", "").strip(),
        "dosage": data.get("dosage", "").strip(),
        "time": data.get("time", ""),
        "date": data.get("date", ""),
        "frequency": data.get("frequency", "Once"),
        "notes": data.get("notes", "").strip(),
        "taken": False,
        "createdAt": datetime.now().isoformat(),
    }
    if not item["medicineName"]:
        return jsonify({"error": "Medicine name is required"}), 400

    reminders = read_data("reminders")
    reminders.append(item)
    write_data("reminders", reminders)
    return jsonify(item), 201


@app.route("/api/reminders/<id>", methods=["PATCH"])
def update_reminder(id):
    reminders = read_data("reminders")
    data = request.get_json(silent=True) or {}
    for i, reminder in enumerate(reminders):
        if reminder.get("id") == id:
            reminders[i].update(data)
            write_data("reminders", reminders)
            return jsonify(reminders[i])
    return jsonify({"error": "Reminder not found"}), 404


@app.route("/api/reminders/<id>", methods=["DELETE"])
def delete_reminder(id):
    reminders = read_data("reminders")
    new_list = [r for r in reminders if r.get("id") != id]
    if len(new_list) == len(reminders):
        return jsonify({"error": "Reminder not found"}), 404
    write_data("reminders", new_list)
    return jsonify({"message": "Reminder deleted successfully"})


# =========================================================
# API: Medicines
# =========================================================

@app.route("/api/medicines", methods=["GET"])
def get_medicines():
    return jsonify(read_data("medicines"))


@app.route("/api/medicines", methods=["POST"])
def add_medicine():
    data = request.get_json(silent=True) or {}
    item = {
        "id": str(uuid.uuid4()),
        "name": data.get("name", "").strip(),
        "quantity": data.get("quantity", ""),
        "expiryDate": data.get("expiryDate", ""),
        "notes": data.get("notes", "").strip(),
        "createdAt": datetime.now().isoformat(),
    }
    if not item["name"]:
        return jsonify({"error": "Medicine name is required"}), 400

    medicines = read_data("medicines")
    medicines.append(item)
    write_data("medicines", medicines)
    return jsonify(item), 201


@app.route("/api/medicines/<id>", methods=["PATCH"])
def update_medicine(id):
    medicines = read_data("medicines")
    data = request.get_json(silent=True) or {}
    for i, medicine in enumerate(medicines):
        if medicine.get("id") == id:
            medicines[i].update(data)
            write_data("medicines", medicines)
            return jsonify(medicines[i])
    return jsonify({"error": "Medicine not found"}), 404


@app.route("/api/medicines/<id>", methods=["DELETE"])
def delete_medicine(id):
    medicines = read_data("medicines")
    new_list = [m for m in medicines if m.get("id") != id]
    if len(new_list) == len(medicines):
        return jsonify({"error": "Medicine not found"}), 404
    write_data("medicines", new_list)
    return jsonify({"message": "Medicine deleted successfully"})


# =========================================================
# API: Prescriptions
# =========================================================

@app.route("/api/prescriptions", methods=["GET"])
def get_prescriptions():
    return jsonify(read_data("prescriptions"))


@app.route("/api/prescriptions", methods=["POST"])
def add_prescription():
    data = request.get_json(silent=True) or {}
    item = {
        "id": str(uuid.uuid4()),
        "doctorName": data.get("doctorName", "").strip(),
        "dateIssued": data.get("dateIssued", ""),
        "disease": data.get("disease", "").strip(),
        "notes": data.get("notes", "").strip(),
        "image": data.get("image", ""),
        "createdAt": datetime.now().isoformat(),
    }
    if not item["doctorName"] or not item["disease"]:
        return jsonify({"error": "Doctor name and disease are required"}), 400

    prescriptions = read_data("prescriptions")
    prescriptions.append(item)
    write_data("prescriptions", prescriptions)
    return jsonify(item), 201


@app.route("/api/prescriptions/<id>", methods=["PATCH"])
def update_prescription(id):
    prescriptions = read_data("prescriptions")
    data = request.get_json(silent=True) or {}
    for i, prescription in enumerate(prescriptions):
        if prescription.get("id") == id:
            prescriptions[i].update(data)
            write_data("prescriptions", prescriptions)
            return jsonify(prescriptions[i])
    return jsonify({"error": "Prescription not found"}), 404


@app.route("/api/prescriptions/<id>", methods=["DELETE"])
def delete_prescription(id):
    prescriptions = read_data("prescriptions")
    new_list = [p for p in prescriptions if p.get("id") != id]
    if len(new_list) == len(prescriptions):
        return jsonify({"error": "Prescription not found"}), 404
    write_data("prescriptions", new_list)
    return jsonify({"message": "Prescription deleted successfully"})


# =========================================================
# Run Server
# =========================================================

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  DoseWise is running!")
    print("  Open → http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
