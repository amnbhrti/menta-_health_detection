from fpdf import FPDF

# Function to generate a report
def generate_report(user_info, detected_symptom):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Cognitive Disorder Detection Report", ln=True, align='C')

    # User Information
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {user_info['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {user_info['gender']}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {user_info['age']}", ln=True)

    # Detected Symptom
    pdf.cell(200, 10, txt=f"Detected Symptom: {detected_symptom}", ln=True)

    # Save the PDF
    file_name = f"report_{user_info['name']}.pdf"
    pdf.output(file_name)

    return file_name
