# Questionnaire Validation Errors - Quick Reference

## Original Error Message
When users tried to submit the questionnaire, they received:
```
"participation_years" must be one of [Less than 1 year, 1-2 years, 3-5 years, More than 5 years], 
"motivation" must be one of [Competition and performance, Health and fitness, Helping or coaching others, Academic or career opportunity, Fame, media, or recognition], 
"career_importance" must be one of [Not important, Slightly important, Moderately important, Very important, My main career focus], 
"work_environment" must be one of [On-field / practical, Office / management, Laboratory / science / clinical, Media / creative, A mix of environments], 
Education/training level is required, 
"biggest_challenge" must be one of [Academic workload, Time management, Financial constraints, Injury risk or health, Lack of facilities or coaching, Motivation], 
"injury_history" must be one of [None, Minor (short recovery), Moderate (missed competitions), Severe (long-term impact)]
```

## Why This Happened

### Root Cause 1: Navigation Bypass
Edit buttons on the Review page (`currentStep = X`) allowed users to jump steps without validation.

**Example Flow:**
1. User fills Step 1 properly ✓
2. User fills Step 2 properly ✓
3. User starts Step 3 but clicks Edit button to go back
4. Edit button uses `currentStep = 3` (no validation)
5. User clicks Back multiple times
6. User clicks Edit on Step 2
7. User returns to Step 5 (Review) by clicking forward
8. Step 3 and 4 fields were never properly filled → empty/invalid values

### Root Cause 2: Incomplete Check
Frontend validation only checked `if (!form.field)` but didn't verify:
- Is the value a valid enum option?
- Is the array length within bounds?
- Does the string match exactly (including capitalization)?

### Root Cause 3: Backend Received Invalid Data
Even with client-side validation passed, if fields were undefined or mismatched, backend Joi validator would reject them with all the enum options listed.

## Solution Implemented

### 1. New Navigation Function
```typescript
function goToStep(step: number) {
  if (step < currentStep.value) {
    // Always allow going backwards
    currentStep.value = step
  } else if (step > currentStep.value) {
    // Going forward requires validation
    if (validateStep(currentStep.value)) {
      currentStep.value = step
    }
  }
}
```

### 2. Enhanced Validation
```typescript
if (step === 4) {
  if (!form.biggest_challenge) 
    errors.biggest_challenge = 'Please select your biggest challenge'
  else if (!biggestChallenges.some((c: any) => c.value === form.biggest_challenge)) 
    errors.biggest_challenge = 'Invalid biggest challenge selection'
  
  // Similar for other fields...
}
```

### 3. Updated All Navigation
- Edit buttons: `@click="goToStep(1)"` instead of `@click="currentStep = 1"`
- Back button: `@click="goToStep(currentStep - 1)"` instead of `@click="currentStep--"`
- Continue button: Calls `nextStep()` which calls `validateStep()`

### 4. Pre-Submission Validation
```typescript
if (step === 5) {
  // Validate all steps before final submission
  for (let s = 1; s <= 4; s++) {
    if (!validateStep(s)) return false
  }
}
```

## Validation Error Types & Solutions

### Error: Field is empty
**Error Message:** `"biggest_challenge" is required`
**Solution:** Select a value for that field. The field will show error message in red until filled.

### Error: Invalid enum value
**Error Message:** `"injury_history" must be one of [None, Minor (short recovery), ...]`
**Cause:** Field value doesn't match allowed options exactly
**Solution:** Use the provided dropdown/buttons. Don't manually type incorrect values.

### Error: Invalid array count
**Error Message:** `"career_interests" must contain 1-3 items`
**Cause:** User selected 0 or 4+ career interests
**Solution:** Step 4 enforces max 3 selections with a progress bar. Add/remove as needed.

### Error: Type mismatch
**Error Message:** `"fitness_level" must be a number`
**Cause:** Backend received string instead of number
**Solution:** Rate fields are sliders returning integers 1-5. Never manually edit or leave as default (3).

