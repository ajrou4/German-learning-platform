# 🇩🇪 AI-Powered German Learning Platform

A comprehensive full-stack web application for learning German, powered by AI. Features include interactive lessons, AI chatbot tutor, real-time translation, speech recognition, and progress tracking.

![Tech Stack](https://img.shields.io/badge/Django-5.0-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue))
![AI](https://img.shields.io/badge/AI-OpenAI-orange)

## ✨ Features

### 🎓 Learning System
- **Structured Courses**: Organized by CEFR levels (A1-C2)
- **Interactive Lessons**: Vocabulary, grammar, exercises, reading, and listening
- **Progress Tracking**: Track completion, scores, and learning streaks
- **Gamification**: Achievements and badges for motivation

### 🤖 AI-Powered Features
- **AI Translator**: German ↔ English/Arabic with grammar explanations
- **Sentence Generator**: Context-aware example sentences
- **AI Chatbot Tutor**: Three modes (Beginner, Grammar, Conversation)
- **Speech-to-Text**: Coming soon (requires Google Cloud Speech API)
- **Text-to-Speech**: Coming soon (requires Google Cloud TTS API)

### 📊 User Features
- **Personal Dashboard**: View stats, streaks, and achievements
- **Profile Management**: Track language level and preferences
- **Dark Mode**: Beautiful dark/light theme support
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🏗️ Tech Stack

### Backend
- **Django 5.0** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Redis** - Caching and Celery broker
- **Google Gemini API** - AI features (translation, chat, sentence generation)
- **JWT** - Authentication

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **React Query** - Data fetching
- **Zustand** - State management
- **Axios** - HTTP client
- **Framer Motion** - Animations

### DevOps
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD (optional)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Google API key with Gemini API enabled (for AI features)

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd german-learning-platform
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:
```env
GOOGLE_API_KEY=your-google-api-key-here
```

3. **Start the application**
```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin

### First-Time Setup

1. **Create a superuser** (in a new terminal):
```bash
docker-compose exec backend python manage.py createsuperuser
```

2. **Add sample data** (optional):
```bash
docker-compose exec backend python manage.py loaddata sample_data.json
```

## 📁 Project Structure

```
german-learning-platform/
├── backend/                 # Django backend
│   ├── config/             # Django settings
│   ├── users/              # User authentication
│   ├── courses/            # Course management
│   ├── lessons/            # Lesson content
│   ├── progress/           # Progress tracking
│   ├── ai_engine/          # AI services
│   ├── chat/               # AI chatbot
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── store/         # State management
│   │   └── App.jsx
│   └── package.json
├── nginx/                  # Nginx configuration
├── docker-compose.yml      # Docker orchestration
└── README.md
```

## 🔧 Development

### Backend Development

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create migrations
docker-compose exec backend python manage.py makemigrations

# Run tests
docker-compose exec backend python manage.py test

# Access Django shell
docker-compose exec backend python manage.py shell
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 📚 API Documentation

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update profile

### Courses & Lessons
- `GET /api/courses/` - List courses
- `GET /api/courses/{id}/` - Get course details
- `GET /api/lessons/` - List lessons
- `GET /api/lessons/{id}/` - Get lesson details
- `POST /api/lessons/{id}/complete/` - Mark lesson complete

### AI Features
- `POST /api/ai/translate/` - Translate text
- `POST /api/ai/generate-sentences/` - Generate example sentences
- `POST /api/ai/speech-to-text/` - Convert speech to text
- `POST /api/ai/text-to-speech/` - Convert text to speech
- `POST /api/ai/pronunciation/` - Check pronunciation

### Chat
- `GET /api/chat/sessions/` - List chat sessions
- `POST /api/chat/send/` - Send message to AI tutor
- `DELETE /api/chat/sessions/{id}/clear/` - Clear chat history

### Progress
- `GET /api/progress/` - Get user progress
- `GET /api/progress/streak/` - Get learning streak
- `GET /api/progress/achievements/` - Get achievements
- `GET /api/progress/dashboard/` - Get dashboard stats

## 🎨 UI Screenshots

### Dashboard
Beautiful dashboard with statistics, streaks, and quick actions.

### AI Chat
Interactive chatbot with three learning modes.

### Translator
Real-time translation with grammar explanations and word breakdown.

## 🔐 Security

- JWT-based authentication
- CORS protection
- Environment variable management
- Rate limiting on AI endpoints
- Input validation and sanitization

## 🌍 Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Build frontend**:
```bash
cd frontend)
npm run build
```

3. **Start with production profile**:
```bash
docker-compose --profile production up -d
```

4. **Collect static files**:
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### Recommended Hosting
- **Backend**: Railway, Render, DigitalOcean
- **Frontend**: Vercel, Netlify
- **Database**: Managed PostgreSQL (AWS RDS, DigitalOcean)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**moahmed**
- GitHub: [ajrou4](https://github.com/ajrou4)
- LinkedIn: [majrou](https://linkedin.com/in/majrou)

## 🙏 Acknowledgments

- Google for Gemini API
- Django and React communities
- All contributors and testers

## 📧 Contact

For questions or support, please open an issue or contact [your-email@example.com](mailto:your-email@example.com)

---

**Made with ❤️ for German language learners**
