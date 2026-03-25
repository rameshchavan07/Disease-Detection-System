"""
📊 Report History Page
Timeline-style view of past prediction results.
"""
import streamlit as st
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.database import get_user_predictions, delete_user_history
from modules.shared_ui import inject_premium_css, render_sidebar
from modules.pdf_generator import generate_report
from modules.disease_info import get_disease_info

st.set_page_config(page_title="Report History - MedDetect AI", page_icon="📊", layout="wide")

# Auth Check
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("🔒 Please sign in from the **🔑 Sign In** page to view your prediction history.")
    st.stop()

# Inject shared premium CSS & sidebar
inject_premium_css()
render_sidebar()

# Page-specific CSS
st.markdown("""
<style>

.page-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.page-header h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.timeline-card {
    background: linear-gradient(145deg, rgba(26,29,41,0.85), rgba(26,29,41,0.5));
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.timeline-card:hover {
    border-color: rgba(108,99,255,0.3);
    transform: translateX(4px);
    box-shadow: 0 8px 24px rgba(108,99,255,0.08);
}

.timeline-card::before {
    content: '';
    position: absolute;
    left: -2rem;
    top: 50%;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #6C63FF;
    transform: translateY(-50%);
    box-shadow: 0 0 10px rgba(108,99,255,0.5);
}

.timeline-line {
    border-left: 2px solid rgba(108,99,255,0.15);
    padding-left: 2rem;
    margin-left: 0.3rem;
}

.report-number {
    font-size: 1.1rem;
    font-weight: 700;
    color: #6C63FF;
}

.report-time {
    font-size: 0.8rem;
    color: rgba(250,250,250,0.4);
}

.report-disease {
    font-size: 1rem;
    font-weight: 600;
    color: #FAFAFA;
}

.report-confidence {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 600;
}

.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: rgba(250,250,250,0.3);
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    animation: emptyBounce 3s ease-in-out infinite;
}

@keyframes emptyBounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <span style="font-size: 2.5rem;">📊</span>
    <h1>Report History</h1>
</div>
""", unsafe_allow_html=True)
st.markdown(f"<p style='color: rgba(250,250,250,0.5); margin-bottom: 1.5rem;'>Viewing reports for <strong style='color: #6C63FF;'>{st.session_state.user_email}</strong></p>", unsafe_allow_html=True)

# Get data
user_id = st.session_state.user_id
history = get_user_predictions(user_id)

if history:
    # Stats bar
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("Total Reports", len(history))
    with col_s2:
        latest = history[0] if history else {}
        st.metric("Latest Disease", latest.get('predicted_disease', 'N/A'))
    with col_s3:
        st.metric("Latest Confidence", f"{latest.get('confidence', 0)}%")
    
    st.markdown("---")
    
    # Timeline view
    st.markdown('<div class="timeline-line">', unsafe_allow_html=True)
    
    for i, record in enumerate(history):
        try:
            dt_obj = datetime.fromisoformat(record['created_at'].replace('Z', '+00:00'))
            formatted_time = dt_obj.strftime("%b %d, %Y • %I:%M %p")
        except:
            formatted_time = record['created_at']
        
        confidence = record.get('confidence', 0)
        if confidence > 70:
            conf_bg = "rgba(0,214,143,0.1)"
            conf_color = "#00D68F"
        elif confidence > 40:
            conf_bg = "rgba(255,170,0,0.1)"
            conf_color = "#FFAA00"
        else:
            conf_bg = "rgba(255,61,113,0.1)"
            conf_color = "#FF3D71"
            
        st.markdown(f"""
        <div class="timeline-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; flex-wrap: wrap; gap: 0.5rem;">
                <span class="report-number">Report #{len(history) - i}</span>
                <span class="report-time">🕐 {formatted_time}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <span class="report-disease">🏥 {record.get('predicted_disease', 'Unknown')}</span>
                <span class="report-confidence" style="background: {conf_bg}; color: {conf_color};">
                    {confidence}% confidence
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📋 Details — Report #{len(history) - i}"):
            symptoms = record.get("symptoms", [])
            if isinstance(symptoms, str):
                import ast
                try:
                    symptoms = ast.literal_eval(symptoms)
                except:
                    symptoms = [symptoms]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Selected Symptoms:**")
                for s in symptoms:
                    st.markdown(f"• {s}")
            with col2:
                st.markdown("**Prediction:**")
                st.markdown(f"• **{record.get('predicted_disease', 'N/A')}** — {confidence}% confidence")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                disease_name = record.get('predicted_disease', 'Unknown')
                info = get_disease_info(disease_name)
                predictions_list = [{"rank": 1, "disease": disease_name, "confidence": confidence}]
                
                # Generate PDF Bytes
                try:
                    pdf_bytes = generate_report(
                        st.session_state.get("user_email", "Patient").split("@")[0].title(),
                        st.session_state.get("user_email", "Not provided"),
                        symptoms, 
                        predictions_list, 
                        {disease_name: info}
                    )
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"MedDetect_Report_{i+1}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"dl_report_{i}"
                    )
                except Exception as e:
                    st.error(f"Error generating report: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    col_d1, col_d2, col_d3 = st.columns([1,1,1])
    with col_d2:
        if st.button("🗑️ Clear All History", type="secondary", use_container_width=True):
            delete_user_history(user_id)
            st.rerun()
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📋</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: rgba(250,250,250,0.5); margin-bottom: 0.5rem;">No Reports Yet</div>
        <p style="color: rgba(250,250,250,0.35); max-width: 400px; margin: 0 auto; line-height: 1.6;">
            Head over to the <strong>🔍 Symptom Checker</strong> to analyze your symptoms and generate your first health report.
        </p>
    </div>
    """, unsafe_allow_html=True)

from modules.floating_chat import render_floating_chatbot
render_floating_chatbot()
