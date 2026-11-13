# Verbo – AI-Powered Writing Assistant

**Write smarter. Transform better. Express freely.**

Verbo is an AI-powered writing platform that helps users generate, improve, and transform written content using Google Gemini AI.

From creating research articles and professional emails to simplifying text and improving grammar, Verbo makes everyday writing easier and more efficient.

##  Live Demo

- **Frontend:** https://verbo-nu.vercel.app
- **Backend:** https://verbo-backend-velk.onrender.com

##  Features

### 1. AI Content Generation

Generate different types of content based on your requirements:

- Research Article
- Literature Review
- Abstract
- Professional Email
- Resume Content
- LinkedIn Post
- Social Media Caption

### 2. AI Text Transformation

Transform existing text using different writing operations:

- Summarize
- Expand
- Simplify
- Rewrite
- Improve Grammar
- Make Professional
- Make Academic
- Convert to Bullet Points
- Change Tone

### 3. Customization Options

Customize your content with options such as:

- Writing length
- Tone of writing
- Target audience
- Complexity level
- Custom instructions

##  Tech Stack

| Technology | Purpose |
|---|---|
| React | Frontend development |
| Vite | Frontend build tool |
| Python | Backend programming |
| FastAPI | Backend API framework |
| Google Gemini AI | AI content generation and transformation |
| Google Gen AI SDK | Gemini API integration |
| Vercel | Frontend deployment |
| Render | Backend deployment |

##  How It Works

1. The user selects a content generation or text transformation option.
2. The user enters text and selects the required customization options.
3. The React frontend sends the request to the FastAPI backend.
4. The backend prepares the prompt and communicates with Google Gemini AI.
5. Gemini processes the request and generates the response.
6. The generated or transformed content is returned to the frontend and displayed to the user.

##  Project Structure

```text
verbo/
│
├── backend/
│   ├── config.py
│   ├── main.py
│   ├── prompt_builder.py
│   ├── requirements.txt
│   ├── test_gemini.py
│   └── test_prompt_builder.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
└── README.md
```

### Backend

Handles API requests, application configuration, prompt creation, and communication with Google Gemini AI.

### Frontend

Contains the React application, user interface, styling, and frontend configuration.

##  Installation and Setup

### Prerequisites

Make sure you have installed:

- Python
- Node.js and npm
- Git
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/hifzawaseem0525-cpu/verbo.git
cd verbo
```

### 2. Set Up the Backend

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend folder:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
GEMINI_MODEL=your_configured_gemini_model
```

Replace the placeholder values with your actual credentials and configured model.

**Important:** Never expose your API key or commit your `.env` file to GitHub.

### Start the Backend

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

###  Set Up the Frontend

Open another terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

##  API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks backend health |
| POST | `/generate` | Generates AI-powered content |
| POST | `/transform` | Transforms existing text |

##  Deployment

Verbo uses the following platforms for deployment:

| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| AI Service | Google Gemini API |

##  Project Objectives

- Make content creation easier with artificial intelligence.
- Generate different types of written content.
- Improve grammar, clarity, and readability.
- Transform existing text according to user requirements.
- Provide customizable writing options.
- Demonstrate the integration of AI services into a full-stack web application.

## Future Enhancements

- User authentication and personalized accounts.
- Save and manage previous writing sessions.
- Export generated content in different file formats.
- Support for additional languages.
- Additional AI-powered writing tools.

##  Developer

**Hifza Waseem**

GitHub: [hifzawaseem0525-cpu](https://github.com/hifzawaseem0525-cpu)

---

If you find Verbo useful, consider giving this repository a star!