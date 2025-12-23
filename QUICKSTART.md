# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google API key
nano .env
```

### 2. Start with Docker
```bash
# Build and start all services
docker-compose up --build

# In a new terminal, create superuser
docker-compose exec backend python manage.py createsuperuser
```

### 3. Access the App
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📝 Default Credentials
After creating a superuser, you can:
1. Login to admin panel to add sample courses
2. Register a new account on the frontend
3. Start learning German!

## 🎯 Next Steps
1. Add courses via Django admin
2. Create lessons and vocabulary
3. Test AI features (requires OpenAI API key)
4. Customize the UI in `frontend/src/`

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "5174:5173"  # Frontend
```

**Database issues?**
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

**Frontend not loading?**
```bash
# Rebuild frontend
cd frontend
npm install
npm run build
```

## 📚 Learn More
- See [README.md](README.md) for full documentation
- Check [API Documentation](#) for endpoint details
- Visit Django admin to manage content
