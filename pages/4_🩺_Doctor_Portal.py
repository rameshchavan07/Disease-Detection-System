"""
🩺 Doctor Portal
Register as a doctor and manage your appointments from a dedicated dashboard.
"""
import streamlit as st
import sys, os
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.shared_ui import inject_premium_css, render_sidebar
from modules.database import (
    register_doctor, get_doctor_by_user_id,
    get_doctor_appointments, update_appointment_status,
    save_prescription, get_user_predictions
)
from modules.email_service import send_prescription_email
from modules.medicine_db import search_medicines, get_medicine_info, get_all_medicine_names
from modules.prescription_pdf import generate_prescription_pdf

st.set_page_config(page_title="Doctor Portal - MedDetect AI", page_icon="🩺", layout="wide")

# Auth Check
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("🔒 Please sign in from the **🔑 Sign In** page to access the Doctor Portal.")
    st.info("Sign in with your account, then register as a doctor here.")
    st.stop()

inject_premium_css()
render_sidebar()

# Page CSS
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b26 100%);
    border-right: 1px solid rgba(108,99,255,0.08);
}
.portal-header {
    display: flex; align-items: center; gap: 1rem;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, rgba(0,214,143,0.1), rgba(108,99,255,0.05));
    border: 1px solid rgba(0,214,143,0.15);
    border-radius: 20px; margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}
