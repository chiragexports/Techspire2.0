# 🚀 Techspire — Premium Educational Platform (v2.0)

Techspire is a full-stack technical education and credential platform designed for computer science mastery. It features an interactive learning engine, assessment evaluations, automated professional technical credential issuance, single-page print engine, and integrated Razorpay course commerce.

---

## 🏗️ Architecture

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons, Canvas Confetti
- **Backend**: Django REST Framework, SimpleJWT Authentication, WhiteNoise, dj-database-url, Gunicorn
- **Database**: PostgreSQL (Production) / SQLite (Local Adaptive Development)
- **Payment & Commerce**: Razorpay Standard Checkout with Server-Side HMAC-SHA256 Signature Verification and Idempotent Webhook Processing
- **Deployment**: Vercel (Frontend Next.js) + Render/Railway/Heroku/AWS (Backend Django REST API)

---

## ⚡ Quick Start

### 1. Backend Setup (Django REST API)
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # On Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_techspire
python manage.py runserver
```

### 2. Frontend Setup (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the application.

---

## 🧪 Testing & Verification
```bash
# Run backend test suite
cd backend
python manage.py test

# Build frontend production bundle
cd frontend
npm run build
```

---

## 🔒 Security & Environment Variables
Refer to `backend/.env.example` and `frontend/.env.example` for environment variable templates. Never commit `.env` files with secret keys.
