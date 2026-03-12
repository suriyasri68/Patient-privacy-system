import gradio as gr

# ---------------------------
# Login Credentials
# ---------------------------
USERNAME = "admin"
PASSWORD = "12345"

# ---------------------------
# Patient Record Storage
# ---------------------------
patient_records = {}

# ---------------------------
# Functions
# ---------------------------

def login(username, password):
    if username == USERNAME and password == PASSWORD:
        return (
            "✅ Login Successful!",
            gr.update(visible=False),   # hide login
            gr.update(visible=True)     # show dashboard
        )
    else:
        return (
            "❌ Invalid Username or Password",
            gr.update(visible=True),
            gr.update(visible=False)
        )


def add_patient(pid, name, age, disease):
    if pid in patient_records:
        return "⚠️ Patient ID already exists."

    patient_records[pid] = {
        "Name": name,
        "Age": age,
        "Disease": disease
    }

    return "✅ Patient added successfully."


def view_patient(pid):
    if pid in patient_records:
        record = patient_records[pid]
        return f"Name: {record['Name']}, Age: {record['Age']}, Disease: {record['Disease']}"
    else:
        return "❌ Patient not found."


def view_all():
    if not patient_records:
        return "⚠️ No records available."

    result = ""
    for pid, data in patient_records.items():
        result += f"\nID: {pid}\nName: {data['Name']}\nAge: {data['Age']}\nDisease: {data['Disease']}\n"
        result += "------------------\n"
    return result


# ---------------------------
# Gradio Interface
# ---------------------------

with gr.Blocks() as demo:

    gr.Markdown("# 🏥 Patient Record Safety System")

    # LOGIN SECTION
    with gr.Column(visible=True) as login_section:
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_output = gr.Textbox(label="Status")

    # MAIN DASHBOARD (Hidden first)
    with gr.Column(visible=False) as dashboard:

        with gr.Tab("➕ Add Patient"):
            pid = gr.Textbox(label="Patient ID")
            name = gr.Textbox(label="Name")
            age = gr.Number(label="Age")
            disease = gr.Textbox(label="Disease")

            add_btn = gr.Button("Add Record")
            add_output = gr.Textbox()

            add_btn.click(add_patient, [pid, name, age, disease], add_output)

        with gr.Tab("🔍 View Patient"):
            search_id = gr.Textbox(label="Patient ID")
            view_btn = gr.Button("Search")
            view_output = gr.Textbox()

            view_btn.click(view_patient, search_id, view_output)

        with gr.Tab("📋 View All Patients"):
            all_btn = gr.Button("Show Records")
            all_output = gr.Textbox(lines=10)

            all_btn.click(view_all, outputs=all_output)

    # LOGIN ACTION
    login_btn.click(
        login,
        inputs=[username, password],
        outputs=[login_output, login_section, dashboard]
    )

demo.launch()
