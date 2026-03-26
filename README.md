# AthleteIQ  

A full-stack athlete performance tracking application built with Vue 3 and node

## Links

- **Frontend:** [athlete-iq-peach.vercel.app](https://athlete-iq-peach.vercel.app/)
- **Backend:** [athleteiq-i8od.onrender.com/api](https://athleteiq-i8od.onrender.com/api)
- **Docs:** [athleteiq-i8od.onrender.com/api/docs](https://athleteiq-i8od.onrender.com/api/docs/)

## Tech Stack

**Client**
- Vue 3 + TypeScript + Vite
- Pinia (state management)
- Vue Router 4
- Tailwind CSS
- Axios

**Server**
- Node.js + Express + TypeScript
- MongoDB + Mongoose
- JWT authentication
- Joi validation
- Winston logging

## Getting Started

### Prerequisites
- Node.js 18+
- MongoDB running locally on port 27017

### Install

```bash
npm run install:all
```

### Development

```bash
npm run dev
```

Starts both client (`http://localhost:5173`) and server (`http://localhost:3000`) concurrently.

### Environment

Copy `server/.env.example` to `server/.env` and fill in the required values:

```
MONGODB_URI=mongodb://localhost:27017/athleteiq
JWT_SECRET=your_long_random_secret
```