## Frontend Validation Improvements

### Step 1: Athletic Background
- [x] primary_sport: required, non-empty string
- [x] academic_level: required, must be one of 5 options
- [x] participation_years: required, must be one of 4 exact values
- [x] participation_level: required, must be one of 5 options

### Step 2: Skills & Abilities
- ✓ All fields have defaults (3)
- ✓ No validation needed (1-5 enforced by UI)

### Step 3: Career Aspirations
- [x] motivation: required, must be one of 5 options
- [x] career_importance: required, must be one of 5 options
- [x] work_environment: required, must be one of 5 options

### Step 4: Context & Interests
- [x] biggest_challenge: required, must be one of 6 options
- [x] injury_history: required, must be one of 4 options
- [x] career_interests: required, array length 1-3
- [x] education_training_level: required, must be one of 5 options

### Step 5: Review & Submit
- [x] All step validations re-run before submission
- [x] Prevents incomplete submissions to backend

## Testing Scenarios

### Scenario 1: Complete Form Submission
```
Step 1: Fill all 4 fields → Continue ✓
Step 2: Use sliders (defaults OK) → Continue ✓
Step 3: Select 3 options → Continue ✓
Step 4: Select all required fields (1-3 interests) → Continue ✓
Step 5: Review shows all data → Submit ✓
Result: Submitted successfully
```

### Scenario 2: Bypass Attempt via Edit Button
```
Step 1: Fill all → Continue ✓
Step 2: Click Continue ✓
Step 3: Click Edit for Step 1 → Go back ✓
Step 1: Try to go to Step 5 directly via Edit → Blocked ✗
Result: Must re-validate each step forward
```

### Scenario 3: Incomplete Step 4
```
Step 1-3: Complete properly ✓
Step 4: Select only 2 fields out of 4 (skip education) → Click Continue ✗
Error: "education_training_level" is required (shown in red)
Result: Cannot proceed, must fix field
```

### Scenario 4: Invalid Selection
```
Step 4: Manually corrupt data (unlikely but tested) → Submit ✗
Backend Joi validates → Rejects with full enum list
Frontend shows generic error (backend error message displayed)
Result: User sees which fields failed, can retry
```

## Enum Value Checklist

When filling the form, ensure these exact values:

**participation_years:** (use hyphens)
- [ ] Less than 1 year
- [ ] 1-2 years
- [ ] 3-5 years
- [ ] More than 5 years

**motivation:** (full exact text)
- [ ] Competition and performance
- [ ] Health and fitness
- [ ] Helping or coaching others
- [ ] Academic or career opportunity
- [ ] Fame, media, or recognition

**career_importance:**
- [ ] Not important
- [ ] Slightly important
- [ ] Moderately important
- [ ] Very important
- [ ] My main career focus

**work_environment:** (with "")
- [ ] On-field / practical
- [ ] Office / management
- [ ] Laboratory / science / clinical
- [ ] Media / creative
- [ ] A mix of environments

**biggest_challenge:**
- [ ] Academic workload
- [ ] Time management
- [ ] Financial constraints
- [ ] Injury risk or health
- [ ] Lack of facilities or coaching
- [ ] Motivation

**injury_history:**
- [ ] None
- [ ] Minor (short recovery)
- [ ] Moderate (missed competitions)
- [ ] Severe (long-term impact)

**education_training_level:**
- [ ] Short courses or certifications only
- [ ] Diploma
- [ ] Bachelor's degree or add-on program  (note: "add-on")
- [ ] Master's degree
- [ ] Medical/clinical or doctoral pathway

## Files Changed
- `client/src/pages/QuestionnairePage.vue`:
  - Enhanced `validateStep()` function
  - Added `goToStep()` function
  - Updated all navigation buttons
  - Added enum validation checks

**Result:** ✅ Validation errors prevented at frontend, users get immediate feedback
             ✅ Backend Joi validator still protects for safety
             ✅ Better UX with clear error messages and guided correction
