# Instant Tutor AI - Project Structure

## 📁 Directory Organization

```
instant-tutor-ai/
├── 📁 backend/                    # Backend API and services
│   ├── 📁 api/                   # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── main.py               # Main FastAPI application
│   │   └── legacy_main.py        # Legacy main file
│   ├── 📁 core/                  # Core configuration
│   │   ├── __init__.py
│   │   └── secure_config.py      # Security configuration
│   ├── 📁 database/              # Database connections
│   │   ├── __init__.py
│   │   ├── weaviate_setup.py     # Weaviate vector database
│   │   └── pinecone_setup.py     # Pinecone vector database
│   ├── 📁 services/              # Business logic
│   │   ├── __init__.py
│   │   └── video_processor.py    # Video processing pipeline
│   ├── 📁 utils/                 # Utility functions
│   │   ├── __init__.py
│   │   └── jwt_utils.py          # JWT authentication
│   └── 📁 tests/                 # Backend tests
│       └── __init__.py
├── 📁 frontend/                  # React frontend (to be created)
│   ├── 📁 src/
│   │   ├── 📁 components/        # React components
│   │   ├── 📁 pages/            # Page components
│   │   ├── 📁 services/         # API services
│   │   └── 📁 utils/            # Frontend utilities
│   └── 📁 public/               # Static assets
├── 📁 docs/                     # Documentation
│   └── implementation_guide.md  # Complete implementation guide
├── 📁 deployment/               # Deployment configurations
│   └── docker-compose.yml       # Docker setup
├── 📁 tests/                    # Integration tests
│   └── test_api.py              # API tests
├── 📁 config/                   # Configuration files
│   └── env.example              # Environment template
├── 📁 logs/                     # Application logs
├── 📁 uploads/                  # File uploads
├── 📄 main.py                   # Main entry point
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Project documentation
├── 📄 .gitignore               # Git ignore rules
└── 📄 PROJECT_STRUCTURE.md     # This file
```

## 🏗️ Architecture Overview

### Backend Structure
- **API Layer** (`backend/api/`): FastAPI endpoints and request handling
- **Core Layer** (`backend/core/`): Configuration and security
- **Database Layer** (`backend/database/`): Vector database connections
- **Services Layer** (`backend/services/`): Business logic and processing
- **Utils Layer** (`backend/utils/`): Helper functions and utilities

### Frontend Structure (To Be Created)
- **Components** (`frontend/src/components/`): Reusable UI components
- **Pages** (`frontend/src/pages/`): Page-level components
- **Services** (`frontend/src/services/`): API communication
- **Utils** (`frontend/src/utils/`): Frontend utilities

## 🔧 Key Files

### Backend Files
- `backend/api/main.py` - Main FastAPI application
- `backend/services/video_processor.py` - Video processing pipeline
- `backend/database/weaviate_setup.py` - Weaviate vector database
- `backend/database/pinecone_setup.py` - Pinecone vector database
- `backend/utils/jwt_utils.py` - JWT authentication
- `backend/core/secure_config.py` - Security configuration

### Configuration Files
- `config/env.example` - Environment variables template
- `deployment/docker-compose.yml` - Docker services
- `requirements.txt` - Python dependencies

### Documentation
- `README.md` - Project overview and setup
- `docs/implementation_guide.md` - Complete implementation guide
- `PROJECT_STRUCTURE.md` - This file

## 🚀 Getting Started

### 1. Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the backend
python main.py
```

### 2. Frontend Development (To Be Created)
```bash
# Create React app
cd frontend
npx create-react-app . --template typescript
npm install @mui/material @emotion/react @emotion/styled
npm install axios react-router-dom
```

### 3. Database Setup
```bash
# Start Weaviate
cd deployment
docker-compose up -d
```

## 📋 Development Workflow

### Adding New Features
1. **API Endpoints**: Add to `backend/api/`
2. **Business Logic**: Add to `backend/services/`
3. **Database Models**: Add to `backend/database/`
4. **Utilities**: Add to `backend/utils/`
5. **Frontend Components**: Add to `frontend/src/components/`

### Testing
- **Unit Tests**: `backend/tests/`
- **Integration Tests**: `tests/`
- **API Tests**: `tests/test_api.py`

### Deployment
- **Docker**: `deployment/docker-compose.yml`
- **Configuration**: `config/env.example`
- **Documentation**: `docs/`

## 🔒 Security

### JWT Authentication
- **Secret Key**: Generated secure key in `backend/core/secure_config.py`
- **Token Management**: `backend/utils/jwt_utils.py`
- **Role-Based Access**: Student, Instructor, Admin roles

### Environment Variables
- **Development**: Copy `config/env.example` to `.env`
- **Production**: Use secure environment variables
- **Secrets**: Never commit sensitive data

## 📊 Monitoring

### Logs
- **Application Logs**: `logs/`
- **Error Tracking**: Integrated with FastAPI
- **Performance**: Response time monitoring

### Analytics
- **User Engagement**: Track query patterns
- **Performance Metrics**: Response times and accuracy
- **Business Metrics**: User satisfaction and cost savings

## 🎯 Kerala Market Features

### Language Support
- **English**: Primary language
- **Malayalam**: Local language support
- **Hindi**: Additional language support

### Curriculum Alignment
- **SCERT**: Kerala state curriculum
- **CBSE**: Central board curriculum
- **ICSE**: Indian certificate curriculum

### Local Integration
- **KSUM**: Kerala Startup Mission alignment
- **Government Schemes**: Digital Kerala integration
- **Local EdTech**: Compatible with existing platforms

## 📈 Scaling Strategy

### MVP Phase
- **Users**: 100-1000 students
- **Infrastructure**: Local server/cloud
- **Cost**: ₹18,000-27,000/month

### Scale Phase
- **Users**: 10,000+ students
- **Infrastructure**: Cloud-native
- **Cost**: ₹45,000-75,000/month

## 🤝 Contributing

### Code Organization
- **Backend**: Python/FastAPI
- **Frontend**: React/TypeScript
- **Database**: PostgreSQL + Vector DB
- **AI**: OpenAI + Whisper + Sentence Transformers

### Development Standards
- **Code Style**: Black, Flake8
- **Testing**: Pytest
- **Documentation**: Markdown
- **Version Control**: Git

---

**Built with ❤️ for Kerala's Education Future**
