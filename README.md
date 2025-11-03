# 🔐 Secure Student Encryption

A **React.js + Python (Flask)** based web application for securely storing and managing student data.  
All student information (name, email, and marks) is **encrypted before storage** and can be **decrypted on demand**, ensuring data confidentiality and integrity.

---

## 📘 Features

- 🧑‍🎓 Add new student records with **encryption** applied automatically.
- 🔒 Encrypt sensitive fields such as:
  - Name  
  - Email  
  - English Marks  
  - Maths Marks  
  - Science Marks
- 🔓 Decrypt data instantly when needed.
- ⚡ Modern frontend built with **React.js**.
- 🐍 Secure backend powered by **Python (Flask)**.
- 📊 Displays decrypted student details in a clean and readable format.

---

## 🏗️ Tech Stack

**Frontend:**  
- React.js  
- Tailwind CSS (optional, if used for styling)  
- Axios (for API communication)

**Backend:**  
- Python  
- Flask  
- Cryptography library (for encryption/decryption)  
- JSON or database for data storage

---

## ⚙️ How It Works

1. The user enters student details on the frontend form.
2. Before saving, data is encrypted using a secret key on the **backend**.
3. Encrypted data is stored securely (e.g., in a file or database).
4. When viewing student data, the backend decrypts and sends it back to the frontend for display.

---

## 🖥️ Project Structure

secure-student-encryption/
├── backend/
│   ├── app.py                # Flask backend
│   ├── encryption_utils.py   # Encryption/Decryption logic
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── README.md
└── .gitignore

---

## 🚀 Getting Started

### 🧩 1. Clone the Repository

```bash
git clone https://github.com/anantyash1/secure-student-encryption.git
cd secure-student-encryption


💻 2. Setup the Frontend
cd frontend
npm install
npm start

The React app will start on http://localhost:3000.

🐍 3. Setup the Backend
cd backend
python -m venv .venv
.venv\Scripts\activate       # for PowerShell
pip install -r requirements.txt
python app.py

The Flask backend will run on http://127.0.0.1:5000.

🔗 4. Connect Frontend & Backend
Make sure your frontend API calls (e.g., using Axios) point to the Flask server (http://127.0.0.1:5000).

🧠 Example Encryption Flow
Input:
{
  "name": "John Doe",
  "email": "john@example.com",
  "english": 85,
  "maths": 90,
  "science": 88
}

Encrypted (stored) form:
{
  "name": "gAAAAABmR...==",
  "email": "gAAAAABmR...==",
  "english": "gAAAAABmR...==",
  "maths": "gAAAAABmR...==",
  "science": "gAAAAABmR...=="
}

Decrypted (displayed) form:
{
  "name": "John Doe",
  "email": "john@example.com",
  "english": 85,
  "maths": 90,
  "science": 88
}


🧰 Environment Variables (Optional)
Create a .env file in the backend with:
SECRET_KEY=your-secret-key-here


📜 License
This project is open-source under the MIT License.

👨‍💻 Author
Anant Yash
🔗 GitHub: anantyash1


---

Would you like me to make it look **fancier** (with badges, emojis for tech stack, and color highlights for commands) so it looks more like a professional open-source project on GitHub?
