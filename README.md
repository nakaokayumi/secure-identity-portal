<div align="center">

# 🛡️ SECURITY CASE STUDY
### Project: Secure Identity & Access Management (IAM) Portal
**Candidate: Nakaoka Yumi**

---

</div>

<div style="border-right: 4px solid #ef4444; padding: 25px; background-color: #0d0d12; border-radius: 12px; border: 1px solid #2a2a35; border-right: 5px solid #ef4444;">

## 📌 Project Overview
This project is a full-stack **Secure Identity & Access Management (IAM) Portal** built with a "Security-First" mindset. I acted as the **Lead Security Developer**, focusing on protecting user data through backend logic, automated audit trails, and encrypted storage.

## 🚀 Process & Results
I utilized **Flask** for the backend and implemented **PBKDF2 password hashing (SHA-256)**. This ensures that even if the database is stolen, user passwords remain unreadable. The result is a functional, secure portal that tracks user logins for compliance auditing and handles the full user lifecycle securely.

</div>

<br>

## 🛠️ Key Technical Features
* **Secure Authentication:** Implements salted PBKDF2 password hashing to prevent plain-text exposure.
* **Session Security:** Configured with `HTTPOnly` and `SameSite` flags to mitigate XSS and CSRF attacks.
* **Audit Logging:** Automated tracking of `LOGIN_SUCCESS`, `LOGIN_FAILED`, and `PASSWORD_RESET` events.
* **Data Privacy (PDPA):** Features a "Danger Zone" for permanent account deletion, supporting the 'Right to be Forgotten'.

<br>

## 📊 Mapping to Industry Skills

| Skill | Implementation |
| :--- | :--- |
| **Networking & HTTP** | Managed RESTful routing and stateful sessions via Flask. |
| **Operating Systems** | Local deployment via Python Virtual Environments (venv). |
| **Confidentiality** | SQL injection prevention via parameterized queries and zero plain-text storage. |

<br>

## 🖥️ Preview & Technical Analysis
<img width="100%" alt="Audit Trail Preview" src="https://github.com/user-attachments/assets/3678eb84-5e5c-4f63-a5c7-13c496a5b1bd" />

> [!IMPORTANT]
> **Incident Response Readiness:** The system captures a chronological record of all critical actions. Each log entry includes the actor's **Email** and **IP Address**, providing the forensic data necessary to investigate unauthorized access attempts.

---

<div align="center">

**[🔗 View My Digital Portfolio](https://nakaokayumi.github.io/digital-portfolio/)**

</div>
