# Validate DataBridge AI Setup
# Run: python validate_setup.py

import os
import sys

def check_file(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND: {path}")
        return False

def main():
    print("=" * 60)
    print("DataBridge AI - Setup Validation")
    print("=" * 60)
    print()
    
    errors = []
    
    # Check root files
    print("Checking root files...")
    if not check_file("docker-compose.yml", "Docker Compose configuration"):
        errors.append("docker-compose.yml")
    if not check_file(".env.example", "Environment template"):
        errors.append(".env.example")
    if not check_file("README.md", "README documentation"):
        errors.append("README.md")
    if not check_file("QUICKSTART.md", "Quick Start guide"):
        errors.append("QUICKSTART.md")
    print()
    
    # Check backend
    print("Checking backend...")
    backend_files = [
        ("backend/Dockerfile", "Backend Dockerfile"),
        ("backend/requirements.txt", "Backend requirements"),
        ("backend/init_db.py", "Database initialization script"),
        ("backend/app/main.py", "FastAPI main application"),
        ("backend/app/worker.py", "Celery worker"),
        ("backend/app/config.py", "Configuration"),
        ("backend/app/db/models.py", "Database models"),
        ("backend/app/db/engine.py", "Database engine"),
        ("backend/app/db/session.py", "Database session"),
        ("backend/app/core/llm_engine.py", "LLM engine"),
        ("backend/app/core/pii.py", "PII masking"),
        ("backend/app/core/transform.py", "Data transformation"),
        ("backend/app/schemas/mapping.py", "Mapping schemas"),
        ("backend/app/routers/upload.py", "Upload router"),
        ("backend/app/routers/status.py", "Status router"),
        ("backend/app/routers/review.py", "Review router"),
        ("backend/app/routers/chat.py", "Chat router"),
    ]
    
    for file, desc in backend_files:
        if not check_file(file, desc):
            errors.append(file)
    print()
    
    # Check frontend
    print("Checking frontend...")
    frontend_files = [
        ("frontend/Dockerfile", "Frontend Dockerfile"),
        ("frontend/requirements.txt", "Frontend requirements"),
        ("frontend/app.py", "Streamlit application"),
        ("frontend/api_client.py", "API client"),
    ]
    
    for file, desc in frontend_files:
        if not check_file(file, desc):
            errors.append(file)
    print()
    
    # Check directories
    print("Checking directories...")
    if not os.path.exists("data/uploads"):
        print("✗ Upload directory - NOT FOUND")
        errors.append("data/uploads")
    else:
        print("✓ Upload directory")
    print()
    
    # Summary
    print("=" * 60)
    if errors:
        print(f"✗ VALIDATION FAILED - {len(errors)} issues found:")
        for error in errors:
            print(f"  - {error}")
        print()
        print("Please ensure all required files are present.")
        return 1
    else:
        print("✓ ALL CHECKS PASSED!")
        print()
        print("Next steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OPENAI_API_KEY to .env")
        print("3. Run: docker-compose up --build")
        print("4. Run: docker-compose exec backend python init_db.py")
        print("5. Open: http://localhost:8501")
        print()
        print("See QUICKSTART.md for detailed instructions.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
