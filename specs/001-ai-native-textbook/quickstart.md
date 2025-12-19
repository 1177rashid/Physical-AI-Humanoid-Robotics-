# Quickstart Guide: AI-Native Textbook on Physical AI & Humanoid Robotics

## Prerequisites

- Ubuntu 22.04 LTS (or equivalent environment)
- Python 3.11+
- Node.js 18+ and npm/yarn
- ROS 2 Humble Hawksbill or Iron Irwini
- Docker and Docker Compose
- Git

## Setup Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai_native_book
```

### 2. Set up Backend Services

#### Install Python Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Set up Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

#### Initialize Database
```bash
# For Neon Postgres
python -m src.utils.database_init

# For Qdrant vector store
# Make sure Qdrant is running (see docker-compose.yml)
```

### 3. Set up Frontend (Docusaurus)

#### Install Node Dependencies
```bash
cd docs
npm install
```

#### Run Development Server
```bash
npm run start
```

### 4. Run Backend API Server
```bash
cd backend
source venv/bin/activate
python main.py
```

## Project Structure Overview

```
ai_native_book/
├── docs/                 # Docusaurus textbook frontend
│   ├── docs/            # Textbook content (MDX files)
│   ├── src/             # Custom React components
│   ├── static/          # Static assets (images, examples)
│   └── docusaurus.config.js  # Docusaurus configuration
├── backend/             # FastAPI backend services
│   ├── src/
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   ├── api/         # API endpoints
│   │   └── utils/       # Utility functions
│   └── tests/           # Backend tests
└── specs/               # Specification files
    └── 001-ai-native-textbook/
```

## Running the Full Application

### 1. Start Infrastructure Services
```bash
# From project root
docker-compose up -d
```

### 2. Start Backend API
```bash
cd backend
source venv/bin/activate
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Docusaurus Frontend
```bash
cd docs
npm run start
```

The application will be available at `http://localhost:3000`

## Key Development Tasks

### Adding New Textbook Content
1. Create MDX files in `docs/docs/[category]/`
2. Update `docs/sidebars.js` to include the new content
3. Add any required learning resources to the database

### Adding a New Lab Exercise
1. Create the lab content in the appropriate textbook section
2. Add lab metadata to the database (or via admin interface)
3. Ensure all code samples are tested and functional

### Working with the RAG Chatbot
1. Index new content: `python -m src.services.rag_service index_new_content`
2. Test chat functionality via the frontend chat interface
3. Monitor vector store for performance optimization

## API Endpoints

### Textbook Content API
- `GET /api/v1/textbook/modules` - List all modules
- `GET /api/v1/textbook/modules/{id}` - Get specific module
- `GET /api/v1/textbook/modules/{id}/labs` - Get labs for a module

### Chatbot API
- `POST /api/v1/chat` - Send message to chatbot
- `POST /api/v1/chat/session` - Start new chat session
- `GET /api/v1/chat/session/{id}` - Get chat session history

### User Progress API
- `GET /api/v1/progress` - Get user progress
- `POST /api/v1/progress/{module_id}` - Update module progress
- `POST /api/v1/labs/submit` - Submit lab exercise

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd docs
npm run test
```

## Deployment

### GitHub Pages (Frontend Only)
```bash
cd docs
npm run build
# The built site is in the build/ directory and can be deployed to GitHub Pages
```

### Backend Deployment
The backend is designed for containerized deployment:
```bash
docker build -t ai-textbook-backend .
docker run -p 8000:8000 ai-textbook-backend
```

## Troubleshooting

### Common Issues
- **ROS 2 Integration**: Ensure ROS 2 environment is sourced before running ROS-dependent components
- **Vector Store**: Verify Qdrant is running and accessible when using RAG features
- **Database Connection**: Check environment variables and network connectivity to Neon Postgres

### Development Tips
- Use the Docusaurus hot-reload feature during content development
- Test ROS 2 examples in simulation before deployment
- Monitor API response times for performance optimization