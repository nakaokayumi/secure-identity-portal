# 🛡️ SECURITY CASE STUDY  
## Secure Identity & Access Management (IAM) Portal  
**Candidate:** Nakaoka Yumi  

---

## 📌 Project Overview  
This project is a full-stack Secure Identity & Access Management (IAM) Portal built with a security-first design approach. I independently designed, developed, and deployed the system, focusing on protecting user data through secure authentication logic, structured audit logging, and encrypted credential storage.

---

## 🚀 Process & Results  
The backend was developed using Flask, with PBKDF2 password hashing (SHA-256) implemented to securely store user credentials. This ensures passwords remain protected even if the database is compromised.  

The system provides a functional secure login environment that records authentication activity for monitoring and traceability, while managing the full user lifecycle from registration to account access and deletion.

---

## 🛠️ Key Technical Features  

### Secure Authentication  
Implements salted PBKDF2 password hashing to prevent plaintext credential storage.

### Session Security  
Server-side session controls restrict access to authenticated users and protect protected routes.

### Audit Logging  
Login activity is recorded with timestamps and IP address data to support monitoring and investigation of suspicious activity.

### Data Privacy Controls  
Includes permanent account deletion functionality, supporting user control over stored personal data.

---

## 📊 Mapping to Industry Skills  

| Skill | Implementation |
|---|---|
| Networking & HTTP | Implemented routing, authentication flows, and session handling using Flask |
| Environment Management | Local development using Python virtual environments (venv) |
| Data Confidentiality | Prevented SQL injection with parameterized queries and enforced encrypted password storage |

---

## 🖥️ Preview & Technical Analysis  

### Audit Trail Preview  

**Forensic Traceability**  
The system maintains a chronological record of authentication activity, including user email and IP address. This provides useful data for reviewing login behaviour and investigating unauthorized access attempts.

---

## ☁️ Tech Stack  

- Python (Flask)  
- PostgreSQL (Supabase)  
- Render (Cloud Hosting)  
- PBKDF2 SHA-256 Password Hashing  
- Server-Side Session Management  

---

## 🔗 Live Application  
https://secure-identity-portal-render-version.onrender.com

## 🔗 Digital Portfolio  
https://nakaokayumi.github.io/digital-portfolio/

---

## 🚀 Future Improvements  

- Multi-factor authentication (MFA)  
- Role-based access control (RBAC)  
- OAuth / Single Sign-On (SSO)  
- Real-time threat detection alerts  
- Containerized deployment with Docker  

---
