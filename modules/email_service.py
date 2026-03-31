import os
import smtplib
from email.message import EmailMessage
import logging
import streamlit as st

def send_report_email(to_email, pdf_bytes, disease_name):
    """
    Sends the generated PDF report to the provided email address.
    Expects SMTP_SERVER, SMTP_PORT, SMTP_USER, and SMTP_PASSWORD 
    to be set in the environment variables.
    """
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT", 587)
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")

    # If SMTP is not configured, we simulate it
    if not smtp_server or not smtp_user or not smtp_password:
        logging.info(f"SMTP credentials not found. Simulated sending report for {disease_name} to {to_email}.")
        print(f"[Simulated Email] Sent report for {disease_name} to {to_email}")
        return True, "Email simulation successful (SMTP not configured)."
        
    smtp_server_str = str(smtp_server)
    smtp_user_str = str(smtp_user)
    smtp_password_str = str(smtp_password)

    try:
        msg = EmailMessage()
        msg['Subject'] = f"Your MedDetect AI Health Report: {disease_name}"
        msg['From'] = smtp_user
        msg['To'] = to_email

        body = (
            f"Hello,\n\n"
            f"Please find attached your AI-generated health report for {disease_name}.\n\n"
            f"Disclaimer: This report is for informational purposes only and does not replace professional medical advice.\n\n"
            f"Best regards,\nMedDetect AI Team"
        )
        msg.set_content(body)

        msg.add_attachment(
            pdf_bytes, 
            maintype='application', 
            subtype='pdf', 
            filename=f"MedDetect_Report_{disease_name.replace(' ', '_')}.pdf"
        )

        with smtplib.SMTP(smtp_server_str, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user_str, smtp_password_str)
            server.send_message(msg)

        logging.info(f"Successfully sent report to {to_email}")
        return True, "Email sent successfully!"
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        logging.error(error_msg)
        return False, error_msg


def send_appointment_email(to_email, doctor_name, specialty, meeting_link, date_time):
    """
    Sends an appointment confirmation email containing the meeting link.
    """
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT", 587)
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")

    # If SMTP is not configured, we simulate it
    if not smtp_server or not smtp_user or not smtp_password:
        logging.info(f"SMTP credentials not found. Simulated appointment email to {to_email}.")
        print(f"[Simulated Email] Sent appointment confirmation with {doctor_name} to {to_email}")
        return True, "Email simulation successful (SMTP not configured)."
        
    smtp_server_str = str(smtp_server)
    smtp_user_str = str(smtp_user)
    smtp_password_str = str(smtp_password)

    try:
        msg = EmailMessage()
        msg['Subject'] = f"Appointment Confirmation: Dr. {doctor_name}"
        msg['From'] = smtp_user_str
        msg['To'] = to_email

        body = (
            f"Hello,\n\n"
            f"Your appointment with Dr. {doctor_name} ({specialty}) has been confirmed!\n\n"
            f"Date & Time: {date_time}\n\n"
            f"Please join your video consultation using the following secure link at the scheduled time:\n"
            f"{meeting_link}\n\n"
            f"Best regards,\nMedDetect AI Team"
        )
        msg.set_content(body)

        with smtplib.SMTP(smtp_server_str, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user_str, smtp_password_str)
            server.send_message(msg)

        logging.info(f"Successfully sent appointment email to {to_email}")
        return True, "Email sent successfully!"
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        logging.error(error_msg)
        return False, error_msg


def send_prescription_email(to_email, doctor_name, hospital_name, diagnosis, medicines, notes, pdf_bytes=None):
    """
    Sends a digital prescription to the patient, optionally attaching a PDF.
    """
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT", 587)
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")

    # If SMTP is not configured, we simulate it
    if not smtp_server or not smtp_user or not smtp_password:
        logging.info(f"SMTP credentials not found. Simulated prescription email to {to_email}.")
        print(f"[Simulated Email] Sent prescription from Dr. {doctor_name} to {to_email}")
        return True, "Email simulation successful (SMTP not configured)."
        
    smtp_server_str = str(smtp_server)
    smtp_user_str = str(smtp_user)
    smtp_password_str = str(smtp_password)

    try:
        msg = EmailMessage()
        msg['Subject'] = f"Your Digital Prescription: Dr. {doctor_name}"
        msg['From'] = smtp_user_str
        msg['To'] = to_email

        body = f"Hello,\n\nPlease find your digital prescription attached.\n\n"
        body += f"Provider: Dr. {doctor_name} ({hospital_name})\n"
        body += f"Diagnosis: {diagnosis}\n\nMedicines:\n"
        
        if isinstance(medicines, list):
            for m in medicines:
                if isinstance(m, dict):
                    body += f"- {m.get('name', '')} | {m.get('dosage', '')} | {m.get('frequency', '')} | {m.get('duration', '')}\n"
                else:
                    body += f"- {m}\n"
        
        body += f"\nAdditional Notes:\n{notes}\n\n"
        body += "Disclaimer: This is an automatically generated prescription summary from the MedDetect AI platform. Please refer to your doctor for further guidance.\n\nBest regards,\nMedDetect AI Team"

        msg.set_content(body)

        # Attach PDF if provided
        if pdf_bytes:
            msg.add_attachment(
                pdf_bytes,
                maintype='application',
                subtype='pdf',
                filename=f"Prescription_Dr_{doctor_name.replace(' ', '_')}_{diagnosis.replace(' ', '_')[:30]}.pdf"
            )

        with smtplib.SMTP(smtp_server_str, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user_str, smtp_password_str)
            server.send_message(msg)

        logging.info(f"Successfully sent prescription email to {to_email}")
        return True, "Email sent successfully!"
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        logging.error(error_msg)
        return False, error_msg