.portal-header h1 {
    margin: 0; font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, #00D68F, #00B377);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.portal-header p { margin: 0.3rem 0 0; font-size: 0.88rem; color: rgba(250,250,250,0.5); }

.appt-card {
    background: linear-gradient(145deg, rgba(26,29,41,0.9), rgba(26,29,41,0.5));
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.appt-card:hover {
    border-color: rgba(108,99,255,0.3);
    box-shadow: 0 8px 24px rgba(108,99,255,0.08);
}
.appt-card.today {
    border-color: rgba(0,214,143,0.4);
    background: linear-gradient(145deg, rgba(0,214,143,0.08), rgba(26,29,41,0.5));
}
.appt-label { font-size: 0.75rem; color: rgba(250,250,250,0.4); text-transform: uppercase; letter-spacing: 1px; }
.appt-value { font-size: 0.95rem; color: #FAFAFA; font-weight: 600; }
.stat-box {
    text-align: center; padding: 1.2rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(108,99,255,0.1);
    border-radius: 16px;
}
.stat-box .num {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-box .lbl { font-size: 0.75rem; color: rgba(250,250,250,0.4); text-transform: uppercase; letter-spacing: 1px; }

.med-info-card {
    background: linear-gradient(135deg, rgba(0,214,143,0.05), rgba(108,99,255,0.03));
    border: 1px solid rgba(0,214,143,0.15);
    border-radius: 12px; padding: 1rem; margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

user_id = st.session_state.user_id
user_email = st.session_state.get("user_email", "")

# Check if user is already a registered doctor
doctor = get_doctor_by_user_id(user_id)

# ════════════════════════════════════════
# MODE 1: Not a doctor → Show registration
# ════════════════════════════════════════
if not doctor:
    st.markdown("""
    <div class="portal-header">
        <span style="font-size: 2.5rem;">🩺</span>
        <div>
            <h1>Doctor Registration</h1>
            <p>Register as a healthcare professional to receive patient appointments and manage your schedule.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    specialties = [
        "General Physician", "Cardiologist", "Neurologist", "Pulmonologist",
        "Gastroenterologist", "Orthopedist", "Dermatologist", "Pediatrician",
        "Psychiatrist", "ENT Specialist", "Endocrinologist", "Rheumatologist"
    ]

    with st.form("doctor_registration", clear_on_submit=True):
        st.subheader("📋 Professional Details")
        
        col1, col2 = st.columns(2)
        with col1:
            doc_name = st.text_input("Full Name *", placeholder="Dr. John Smith")
            doc_specialty = st.selectbox("Specialty *", specialties)
            doc_phone = st.text_input("Phone Number", placeholder="+91 98765 43210")
        with col2:
            doc_email = st.text_input("Professional Email *", value=user_email)
            doc_city = st.text_input("City / Practice Location *", placeholder="Mumbai")
            
        col3, col4 = st.columns(2)
        with col3:
            doc_hospital = st.text_input("Hospital / Clinic Name *", placeholder="City Medical Center")
        with col4:
            doc_address = st.text_input("Full Address *", placeholder="123 Health Ave, Mumbai")
        
        st.markdown("---")
        submitted = st.form_submit_button("🩺 Register as Doctor", type="primary", use_container_width=True)
        
        if submitted:
            if not doc_name or not doc_email or not doc_specialty or not doc_city or not doc_hospital or not doc_address:
                st.error("Please fill in all required fields (marked with *).")
            else:
                with st.spinner("Registering..."):
                    success = register_doctor(
                        user_id=user_id,
                        name=doc_name,
                        email=doc_email,
                        specialty=doc_specialty,
                        phone=doc_phone,
                        city=doc_city,
                        hospital_name=doc_hospital,
                        hospital_address=doc_address
                    )
                    if success:
                        st.balloons()
                        st.success("🎉 **Registration successful!** You are now registered as a doctor.")
                        st.info("The page will refresh to show your dashboard.")
                        st.rerun()
                    else:
                        st.error("Registration failed. You may already be registered, or the database is unavailable.")

# ════════════════════════════════════════
# MODE 2: Doctor → Show Dashboard
# ════════════════════════════════════════
else:
    doc_name = doctor.get("name", "Doctor")
    doc_specialty = doctor.get("specialty", "")
    doc_city = doctor.get("city", "")
    doc_hospital = doctor.get("hospital_name", "Independent Clinic")
    doc_address = doctor.get("hospital_address", "")
    doc_email_val = doctor.get("email", "")

    st.markdown(f"""
    <div class="portal-header">
        <span style="font-size: 2.5rem;">🩺</span>
        <div>
            <h1>Welcome, Dr. {doc_name}</h1>
            <p>{doc_specialty} • {doc_city}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch appointments
    appointments = get_doctor_appointments(doctor["id"])
    today = datetime.date.today()

    # Categorize
    today_appts = []
    upcoming_appts = []
    past_appts = []

    for appt in appointments:
        appt_date = datetime.date.fromisoformat(appt["appointment_date"])
        if appt["status"] == "cancelled":
            past_appts.append(appt)
        elif appt_date == today:
            today_appts.append(appt)
        elif appt_date > today:
            upcoming_appts.append(appt)
        else:
            past_appts.append(appt)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-box"><div class="num">{len(today_appts)}</div><div class="lbl">Today</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-box"><div class="num">{len(upcoming_appts)}</div><div class="lbl">Upcoming</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-box"><div class="num">{len(past_appts)}</div><div class="lbl">Past</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-box"><div class="num">{len(appointments)}</div><div class="lbl">Total</div></div>""", unsafe_allow_html=True)

    st.markdown("")

    # ──────────────────────────────────────
    # Helper: Render Prescription Builder
    # ──────────────────────────────────────
    def render_prescription_builder(appt, key_prefix):
        """Render the advanced prescription builder for an appointment."""
        st.markdown("##### 💊 Write Prescription")

        all_meds = get_all_medicine_names()

        # Initialize session state for medicine rows
        med_key = f"med_count_{key_prefix}_{appt['id']}"
        if med_key not in st.session_state:
            st.session_state[med_key] = 1

        # Diagnosis
        diag = st.text_input("Diagnosis / Disease Name", key=f"diag_{key_prefix}_{appt['id']}")

        st.markdown("---")
        st.markdown("**Prescribed Medicines** — _Select a medicine to see details_")

        medicine_entries = []
        medicine_details_list = []

        for i in range(st.session_state[med_key]):
            st.markdown(f"###### Medicine {i+1}")
            mc1, mc2, mc3, mc4 = st.columns([3, 2, 2, 2])

            with mc1:
                # Searchable medicine selectbox
                selected_med = st.selectbox(
                    "Medicine Name",
                    options=[""] + all_meds,
                    key=f"med_name_{key_prefix}_{appt['id']}_{i}",
                    label_visibility="collapsed",
                    placeholder="🔍 Search medicine..."
                )
            with mc2:
                dosage = st.text_input("Dosage", placeholder="500mg", key=f"med_dose_{key_prefix}_{appt['id']}_{i}")
            with mc3:
                frequency = st.text_input("Frequency", placeholder="Twice daily", key=f"med_freq_{key_prefix}_{appt['id']}_{i}")
            with mc4:
                duration = st.text_input("Duration", placeholder="5 days", key=f"med_dur_{key_prefix}_{appt['id']}_{i}")

            # Show medicine info card when a medicine is selected
            if selected_med:
                med_info = get_medicine_info(selected_med)
                if med_info:
                    medicine_details_list.append(med_info)
                    side_fx = ", ".join(med_info.get("side_effects", [])[:4])
                    contra = ", ".join(med_info.get("contraindications", [])[:3])
                    st.markdown(f"""
<div class="med-info-card">
<div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
<div><span style="color: #00D68F; font-weight: 700;">{med_info['name']}</span> <span style="color: rgba(250,250,250,0.4); font-size: 0.8rem;">({med_info['generic_name']})</span></div>
<div style="font-size: 0.75rem; color: rgba(250,250,250,0.4);">{med_info['category']}</div>
</div>
<div style="margin-top: 0.5rem; font-size: 0.82rem; color: rgba(250,250,250,0.6);">
<b>Form:</b> {med_info['form']} &nbsp;|&nbsp; <b>Usual Dosage:</b> {med_info['common_dosage']} &nbsp;|&nbsp; <b>Max Daily:</b> {med_info['max_daily']}
</div>
<div style="margin-top: 0.4rem; font-size: 0.78rem;">
<span style="color: #FFB347;">⚠️ Side Effects:</span> <span style="color: rgba(250,250,250,0.5);">{side_fx}</span>
</div>
<div style="font-size: 0.78rem;">
<span style="color: #FF6B6B;">🚫 Contraindications:</span> <span style="color: rgba(250,250,250,0.5);">{contra}</span>
</div>
</div>
""", unsafe_allow_html=True)

                    medicine_entries.append({
                        "name": selected_med,
                        "dosage": dosage or med_info.get("common_dosage", ""),
                        "frequency": frequency or "As directed",
                        "duration": duration or "As directed"
                    })

        # Add/Remove medicine buttons
        add_col, rem_col = st.columns(2)
        with add_col:
            if st.button("➕ Add Another Medicine", key=f"add_med_{key_prefix}_{appt['id']}"):
                st.session_state[med_key] += 1
                st.rerun()
        with rem_col:
            if st.session_state[med_key] > 1:
                if st.button("➖ Remove Last", key=f"rem_med_{key_prefix}_{appt['id']}"):
                    st.session_state[med_key] -= 1
                    st.rerun()

        st.markdown("---")
        notes = st.text_area("Additional Notes / Advice", key=f"notes_{key_prefix}_{appt['id']}")

        # Action buttons
        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            if st.button("📄 Generate PDF & Send Email", key=f"send_presc_{key_prefix}_{appt['id']}", type="primary", use_container_width=True):
                if not diag or not medicine_entries:
                    st.error("Please enter a diagnosis and at least one medicine.")
                else:
                    with st.spinner("Generating prescription PDF..."):
                        # Generate PDF
                        pdf_bytes = generate_prescription_pdf(
                            hospital_name=doc_hospital,
                            hospital_address=doc_address,
                            doctor_name=doc_name,
                            doctor_specialty=doc_specialty,
                            doctor_email=doc_email_val,
                            patient_email=appt['patient_email'],
                            appointment_date=appt['appointment_date'],
                            diagnosis=diag,
                            medicines=medicine_entries,
                            medicine_details=medicine_details_list,
                            notes=notes
                        )

                        # Save to database
                        med_names = [m['name'] for m in medicine_entries]
                        save_prescription(
                            appt['id'], doctor['id'], appt['patient_id'],
                            appt['patient_email'], diag, med_names, notes
                        )

                        # Send email with PDF attachment
                        send_prescription_email(
                            appt['patient_email'],
                            doc_name,
                            doc_hospital,
                            diag,
                            medicine_entries,
                            notes,
                            pdf_bytes=pdf_bytes
                        )

                    st.success("✅ Prescription generated, saved, and emailed with PDF attachment!")

                    # Offer download
                    st.download_button(
                        label="📥 Download Prescription PDF",
                        data=pdf_bytes,
                        file_name=f"Prescription_{appt['patient_email'].split('@')[0]}_{datetime.date.today()}.pdf",
                        mime="application/pdf",
                        key=f"dl_sent_{key_prefix}_{appt['id']}"
                    )

        with btn_col2:
            if st.button("📥 Download PDF Only", key=f"dl_presc_{key_prefix}_{appt['id']}", use_container_width=True):
                if not diag or not medicine_entries:
                    st.error("Please enter a diagnosis and at least one medicine.")
                else:
                    with st.spinner("Generating PDF..."):
                        pdf_bytes = generate_prescription_pdf(
                            hospital_name=doc_hospital,
                            hospital_address=doc_address,
                            doctor_name=doc_name,
                            doctor_specialty=doc_specialty,
                            doctor_email=doc_email_val,
                            patient_email=appt['patient_email'],
                            appointment_date=appt['appointment_date'],
                            diagnosis=diag,
                            medicines=medicine_entries,
                            medicine_details=medicine_details_list,
                            notes=notes
                        )

                    st.download_button(
                        label="📥 Download Prescription PDF",
                        data=pdf_bytes,
                        file_name=f"Prescription_{appt['patient_email'].split('@')[0]}_{datetime.date.today()}.pdf",
                        mime="application/pdf",
                        key=f"dl_only_{key_prefix}_{appt['id']}"
                    )


    # ── Today's Appointments ──
    if today_appts:
        st.markdown("### 🟢 Today's Appointments")
        for appt in today_appts:
            st.markdown(f"""
            <div class="appt-card today">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <div class="appt-label">Patient</div>
                        <div class="appt-value">✉️ {appt['patient_email']}</div>
                    </div>
                    <div>
                        <div class="appt-label">Time</div>
                        <div class="appt-value">🕐 {appt['appointment_time'][:5]}</div>
                    </div>
                    <div>
                        <div class="appt-label">Specialty</div>
                        <div class="appt-value">{appt['specialty']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🛠️ Actions & Patient History"):
                # Patient History
                patient_history = get_user_predictions(appt['patient_id'])
                if patient_history:
                    st.markdown("##### 📂 Patient's Recent AI Symptom Reports")
                    for hist in patient_history[:3]:
                        st.caption(f"**Date:** {hist['created_at'][:10]} | **Predicted:** {hist.get('predicted_disease', 'N/A')} ({hist.get('confidence', 0)}%)")
                else:
                    st.caption("No recent symptom reports found for this patient.")
                    
                st.markdown("---")
                render_prescription_builder(appt, "tod")
                
                st.markdown("---")
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    st.link_button("🎥 Join Video Call", appt["meeting_url"], type="primary", use_container_width=True)
                with col_b:
                    if st.button("✅ Mark Completed", key=f"complete_{appt['id']}", use_container_width=True):
                        update_appointment_status(appt["id"], "completed")
                        st.rerun()
        st.markdown("---")

    # ── Upcoming Appointments ──
    if upcoming_appts:
        st.markdown("### 📅 Upcoming Appointments")
        for appt in upcoming_appts:
            appt_date = datetime.date.fromisoformat(appt["appointment_date"])
            days_until = (appt_date - today).days

            st.markdown(f"""
            <div class="appt-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <div class="appt-label">Patient</div>
                        <div class="appt-value">✉️ {appt['patient_email']}</div>
                    </div>
                    <div>
                        <div class="appt-label">Date</div>
                        <div class="appt-value">📆 {appt_date.strftime('%b %d, %Y')}</div>
                    </div>
                    <div>
                        <div class="appt-label">Time</div>
                        <div class="appt-value">🕐 {appt['appointment_time'][:5]}</div>
                    </div>
                    <div>
                        <div class="appt-label">In</div>
                        <div class="appt-value">{days_until} day{'s' if days_until != 1 else ''}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🛠️ Actions & Patient History"):
                # Patient History
                patient_history = get_user_predictions(appt['patient_id'])
                if patient_history:
                    st.markdown("##### 📂 Patient's Recent AI Symptom Reports")
                    for hist in patient_history[:3]:
                        st.caption(f"**Date:** {hist['created_at'][:10]} | **Predicted:** {hist.get('predicted_disease', 'N/A')} ({hist.get('confidence', 0)}%)")
                else:
                    st.caption("No recent symptom reports found for this patient.")
                    
                st.markdown("---")
                render_prescription_builder(appt, "up")
                
                st.markdown("---")
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    st.link_button("🔗 Meeting Link", appt["meeting_url"], use_container_width=True)
                with col_b:
                    if st.button("❌ Cancel", key=f"cancel_{appt['id']}", use_container_width=True):
                        update_appointment_status(appt["id"], "cancelled")
                        st.rerun()
    elif not today_appts:
        st.info("📭 No upcoming appointments. Patients can find and book you from the **👨‍⚕️ Book Appointment** page.")

    # ── Past Appointments ──
    if past_appts:
        with st.expander(f"📜 Past Appointments ({len(past_appts)})"):
            for appt in past_appts:
                status_icon = "✅" if appt["status"] == "completed" else "❌"
                appt_date = datetime.date.fromisoformat(appt["appointment_date"])
                st.markdown(f"""
                <div style="padding: 0.8rem; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
                    <span style="color: rgba(250,250,250,0.6);">{status_icon} {appt_date.strftime('%b %d, %Y')} at {appt['appointment_time'][:5]}</span>
                    <span style="color: rgba(250,250,250,0.4);">Patient: {appt['patient_email']}</span>
                </div>
                """, unsafe_allow_html=True)

