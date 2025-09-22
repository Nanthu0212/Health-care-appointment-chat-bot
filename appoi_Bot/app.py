from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

appointments = []
doctors = {
    "Dr. John": ["10:00 AM", "11:00 AM", "2:00 PM"],
    "Dr. Smith": ["9:00 AM", "1:00 PM", "3:00 PM"]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower()

    if "hi" in user_input or "hello" in user_input:
        return jsonify({"reply": "Hello! How can I help you with your appointment today?"})

    elif "doctor" in user_input or "available" in user_input:
        response = "We have the following doctors available:\n"
        for doc, slots in doctors.items():
            response += f"{doc}: {', '.join(slots)}\n"
        response += "Please mention the doctor and time to book an appointment."
        return jsonify({"reply": response})

    elif "book" in user_input:
        for doc in doctors:
            if doc.lower() in user_input:
                for slot in doctors[doc]:
                    if slot.lower() in user_input:
                        appointments.append({"doctor": doc, "time": slot})
                        doctors[doc].remove(slot)
                        return jsonify({"reply": f"Your appointment with {doc} at {slot} is confirmed!"})
        return jsonify({"reply": "Please provide a valid doctor name and time slot."})

    elif "appointments" in user_input:
        if not appointments:
            return jsonify({"reply": "No appointments booked yet."})
        reply = "Here are your booked appointments:\n"
        for a in appointments:
            reply += f"{a['doctor']} at {a['time']}\n"
        return jsonify({"reply": reply})

    else:
        return jsonify({"reply": "Sorry, I didn't understand that. You can say things like 'Show available doctors' or 'Book an appointment with Dr. John at 10:00 AM'."})

if __name__ == "__main__":
    app.run(debug=True)
