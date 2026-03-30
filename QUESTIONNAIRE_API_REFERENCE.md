# Questionnaire API Reference & Testing Guide

## Endpoints

### 1. Submit Questionnaire Response
Submit a completed questionnaire and get ML-generated recommendations.

**Endpoint:** `POST /api/questionnaire/submit`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "academic_level": "Year 3",
  "primary_sport": "Football (Soccer)",
  "participation_years": "3-5 years",
  "participation_level": "University/School team",
  "fitness_level": 4,
  "technical_skill": 3,
  "leadership": 4,
  "data_comfort": 2,
  "motivation": "Competition and performance",
  "career_importance": "Very important",
  "work_environment": "On-field / practical",
  "biggest_challenge": "Time management",
  "injury_history": "Minor (short recovery)",
  "career_interests": ["Professional athlete", "Coach / Coaching education", "Sports science / Performance science"],
  "education_training_level": "Master's degree"
}
```

**Success Response:** `201 Created`
```json
{
  "message": "Questionnaire submitted and recommendations generated",
  "data": {
    "questionnaireResponse": {
      "_id": "507f1f77bcf86cd799439011",
      "user": "507f1f77bcf86cd799439010",
      "academic_level": "Year 3",
      "primary_sport": "Football (Soccer)",
      // ... all submitted fields
      "submittedAt": "2026-03-30T14:22:00Z",
      "createdAt": "2026-03-30T14:22:00Z",
      "updatedAt": "2026-03-30T14:22:00Z"
    },
    "recommendation": {
      // ML-generated career pathway recommendations
      "topPathways": [...],
      "matchScore": 0.87,
      "reasoning": "..."
    }
  }
}
```

**Error Response:** `400 Bad Request` (Validation failure)
```json
{
  "message": "Validation failed",
  "errors": {
    "academic_level": "Invalid value",
    "fitness_level": "Must be between 1 and 5"
  }
}
```

---

### 2. Get Questionnaire History
Retrieve all past questionnaire responses for the authenticated user.

**Endpoint:** `GET /api/questionnaire/history`

**Authentication:** Required (Bearer token)

**Query Parameters:** None

**Success Response:** `200 OK`
```json
{
  "message": "Questionnaire history retrieved",
  "data": {
    "responses": [
      {
        "_id": "507f1f77bcf86cd799439011",
        "user": "507f1f77bcf86cd799439010",
        "academic_level": "Year 3",
        // ... questionnaire response 1
        "submittedAt": "2026-03-30T14:22:00Z"
      },
      {
        "_id": "507f1f77bcf86cd799439012",
        "user": "507f1f77bcf86cd799439010",
        "academic_level": "Year 2",
        // ... questionnaire response 2
        "submittedAt": "2026-03-20T10:15:00Z"
      }
    ]
  }
}
```

**Empty History Response:** `200 OK`
```json
{
  "message": "Questionnaire history retrieved",
  "data": {
    "responses": []
  }
}
```

---

## Testing with cURL / Postman

### Test Submit Endpoint

```bash
curl -X POST http://localhost:3000/api/questionnaire/submit \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "academic_level": "Year 1",
    "primary_sport": "Basketball",
    "participation_years": "Less than 1 year",
    "participation_level": "Recreational",
    "fitness_level": 2,
    "technical_skill": 2,
    "leadership": 3,
    "data_comfort": 4,
    "motivation": "Health and fitness",
    "career_importance": "Slightly important",
    "work_environment": "A mix of environments",
    "biggest_challenge": "Academic workload",
    "injury_history": "None",
    "career_interests": ["Community sports development", "Sports media / Journalism / Content creation"],
    "education_training_level": "Short courses or certifications only"
  }'
```

### Test Get History Endpoint

```bash
curl -X GET http://localhost:3000/api/questionnaire/history \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Test with Custom Sport

```bash
curl -X POST http://localhost:3000/api/questionnaire/submit \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "academic_level": "Year 2",
    "primary_sport": "Rock Climbing",
    "participation_years": "1-2 years",
    "participation_level": "Club or academy",
    "fitness_level": 5,
    "technical_skill": 4,
    "leadership": 3,
    "data_comfort": 3,
    "motivation": "Competition and performance",
    "career_importance": "Moderately important",
    "work_environment": "On-field / practical",
    "biggest_challenge": "Financial constraints",
    "injury_history": "Moderate (missed competitions)",
    "career_interests": ["Professional athlete", "Coach / Coaching education", "Sports science / Performance science"],
    "education_training_level": "Bachelor'"'"'s degree or add-on program"
  }'
```

---

## Validation Rules

### Required Fields
- All 15 fields must be provided
- No optional fields

### Enum Validation

**academic_level:**
- Must be one of: `Year 1`, `Year 2`, `Year 3`, `Year 4`, `Postgraduate`

**participation_years:**
- Must be one of: `Less than 1 year`, `1-2 years`, `3-5 years`, `More than 5 years`

**participation_level:**
- Must be one of: `Not active`, `Recreational`, `University/School team`, `Club or academy`, `Elite/competitive pathway`

**motivation:**
- Must be one of: `Competition and performance`, `Health and fitness`, `Helping or coaching others`, `Academic or career opportunity`, `Fame, media, or recognition`

**career_importance:**
- Must be one of: `Not important`, `Slightly important`, `Moderately important`, `Very important`, `My main career focus`

**work_environment:**
- Must be one of: `On-field / practical`, `Office / management`, `Laboratory / science / clinical`, `Media / creative`, `A mix of environments`

