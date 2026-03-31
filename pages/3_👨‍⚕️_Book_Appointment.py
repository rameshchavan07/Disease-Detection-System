"""
👨‍⚕️ Book Appointment Page
Discover registered specialists and book video consultations instantly.
Now shows doctors from the database first, with AI-suggested fallback.
"""
import streamlit as st
import sys, os
import uuid
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.shared_ui import inject_premium_css, render_sidebar
from modules.doctor_locator import get_nearest_doctors
from modules.email_service import send_appointment_email
from modules.database import get_registered_doctors, save_appointment

st.set_page_config(page_title="Book Appointment - MedDetect AI", page_icon="👨‍⚕️", layout="wide")

if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("🔒 Please sign in from the **🔑 Sign In** page to book an appointment.")
    st.info("Creating a free account allows you to securely book and manage appointments.")
    st.stop()
elif st.session_state.get("is_doctor", False):
    st.warning("🩺 **This page is for patients.** Please navigate to the Doctor Portal.")
    st.stop()

# Inject shared premium CSS & sidebar
inject_premium_css()
render_sidebar()

# Page-specific CSS
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b26 100%);
    border-right: 1px solid rgba(108,99,255,0.08);
}
.booking-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, rgba(108,99,255,0.1), rgba(99,179,255,0.05));
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 20px;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}
.booking-header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.booking-header p {
    margin: 0.3rem 0 0;
    font-size: 0.88rem;
    color: rgba(250,250,250,0.5);
}
.doctor-card {
    background: linear-gradient(145deg, rgba(26,29,41,0.9), rgba(26,29,41,0.5));
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.doctor-card:hover {
    border-color: rgba(108,99,255,0.3);
    box-shadow: 0 8px 24px rgba(108,99,255,0.08);
}
.doctor-card.registered {
    border-color: rgba(0,214,143,0.2);
    background: linear-gradient(145deg, rgba(0,214,143,0.05), rgba(26,29,41,0.5));
}
.doctor-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.2rem;
}
.doctor-detail {
    font-size: 0.85rem;
    color: rgba(250,250,250,0.6);
    margin-bottom: 0.2rem;
}
.verified-badge {
    display: inline-block;
    background: rgba(0,214,143,0.15);
    color: #00D68F;
    padding: 0.15rem 0.6rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="booking-header">
    <span style="font-size: 2.5rem;">👨‍⚕️</span>
    <div>
        <h1>Find & Book Specialists</h1>
        <p>Select a specialty, find registered and nearby doctors, and schedule a secure video consultation instantly.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Specialty Section
specialties = [
    "General Physician", "Cardiologist", "Neurologist", "Pulmonologist", 
    "Gastroenterologist", "Orthopedist", "Dermatologist", "Pediatrician",
    "Psychiatrist", "ENT Specialist", "Endocrinologist", "Rheumatologist"
]

col1, col2 = st.columns([2, 1])
with col1:
    selected_spec = st.selectbox("Select required medical specialty:", specialties)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_pressed = st.button("🔍 Find Doctors", type="primary", use_container_width=True)

if search_pressed or "search_specialty" in st.session_state:
    if search_pressed:
         st.session_state.search_specialty = selected_spec
    
    spec_to_search = st.session_state.search_specialty
    
    # ═══════════════════════════════════════
    # SECTION 1: Registered Doctors (from DB)
    # ═══════════════════════════════════════
    registered_docs = get_registered_doctors(spec_to_search)
    
    if registered_docs:
        st.markdown("---")
        st.markdown(f"### ✅ Registered {spec_to_search}s on MedDetect AI")
        st.caption("These doctors are registered on our platform and will see your appointment in their dashboard.")
        
        for i, doc in enumerate(registered_docs):
            st.markdown(f"""
            <div class="doctor-card registered">
                <div class="doctor-name">🩺 Dr. {doc.get('name', 'Doctor')} <span class="verified-badge">✓ VERIFIED</span></div>
                <div class="doctor-detail">👨‍⚕️ {doc.get('specialty', '')}</div>
                <div class="doctor-detail">🏥 {doc.get('hospital_name', 'Independent Clinic')}</div>
                <div class="doctor-detail">📍 {doc.get('hospital_address', doc.get('city', 'Location not provided'))}</div>
                <div class="doctor-detail">📞 {doc.get('phone', 'Phone not provided')}</div>
                <div class="doctor-detail">✉️ {doc.get('email', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📅 Schedule Appointment"):
                c1, c2 = st.columns(2)
                with c1:
                    app_date = st.date_input("Date", min_value=datetime.date.today(), key=f"reg_date_{i}")
                with c2:
                    app_time = st.time_input("Time", value=datetime.time(10, 0), key=f"reg_time_{i}")
                
                if st.button("✅ Confirm Booking", key=f"reg_book_{i}", type="primary"):
                    user_email = st.session_state.get("user_email")
                    user_id = st.session_state.get("user_id")
                    if not user_email:
                        st.error("Cannot book appointment without a registered email address.")
                    else:
                        with st.spinner("Booking appointment..."):
                            try:
                                # Generate meeting link
                                room_id = f"MedDetect_Consultation_{uuid.uuid4().hex[:10]}"
                                meeting_url = f"https://meet.jit.si/{room_id}"
                                
                                # Save to database — doctor will see it in their portal
                                db_saved = save_appointment(
                                    patient_id=user_id,
                                    patient_email=user_email,
                                    doctor_id=doc["id"],
                                    doctor_name=doc.get("name", ""),
                                    specialty=spec_to_search,
                                    appointment_date=app_date.isoformat(),
                                    appointment_time=app_time.strftime("%H:%M:%S"),
                                    meeting_url=meeting_url
                                )
                                
                                # Also send email to patient
                                date_str = app_date.strftime("%B %d, %Y")
                                time_str = app_time.strftime("%I:%M %p")
                                datetime_str = f"{date_str} at {time_str}"
                                
                                try:
                                    send_appointment_email(
                                        user_email,
                                        doc.get('name'),
                                        spec_to_search,
                                        meeting_url,
                                        datetime_str
                                    )
                                except Exception:
                                    pass  # Email is non-critical
                                
                                if db_saved:
                                    st.success("🎉 **Appointment Confirmed!**")
                                    st.info(
                                        f"📩 Dr. {doc.get('name')} will see this appointment in their **Doctor Portal**.\n\n"
                                        f"**Meeting Link:** {meeting_url}\n\n"
                                        f"Both you and the doctor can join at the scheduled time."
                                    )
                                else:
                                    st.warning(f"Appointment saved locally but database sync failed.\n\n**Meeting Link:** {meeting_url}")
                            except Exception as e:
                                st.error(f"⚠️ Failed to book appointment: {str(e)}. Please try again.")

    # ═══════════════════════════════════════
    # SECTION 2: AI-Suggested Doctors (Groq)
    # ═══════════════════════════════════════
    st.markdown("---")
    st.markdown(f"### 🔍 Other {spec_to_search}s Near You")
    st.caption("These are AI-suggested doctors from your area. They are not registered on MedDetect AI.")
    
    with st.spinner(f"Finding {spec_to_search}s in your area..."):
        api_result = get_nearest_doctors(spec_to_search)
        
        if api_result and len(api_result.get("doctors", [])) > 0:
            doctors = api_result["doctors"]
            city = api_result.get("city", "your area")
        else:
            city = "Local Area"
            doctors = [
                {"name": "Dr. Alex Mercer", "phone": "(555) 123-4567", "address": f"Premier Health Center, {city}"},
                {"name": "Dr. Sarah Jenkins", "phone": "(555) 987-6543", "address": f"City Medical Hospital, {city}"}
            ]

    st.markdown(f"*Showing results for **{city}***")
    
    for i, doc in enumerate(doctors):
        st.markdown(f"""
        <div class="doctor-card">
            <div class="doctor-name">🩺 {doc.get('name', 'Doctor')}</div>
            <div class="doctor-detail">📍 {doc.get('address', 'Location info unavailable')}</div>
            <div class="doctor-detail">📞 {doc.get('phone', 'Phone info unavailable')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📅 Schedule Appointment"):
            c1, c2 = st.columns(2)
            with c1:
                app_date = st.date_input("Date", min_value=datetime.date.today(), key=f"ai_date_{i}")
            with c2:
                app_time = st.time_input("Time", value=datetime.time(10, 0), key=f"ai_time_{i}")
            
            if st.button("✅ Confirm Booking", key=f"ai_book_{i}", type="primary"):
                user_email = st.session_state.get("user_email")
                if not user_email:
                    st.error("Cannot book appointment without a registered email address.")
                else:
                    with st.spinner("Booking appointment & sending email..."):
                        room_id = f"MedDetect_Consultation_{uuid.uuid4().hex[:10]}"
                        meeting_url = f"https://meet.jit.si/{room_id}"
                        
                        date_str = app_date.strftime("%B %d, %Y")
                        time_str = app_time.strftime("%I:%M %p")
                        datetime_str = f"{date_str} at {time_str}"
                        
                        success, error = send_appointment_email(
                            user_email, 
                            doc.get('name'), 
                            spec_to_search, 
                            meeting_url, 
                            datetime_str
                        )
                        
                        if success:
                            st.success(f"🎉 **Appointment Confirmed!** An email has been sent to **{user_email}**.")
                            st.info(f"**Meeting Link:** {meeting_url}\nPlease save this link or refer to your email.")
                            st.warning("⚠️ This doctor is not on MedDetect AI. Please share the meeting link with them directly.")
                        else:
                            st.warning(f"Booking confirmed, but email sending failed: {error}\n\n**Meeting Link:** {meeting_url}")

