# Instant Tutor AI - AI-Powered EdTech MVP

An intelligent tutoring system that replaces traditional weekly Q&A forums with instant, course-specific AI responses using vector databases.

## 🎯 Project Overview

This MVP demonstrates how AI can transform education in Kerala by providing instant, intelligent answers to student questions using course video content and vector database technology.

## 🚀 Key Features

- **Instant Q&A**: Get immediate answers to course-related questions
- **Video Content Processing**: Extract knowledge from course videos using Whisper and vector embeddings
- **Vector Database Integration**: Support for both Weaviate and Pinecone
- **Kerala Market Focus**: Malayalam language support and local curriculum alignment
- **Scalable Architecture**: FastAPI backend with React frontend

## 🏗️ Architecture

```
Frontend (React) ←→ FastAPI Backend ←→ Vector DB (Weaviate/Pinecone)
                     │
                   PostgreSQL (Metadata)
                   OpenAI API (AI Responses)
                   Whisper (Speech-to-Text)
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Vector Database**: Weaviate (MVP) / Pinecone (Production)
- **AI Models**: OpenAI GPT, Whisper, Sentence Transformers
- **Frontend**: React, Material-UI
- **Database**: PostgreSQL
- **Video Processing**: MoviePy, OpenCV, FFmpeg

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (for Weaviate)
- PostgreSQL
- 8GB+ RAM

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/roshanm20/instant-tutor-ai.git
cd instant-tutor-ai
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit configuration
nano .env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Vector Database (Weaviate)
```bash
cd deployment
docker-compose up -d
```

### 5. Run the Application
```bash
# Option 1: Use the startup script (recommended)
python start.py

# Option 2: Direct backend start
python main.py

# Option 3: Manual start
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

### Ask a Question
```bash
POST /api/query
Content-Type: application/json
Authorization: Bearer demo-token-123

{
  "query": "What is the derivative of x squared?",
  "course_id": "MATH_101",
  "user_id": "student_123"
}
```

### Upload Course
```bash
POST /api/courses/upload
Content-Type: application/json
Authorization: Bearer demo-token-123

{
  "course_id": "MATH_101",
  "course_title": "Calculus Fundamentals",
  "video_urls": ["lectures/lecture1.mp4"],
  "instructor_name": "Dr. Smith",
  "language": "english",
  "difficulty": "intermediate"
}
```

## 🎯 Kerala Market Features

- **Malayalam Language Support**: Using IndicBART for local language processing
- **SCERT/CBSE Alignment**: Curriculum-specific knowledge graphs
- **Local EdTech Integration**: Compatible with existing Kerala education platforms
- **Cost-Effective Scaling**: Optimized for Indian market pricing

## 💰 Cost Estimation

### MVP Phase (Month 1-3)
- Infrastructure: ₹10,000-15,000/month
- AI API costs: ₹8,000-12,000/month
- **Total: ₹18,000-27,000/month**

### Scale Phase (Month 4-12)
- Infrastructure: ₹25,000-40,000/month
- AI API costs: ₹20,000-35,000/month
- **Total: ₹45,000-75,000/month**

## 📈 Success Metrics

- **Response Time**: < 2 seconds
- **Accuracy**: 85%+ content-specific accuracy
- **Uptime**: 95%+ availability
- **User Satisfaction**: 4.0+ rating
- **Cost Savings**: 30%+ reduction for institutions

## 🔧 Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
black .
flake8 .
```

### Docker Deployment
```bash
docker build -t kerala-ai-tutor .
docker run -p 8000:8000 kerala-ai-tutor
```

## 📚 Documentation

- [Implementation Guide](implementation_guide.md)
- [API Documentation](http://localhost:8000/docs)
- [Kerala Market Strategy](docs/kerala-strategy.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 Kerala Startup Mission (KSUM)

This project is designed to align with Kerala's startup ecosystem and can be submitted to KSUM for potential government support and funding opportunities.

## 📞 Contact

- **Project Lead**: [Your Name]
- **Email**: [your.email@example.com]
- **LinkedIn**: [Your LinkedIn Profile]
- **GitHub**: [Your GitHub Profile]

## 🙏 Acknowledgments

- Kerala Startup Mission (KSUM) for ecosystem support
- OpenAI for AI model access
- Weaviate team for vector database technology
- Kerala education community for feedback and testing

---

**Built with ❤️ for Kerala's Education Future**