**biggest_challenge:**
- Must be one of: `Academic workload`, `Time management`, `Financial constraints`, `Injury risk or health`, `Lack of facilities or coaching`, `Motivation`

**injury_history:**
- Must be one of: `None`, `Minor (short recovery)`, `Moderate (missed competitions)`, `Severe (long-term impact)`

**education_training_level:**
- Must be one of: `Short courses or certifications only`, `Diploma`, `Bachelor's degree or add-on program`, `Master's degree`, `Medical/clinical or doctoral pathway`

### Range Validation

**fitness_level, technical_skill, leadership, data_comfort:**
- Type: integer
- Min: 1, Max: 5
- No decimals

**career_interests:**
- Type: array of strings
- Min items: 1
- Max items: 3
- Valid options:
  - `Professional athlete`
  - `Coach / Coaching education`
  - `Strength & conditioning / Fitness coach`
  - `Sports science / Performance science`
  - `Sports physiotherapy / Rehabilitation`
  - `Sports analytics / Performance analysis`
  - `Sports management / Administration`
  - `Sports media / Journalism / Content creation`
  - `Officiating / Refereeing`
  - `Community sports development`

### No Validation Applied

**primary_sport:**
- Any non-empty string is accepted
- Supports custom sports (e.g., "Rock Climbing", "Surfing")
- No enum restriction

---

## Common Error Scenarios

### Missing Required Field
**Status:** 400 Bad Request
```json
{
  "message": "Validation failed",
  "errors": {
    "fitness_level": "fitness_level is required"
  }
}
```

### Invalid Enum Value
**Status:** 400 Bad Request
```json
{
  "message": "Validation failed",
  "errors": {
    "academic_level": "academic_level must be one of: Year 1, Year 2, Year 3, Year 4, Postgraduate"
  }
}
```

### Out of Range Rating
**Status:** 400 Bad Request
```json
{
  "message": "Validation failed",
  "errors": {
    "technical_skill": "technical_skill must be between 1 and 5"
  }
}
```

### Invalid Career Interests Count
**Status:** 400 Bad Request
```json
{
  "message": "Validation failed",
  "errors": {
    "career_interests": "Select between 1 and 3 career interests"
  }
}
```

### No Authentication
**Status:** 401 Unauthorized
```json
{
  "message": "Unauthorized - authentication required",
  "error": "No bearer token provided"
}
```

### Invalid Token
**Status:** 401 Unauthorized
```json
{
  "message": "Unauthorized",
  "error": "Invalid or expired token"
}
```

---

## Data Access Patterns

### Get Specific User's Latest Response
```bash
GET /api/questionnaire/history
# Returns sorted by createdAt descending, grab first item
```

### Query Custom Sports in Database
```javascript
// MongoDB shell
db.questionnaireresponses.find({
  "primary_sport": { $nin: ["Football (Soccer)", "Basketball", "Athletics / Track & Field", "Volleyball", "Rugby"] }
})
```

### Aggregate Injury Statistics
```javascript
db.questionnaireresponses.aggregate([
  {
    $group: {
      _id: "$injury_history",
      count: { $sum: 1 },
      percentage: { $avg: 100 }
    }
  }
])
```

---

## Database Schema

**Collection:** `questionnaireresponses`

**Indexes:**
- `{ user: 1, createdAt: -1 }` - For history retrieval and sorting

**Fields:**
- `user` - ObjectId reference to User
- `academic_level` - String (enum)
- `primary_sport` - String (no enum)
- `participation_years` - String (enum)
- `participation_level` - String (enum)
- `fitness_level` - Number (1-5)
- `technical_skill` - Number (1-5)
- `leadership` - Number (1-5)
- `data_comfort` - Number (1-5)
- `motivation` - String (enum)
- `career_importance` - String (enum)
- `work_environment` - String (enum)
- `biggest_challenge` - String (enum)
- `injury_history` - String (enum)
- `career_interests` - Array of Strings (1-3)
- `education_training_level` - String (enum)
- `submittedAt` - Date (default: now)
- `createdAt` - Date (Mongoose auto)
- `updatedAt` - Date (Mongoose auto)

---

## Integration Notes

### ML Recommendation Trigger
- Automatically called in `questionnaireService.submit()`
- Uses `careerService.predict(userId, responseId, payload)`
- Process is synchronous within submit transaction

### Google Sheets Export
- Also triggered in `questionnaireService.submit()`
- Non-blocking (errors don't affect submission response)
- Uses `googleSheetsService.exportSubmission()`
- Requires env vars: `GOOGLE_SHEETS_SPREADSHEET_ID`, `GOOGLE_SHEETS_CREDENTIALS_*`

### User History Access
- Paginated via MongoDB sort + lean() for performance
- Limited to authenticated user via `req.user._id`
- Returns empty array if no submissions yet

---

## Performance Considerations

✅ **Optimized Queries:**
- History lookup uses index `{ user: 1, createdAt: -1 }`
- `.lean()` removes Mongoose document overhead

✅ **Non-blocking Export:**
- Google Sheets export runs asynchronously
- Doesn't block submit response

⚠️ **ML Computation:**
- Prediction runs synchronously during submit
- May add 100-500ms depending on complexity
- Consider making async if performance degrades

---

## Version History

**v1.0** (March 30, 2026)
- Initial implementation with all 15 questions
- 5-step frontend wizard
- ML recommendation integration
- Google Sheets export
- User history tracking
