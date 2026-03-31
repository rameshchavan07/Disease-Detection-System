"""
Prescription PDF Generator for MedDetect AI
Generates professional PDF prescriptions using fpdf2 with hospital details,
doctor info, patient info, medicines table, and safety information.
"""

from fpdf import FPDF
from datetime import datetime
import io


class PrescriptionPDF(FPDF):
    """Custom PDF class for prescription generation."""

    def __init__(self, hospital_name="", hospital_address="", doctor_name="",
                 doctor_specialty="", doctor_email=""):
        super().__init__()
        self.hospital_name = hospital_name
        self.hospital_address = hospital_address
        self.doctor_name = doctor_name
        self.doctor_specialty = doctor_specialty
        self.doctor_email = doctor_email

    def header(self):
        """Professional prescription header with hospital and doctor details."""
        # ── Top accent bar ──
        self.set_fill_color(0, 150, 100)  # Teal-green
        self.rect(0, 0, 210, 3, 'F')

        # ── Hospital Name ──
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(0, 120, 80)
        self.set_y(8)
        self.cell(0, 10, self.hospital_name or "Medical Center", ln=True, align="C")

        # ── Hospital Address ──
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, self.hospital_address or "", ln=True, align="C")
        self.ln(2)

        # ── Separator ──
        self.set_draw_color(0, 150, 100)
        self.set_line_width(0.5)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

        # ── Doctor info row ──
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(100, 6, f"Dr. {self.doctor_name}", ln=False)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        date_str = datetime.now().strftime("%B %d, %Y  |  %I:%M %p")
        self.cell(0, 6, f"Date: {date_str}", ln=True, align="R")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(80, 80, 80)
        self.cell(100, 5, f"{self.doctor_specialty}", ln=False)
        self.cell(0, 5, f"Email: {self.doctor_email}", ln=True, align="R")

        # ── Rx symbol line ──
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(0, 150, 100)
        self.cell(20, 15, "Rx", ln=False)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 15, "PRESCRIPTION", ln=True)
        self.ln(2)

    def footer(self):
        """Footer with disclaimer and page number."""
        self.set_y(-30)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

        self.set_font("Helvetica", "I", 7)
        self.set_text_color(130, 130, 130)
        self.multi_cell(0, 3,
            "DISCLAIMER: This prescription is generated via MedDetect AI platform. "
            "It is intended for the named patient only. Always follow your doctor's verbal instructions. "
            "Do not self-medicate. Contact your healthcare provider for any concerns."
        )
        self.ln(1)
        self.set_font("Helvetica", "", 7)
        self.cell(0, 3, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  MedDetect AI Platform", ln=False)
        self.cell(0, 3, f"Page {self.page_no()}/{{nb}}", align="R")


def generate_prescription_pdf(
    hospital_name: str,
    hospital_address: str,
    doctor_name: str,
    doctor_specialty: str,
    doctor_email: str,
    patient_email: str,
    appointment_date: str,
    diagnosis: str,
    medicines: list,
    medicine_details: list,
    notes: str = ""
) -> bytes:
    """
    Generate a professional prescription PDF.

    Args:
        hospital_name: Name of the hospital/clinic
        hospital_address: Full address of the hospital
        doctor_name: Doctor's full name
        doctor_specialty: Doctor's specialty
        doctor_email: Doctor's email
        patient_email: Patient's email
        appointment_date: Date of appointment
        diagnosis: Diagnosis / disease name
        medicines: List of dicts, each with keys: name, dosage, frequency, duration
        medicine_details: List of dicts from medicine_db with full drug info
        notes: Additional notes from the doctor

    Returns:
        PDF content as bytes
    """
    pdf = PrescriptionPDF(
        hospital_name=hospital_name,
        hospital_address=hospital_address,
        doctor_name=doctor_name,
        doctor_specialty=doctor_specialty,
        doctor_email=doctor_email
    )
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=35)

    # ═══════════════════════════════════════════
    # Patient Information Block
    # ═══════════════════════════════════════════
    pdf.set_fill_color(245, 248, 250)
    pdf.rect(15, pdf.get_y(), 180, 18, 'F')

    y_start = pdf.get_y() + 3
    pdf.set_xy(20, y_start)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(30, 5, "PATIENT:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(60, 5, patient_email, ln=False)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(30, 5, "DATE:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 5, appointment_date, ln=True)

    pdf.set_xy(20, y_start + 7)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(30, 5, "DIAGNOSIS:", ln=False)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 120, 80)
    pdf.cell(0, 5, diagnosis, ln=True)

    pdf.set_y(pdf.get_y() + 8)

    # ═══════════════════════════════════════════
    # Medicines Table
    # ═══════════════════════════════════════════
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, "PRESCRIBED MEDICATIONS", ln=True)
    pdf.ln(2)

    # Table header
    pdf.set_fill_color(0, 150, 100)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    col_widths = [8, 50, 40, 40, 42]
    headers = ["#", "Medicine", "Dosage", "Frequency", "Duration"]
    for i, (header, w) in enumerate(zip(headers, col_widths)):
        pdf.cell(w, 7, header, border=1, fill=True, align="C")
    pdf.ln()

    # Table rows
    pdf.set_text_color(30, 30, 30)
    for idx, med in enumerate(medicines, 1):
        pdf.set_fill_color(255, 255, 255) if idx % 2 == 1 else pdf.set_fill_color(245, 248, 250)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(col_widths[0], 7, str(idx), border=1, fill=True, align="C")
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(col_widths[1], 7, med.get("name", ""), border=1, fill=True)
        pdf.cell(col_widths[2], 7, med.get("dosage", ""), border=1, fill=True, align="C")
        pdf.cell(col_widths[3], 7, med.get("frequency", ""), border=1, fill=True, align="C")
        pdf.cell(col_widths[4], 7, med.get("duration", ""), border=1, fill=True, align="C")
        pdf.ln()

    pdf.ln(5)

    # ═══════════════════════════════════════════
    # Drug Safety Information
    # ═══════════════════════════════════════════
    if medicine_details:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, "MEDICATION INFORMATION & SAFETY", ln=True)
        pdf.ln(2)

        for detail in medicine_details:
            if not detail:
                continue

            # Medicine name box
            pdf.set_fill_color(240, 248, 245)
            pdf.set_draw_color(0, 150, 100)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(0, 120, 80)
            pdf.cell(180, 6, f"  {detail['name']}  ({detail['generic_name']})", border=1, fill=True, ln=True)

            pdf.set_text_color(60, 60, 60)
            pdf.set_font("Helvetica", "", 7.5)

            # Category & Form
            pdf.cell(90, 5, f"Category: {detail['category']}", ln=False)
            pdf.cell(90, 5, f"Form: {detail['form']}", ln=True)

            # Dosage & Max
            pdf.cell(90, 5, f"Common Dosage: {detail['common_dosage']}", ln=False)
            pdf.cell(90, 5, f"Max Daily: {detail['max_daily']}", ln=True)

            # Side Effects
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(180, 80, 0)
            side_str = ", ".join(detail.get("side_effects", []))
            pdf.cell(180, 5, f"Side Effects: {side_str}", ln=True)

            # Contraindications
            pdf.set_text_color(200, 50, 50)
            contra_str = ", ".join(detail.get("contraindications", []))
            pdf.cell(180, 5, f"Contraindications: {contra_str}", ln=True)

            # Drug Interactions
            pdf.set_text_color(100, 80, 160)
            inter_str = ", ".join(detail.get("interactions", []))
            pdf.cell(180, 5, f"Interactions: {inter_str}", ln=True)

            pdf.set_draw_color(220, 220, 220)
            pdf.ln(3)

    # ═══════════════════════════════════════════
    # Doctor's Notes
    # ═══════════════════════════════════════════
    if notes:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, "DOCTOR'S NOTES & ADVICE", ln=True)
        pdf.ln(1)

        pdf.set_fill_color(255, 252, 240)
        pdf.set_draw_color(200, 180, 100)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.rect(15, y, 180, 4 + 5 * max(1, len(notes) // 80 + 1), 'DF')
        pdf.set_xy(18, y + 2)
        pdf.multi_cell(174, 5, notes)
        pdf.ln(5)

    # ═══════════════════════════════════════════
    # Signature Block
    # ═══════════════════════════════════════════
    pdf.ln(8)
    sig_y = pdf.get_y()
    pdf.set_draw_color(30, 30, 30)
    pdf.line(120, sig_y, 190, sig_y)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 30, 30)
    pdf.set_xy(120, sig_y + 2)
    pdf.cell(70, 5, f"Dr. {doctor_name}", ln=True, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(120)
    pdf.cell(70, 4, doctor_specialty, ln=True, align="C")
    pdf.set_x(120)
    pdf.cell(70, 4, "Digital Signature", ln=True, align="C")

    # ── Output ──
    return bytes(pdf.output())
