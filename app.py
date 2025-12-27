from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    issue = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ref_id = db.Column(db.String(20), unique=True, nullable=False)

# ========== 🔑 CHANGE THESE ==========
EMAIL_SENDER = "hemachelli5@gmail.com"      # 👈 Nee Gmail
EMAIL_PASSWORD = "tome pmbp ayzg hyxq"       # 👈 App password
# =====================================

def send_email(to_email, ref_id, city, area, street, issue_type):
    """Send email with ALL details"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        msg['Subject'] = f"Smart City Lab - Issue Report #{ref_id}"
        
        # Email body with ALL details
        current_time = datetime.now().strftime("%d %B, %Y at %I:%M %p")
        
        body = f"""
        SMART CITY LAB - ISSUE REPORT CONFIRMATION
        
        ✅ ISSUE REPORTED SUCCESSFULLY
        
        Reference ID: {ref_id}
        
        📋 ISSUE DETAILS:
        -----------------
        Issue Type: {issue_type}
        City: {city}
        Area: {area}
        Street/Location: {street}
        Reported Date & Time: {current_time}
        Current Status: Pending Verification
        Expected Verification: Within 24 hours
        
        📈 NEXT STEPS:
        1. Our team will verify the issue
        2. Sensor-based validation will be initiated
        3. Issue will be assigned for resolution
        4. You'll be notified when resolved
        
        Thank you for helping build a smarter city!
        
        Smart City Lab Team
        kietsmartcitylab@gmail.com
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get ALL form data
        city = request.form.get('city', '').strip()
        area = request.form.get('area', '').strip()
        street = request.form.get('street', '').strip()
        issue = request.form.get('issue', '').strip()
        email = request.form.get('email', '').strip()
        
        # Generate reference ID
        ref_id = str(uuid.uuid4())[:8].upper()
        
        # Save to database
        new_report = Report(
            city=city,
            area=area,
            street=street,
            issue=issue,
            email=email,
            ref_id=ref_id
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        # Send email with ALL details
        email_sent = send_email(email, ref_id, city, area, street, issue)
        
        # Return response
        if email_sent:
            message = f"""
            <div style='background:#d4edda; padding:20px; border-radius:10px;'>
            <h3 style='color:#155724;'>✅ Report Submitted Successfully!</h3>
            <p><strong>Reference ID:</strong> {ref_id}</p>
            <p><strong>Issue:</strong> {issue}</p>
            <p><strong>Location:</strong> {city}, {area}, {street}</p>
            <p>Confirmation email sent to: <strong>{email}</strong></p>
            <p>Please check your inbox.</p>
            </div>
            """
        else:
            message = f"""
            <div style='background:#fff3cd; padding:20px; border-radius:10px;'>
            <h3 style='color:#856404;'>⚠️ Report Submitted</h3>
            <p><strong>Reference ID:</strong> {ref_id}</p>
            <p><strong>Issue:</strong> {issue}</p>
            <p><strong>Location:</strong> {city}, {area}, {street}</p>
            <p>Report saved. Please note your Reference ID.</p>
            </div>
            """
        
        return jsonify({
            "success": True,
            "message": message,
            "ref_id": ref_id
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("🚀 Server starting... Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)