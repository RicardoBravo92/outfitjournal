# Outfit Journal API

A FastAPI backend for managing users, clothing items, outfits, and statistics for your wardrobe.

## Features
- User registration and authentication (JWT)
- CRUD for clothing and outfits
- Outfit statistics (most used, unused, category summary, monthly frequency)
- Cloudinary integration for image storage
- CORS configuration via environment variables
- Modular service and route structure
- Global error handling

## Requirements
- Python 3.10+
- PostgreSQL (or your preferred SQL database)
- Cloudinary account (for image uploads)

## Setup
1. **Clone the repository:**
   ```bash
   git clone git@github.com:RicardoBravo92/outfitjournal.git
   cd outfitjournal/backend
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   Create a `.env` file in the backend directory with at least:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/outfitjournal
   SECRET_KEY=your_secret_key
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ALLOWED_ORIGINS=http://localhost:3000
   ```
5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation
Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Project Structure
```
app/
  api/           # API routes
  core/          # Config, database
  models/        # SQLAlchemy models
  schemas/       # Pydantic schemas
  services/      # Business logic
  utils/         # Utilities (error handlers, etc)
```

## Security
- CORS origins are set via the `ALLOWED_ORIGINS` variable in `.env`.
- JWT authentication for all protected endpoints.
- Rate limiting and CSRF protection can be added as needed.

## License
MIT

## Docker

You can run the API using Docker for easier deployment and environment consistency.

### Build the Docker image
```bash
docker build -t outfitjournal-backend .
```

### Run the container
```bash
docker run --env-file .env -p 8000:8000 outfitjournal-backend
```

- The API will be available at [http://localhost:8000](http://localhost:8000)
- Make sure your `.env` file is present in the backend directory and contains all required variables.


