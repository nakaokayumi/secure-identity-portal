# Secure Identity & Access Management (IAM) Portal
### Built for Cybersecurity Portfolio & PDPA Compliance Demonstration

## 🛡️ Project Overview
This is a full-stack Flask web application designed with a "Security-First" mindset. It handles user lifecycle management—from registration to account deletion—while maintaining a rigorous audit trail and encrypted data storage.

## 🛠️ Key Technical Features
- **Secure Authentication:** Implements salted PBKDF2 password hashing (SHA-256).
- **Session Security:** Configured with `HTTPOnly` and `SameSite` flags to mitigate XSS and CSRF attacks.
- **Audit Logging:** Automated tracking of `LOGIN_SUCCESS`, `LOGIN_FAILED`, and `PASSWORD_RESET` events with IP address logging.
- **Data Privacy (PDPA):** Features a dedicated "Danger Zone" for permanent account deletion, supporting the 'Right to be Forgotten'.

## 📊 Mapping to Industry Skills
| Skill | Implementation |
| :--- | :--- |
| **Networking & HTTP** | Managed RESTful routing and stateful sessions via Flask. |
| **Operating Systems** | Local deployment via Python Virtual Environments (venv). |
| **Confidentiality** | Zero plain-text password storage; SQL injection prevention via parameterized queries. |

## 🚀 Cloud Readiness
This application is structured for easy containerization. Future deployment plans include:
- **Hosting:** AWS App Runner or Google Cloud Run.
- **Database:** Migrating from local SQLite to AWS RDS for production-grade scalability.

## 🖥️ Preview
*(Insert a screenshot of your beautiful Red & Black dashboard here!)*
