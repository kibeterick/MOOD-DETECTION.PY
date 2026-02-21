# 🔌 API Documentation

REST API endpoints for the Mood Detection System.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Home Page

**GET** `/`

Returns the main web interface.

**Response:**
- HTML page with camera feed and controls

---

### 2. Video Feed

**GET** `/video_feed`

Streams live video with emotion detection overlay.

**Response:**
- Content-Type: `multipart/x-mixed-replace; boundary=frame`
- Continuous JPEG frames with emotion annotations

**Features:**
- Real-time face detection
- Emotion overlay with confidence scores
- Emotion bars for top 3 emotions
- Bounding boxes around detected faces

---

### 3. Get Current Emotion

**GET** `/get_emotion`

Returns current emotion data in JSON format.

**Response:**
```json
{
  "emotion": "happy",
  "confidence": 0.85,
  "message": "Keep smiling, it makes others happy too!",
  "voice_text": "I'm feeling great today!",
  "voice_emotion": "happy",
  "is_listening": false,
  "timestamp": "2026-02-21T20:30:45.123456"
}
```

**Fields:**
- `emotion` (string): Detected emotion (happy, sad, angry, fear, surprise, neutral, disgust)
- `confidence` (float): Confidence score (0.0 - 1.0)
- `message` (string): Motivational message based on emotion
- `voice_text` (string): Transcribed speech text
- `voice_emotion` (string): Emotion detected from voice
- `is_listening` (boolean): Whether voice recognition is active
- `timestamp` (string): ISO format timestamp

**Update Frequency:**
- Frontend polls this endpoint every 1 second

---

### 4. Start Voice Recognition

**POST** `/start_listening`

Initiates voice recognition session.

**Request:**
- No body required

**Response:**
```json
{
  "status": "listening",
  "message": "Listening to your voice..."
}
```

**Behavior:**
- Activates microphone
- Listens for 5-10 seconds
- Processes speech in background thread
- Auto-stops after timeout
- Updates global voice emotion state

**Error Responses:**
```json
{
  "status": "error",
  "message": "No speech detected. Please try again."
}
```

```json
{
  "status": "error",
  "message": "Could not understand audio. Please speak clearly."
}
```

---

### 5. Stop Voice Recognition

**POST** `/stop_listening`

Manually stops voice recognition.

**Request:**
- No body required

**Response:**
```json
{
  "status": "stopped",
  "message": "Voice recognition stopped"
}
```

---

## Data Models

### Emotion Object

```python
{
  "happy": 0.85,      # Confidence for happy
  "sad": 0.05,        # Confidence for sad
  "angry": 0.02,      # Confidence for angry
  "fear": 0.01,       # Confidence for fear
  "surprise": 0.03,   # Confidence for surprise
  "neutral": 0.03,    # Confidence for neutral
  "disgust": 0.01     # Confidence for disgust
}
```

### Voice Analysis

**Keyword Matching:**
- Matches words against emotion database
- Keywords: angry, hate, sad, depressed, happy, joy, worried, anxious, etc.

**Sentiment Analysis:**
- Polarity > 0.3: Happy
- Polarity < -0.3: Sad
- Otherwise: Neutral

---

## Usage Examples

### JavaScript (Frontend)

```javascript
// Get current emotion
fetch('/get_emotion')
  .then(response => response.json())
  .then(data => {
    console.log('Emotion:', data.emotion);
    console.log('Confidence:', data.confidence);
  });

// Start voice recognition
fetch('/start_listening', { method: 'POST' })
  .then(response => response.json())
  .then(data => console.log(data.message));
```

### Python (Backend Integration)

```python
import requests

# Get emotion data
response = requests.get('http://localhost:5000/get_emotion')
data = response.json()
print(f"Emotion: {data['emotion']}")

# Start voice recognition
response = requests.post('http://localhost:5000/start_listening')
print(response.json())
```

### cURL

```bash
# Get emotion
curl http://localhost:5000/get_emotion

# Start voice recognition
curl -X POST http://localhost:5000/start_listening

# Stop voice recognition
curl -X POST http://localhost:5000/stop_listening
```

---

## Rate Limiting

Currently no rate limiting implemented. For production use, consider:
- Max 60 requests per minute per IP
- Max 10 concurrent voice recognition sessions

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK`: Success
- `400 Bad Request`: Invalid request
- `500 Internal Server Error`: Server error

---

## WebSocket Support (Future)

Planned for real-time bidirectional communication:
```javascript
const socket = io('http://localhost:5000');
socket.on('emotion_update', (data) => {
  console.log('Real-time emotion:', data);
});
```

---

## Security Considerations

### Current Implementation
- No authentication required
- Runs on localhost only
- Debug mode enabled

### Production Recommendations
- Add API key authentication
- Enable HTTPS/TLS
- Implement rate limiting
- Disable debug mode
- Add CORS headers for specific origins
- Validate all inputs
- Sanitize user data

---

## Performance

### Optimization Tips
- Camera resolution: 640x480 for best performance
- Frame rate: 30 FPS
- Emotion detection: ~100ms per frame
- Voice recognition: 2-5 seconds processing time

### Caching
- Emotion results cached for 1 second
- Voice results cached until new speech detected

---

## Integration Examples

### React Integration

```jsx
import { useState, useEffect } from 'react';

function MoodDetector() {
  const [emotion, setEmotion] = useState(null);
  
  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await fetch('/get_emotion');
      const data = await response.json();
      setEmotion(data);
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div>
      <h1>Current Emotion: {emotion?.emotion}</h1>
      <p>Confidence: {emotion?.confidence}</p>
    </div>
  );
}
```

### Mobile App Integration

```swift
// iOS Swift
func getEmotion() {
    let url = URL(string: "http://localhost:5000/get_emotion")!
    URLSession.shared.dataTask(with: url) { data, response, error in
        if let data = data {
            let emotion = try? JSONDecoder().decode(EmotionData.self, from: data)
            print("Emotion: \(emotion?.emotion ?? "unknown")")
        }
    }.resume()
}
```

---

## Support

For API questions or issues:
- Open an issue on [GitHub](https://github.com/kibeterick/MOOD-DETECTION.PY/issues)
- Check [README.md](README.md) for general documentation
- Review [INSTALLATION.md](INSTALLATION.md) for setup help
