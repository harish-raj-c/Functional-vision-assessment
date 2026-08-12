# Functional Vision Assessment

A production-ready Functional Vision Assessment system for companion robots that measures functional vision using real-world object detection and counting under progressively challenging visual conditions.

## Overview

This assessment is **NOT** intended to replace Visual Acuity or Contrast Sensitivity tests. Instead, it evaluates:
- Functional Vision
- Object Detection
- Visual Search
- Recognition Accuracy
- Processing Speed
- Selective Attention
- Peripheral Awareness

The assessment simulates everyday visual tasks using object counting instead of reading letters, making it more engaging and representative of real-world challenges.

## Tech Stack

### Frontend
- **Svelte 5** - Modern reactive UI framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling with healthcare-focused design system

### Backend
- **FastAPI** - High-performance Python web framework
- **Python 3.10+** - Backend logic
- **Pydantic** - Data validation and settings management

### Communication
- **REST API** - Frontend-backend communication
- **NATS** - Message queuing for vision data subscription

## Architecture

The application follows a modular, component-based architecture:

```
backend/
├── app/
│   ├── api/              # REST API endpoints
│   ├── assessment/       # Assessment controller
│   ├── calibration/      # Calibration manager
│   ├── models/           # Pydantic models
│   ├── nats/             # NATS subscriber
│   ├── results/          # Results engine (JSON/CSV/PDF)
│   ├── scene/            # Scene engine
│   ├── score/            # Score calculation engine
│   └── config.py         # Configuration
└── main.py               # Application entry point

frontend/
├── src/
│   ├── components/       # Svelte components
│   ├── lib/             # Utilities (API, stores, types)
│   ├── App.svelte       # Main application
│   └── app.css          # Global styles
└── package.json
```

## Features

### Assessment Flow
1. **Home** - Introduction and start button
2. **Instructions** - Clear guidance for users
3. **Calibration** - NATS-based position verification
4. **Practice** - One unscored practice round
5. **Assessment** - 5 levels with progressive difficulty
6. **Results** - Comprehensive score display and report downloads

### 5-Level Difficulty System

| Level | Purpose | Objects | Time | Challenges |
|-------|---------|---------|------|------------|
| 1 | Baseline Detection | 4-5 | Unlimited | Large, bright, plain background |
| 2 | Recognition | 6-8 | 10s | Medium size, multiple types, distractions |
| 3 | Visual Search | 10-12 | 8s | Natural scene, moderate clutter |
| 4 | Functional Vision | 12-15 | 6s | Similar colors, lower contrast, peripheral |
| 5 | Advanced | 15-18 | 5s | Small, cluttered, low contrast, overlap |

### Object Library
16 SVG objects: Balloon, Football, Basketball, Teddy Bear, Cup, Bottle, Apple, Book, Chair, Clock, Flower, Toy Car, Dog, Cat, Gift Box, Plant

### Input Methods
- **Primary**: Large on-screen number buttons
- **Secondary**: Voice recognition (Web Speech API)
- **Optional**: Keyboard input (0-9 keys)

### Accessibility
- Dark/Light mode toggle
- High contrast mode
- Large text option
- Screen-reader friendly
- Simple, clear language
- Healthcare-style UI with large typography

### Live Monitoring
Continuous NATS subscription monitors:
- Face detection status
- User distance (120-200cm range)
- Position centering
- Automatic pause/resume when user leaves frame

### Score Calculation
Metrics measured:
- Detection Accuracy
- Recognition Accuracy
- Response Time
- Miss Rate
- False Positives
- Average Time
- Level Completion

**Functional Vision Score (0-100)**: Weighted calculation:
- Accuracy: 60%
- Speed: 20%
- Level Completion: 20%

### Report Generation
- **JSON** - Machine-readable data
- **CSV** - Spreadsheet compatible
- **PDF** - Professional report with charts

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- NATS server running
- Vision camera system publishing to NATS topics

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Configure environment variables in `.env`:
```env
NATS_URL=nats://localhost:4222
MIN_DISTANCE_CM=120
MAX_DISTANCE_CM=200
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## NATS Integration

The application subscribes to these NATS topics:

- `vision.eye.cam0.face` - Face detection data
- `vision.eye.cam0.depth` - Distance estimation
- `vision.eye.cam0.blink` - Blink detection

Expected message format:
```json
{
  "detected": true,
  "bounding_box": [x, y, width, height],
  "confidence": 0.95,
  "distance_cm": 165,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## API Endpoints

### Vision
- `GET /api/v1/vision-state` - Current vision state
- `GET /api/v1/calibration-status` - Calibration status

### Assessment
- `POST /api/v1/assessment/start` - Start assessment
- `POST /api/v1/assessment/stop` - Stop assessment
- `GET /api/v1/assessment/next-scene` - Get next scene
- `POST /api/v1/assessment/submit-answer` - Submit answer
- `GET /api/v1/assessment/progress` - Get progress
- `GET /api/v1/assessment/results` - Get final results

### Reports
- `GET /api/v1/assessment/results/json` - Download JSON
- `GET /api/v1/assessment/results/csv` - Download CSV
- `GET /api/v1/assessment/results/pdf` - Download PDF

## Future Extensibility

The modular architecture allows easy addition of:
- Shape Recognition tests
- Color Vision tests
- Memory tests
- Peripheral Vision tests
- Motion Detection tests
- Contrast Challenge tests

Add new test types by:
1. Creating new scene generation logic in `scene_engine.py`
2. Adding new level configurations
3. Extending the score engine with new metrics

## Development

### Code Quality
- Strong TypeScript typing
- Modular backend with clear separation of concerns
- Reusable Svelte components
- Type-safe API communication
- Production-ready error handling

### Testing
Run backend tests:
```bash
cd backend
pytest
```

Run frontend type checking:
```bash
cd frontend
npm run check
```

## License

Proprietary - Companion Robot Vision Assessment System

## Support

For issues or questions, contact the development team.
