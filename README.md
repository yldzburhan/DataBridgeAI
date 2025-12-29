# DataBridge AI

**Enterprise-Grade ETL Platform with AI-Powered Data Quality Management**

DataBridge AI is a comprehensive Extract-Transform-Load (ETL) solution designed to address the challenges enterprises face when processing, validating, and integrating heterogeneous data sources. By combining deterministic data validation with AI-powered error correction, the platform significantly reduces manual data cleansing efforts while maintaining data integrity.

---

## The Problem

Organizations dealing with large-scale data ingestion face several recurring challenges:

- **Inconsistent Data Formats**: Data from different sources arrives in varying formats, requiring extensive manual normalization
- **Data Quality Issues**: Missing values, invalid formats, and inconsistent entries degrade downstream analytics
- **PII Compliance**: Sensitive personal information must be identified and protected before processing
- **Manual Review Bottlenecks**: Traditional ETL systems either reject bad data entirely or require extensive human intervention
- **Lack of Transparency**: Understanding why data failed validation and how to fix it remains opaque

## The Solution

DataBridge AI introduces an intelligent data pipeline that:

1. **Automates Schema Inference**: Uses GPT-4o-mini to analyze sample data and generate appropriate mapping specifications
2. **Applies Deterministic Validation**: Enforces type checking, format validation, and business rules consistently
3. **Provides AI-Powered Auto-Fix**: Automatically suggests corrections for common data quality issues
4. **Enables Human-in-the-Loop Review**: Presents failed records with clear explanations and suggested fixes for approval
5. **Tracks Costs Transparently**: Monitors actual AI API usage with real-time cost tracking

---

## Key Features

### Data Processing Pipeline
- Support for Excel (.xlsx, .xls) and CSV file uploads
- Asynchronous processing with real-time progress tracking
- Automatic schema detection and column mapping
- Configurable validation rules and transformations

### AI-Assisted Data Quality
- Intelligent mapping specification generation using OpenAI GPT-4o-mini
- Rule-based fixes for common issues (date formats, currency values, email normalization)
- AI-powered fixes for complex cases with confidence scoring
- Clear explanations for every suggested correction

### Privacy and Security
- PII detection using Microsoft Presidio with spaCy NLP models
- Data masking before LLM processing to protect sensitive information
- Read-only Text-to-SQL queries with schema restrictions
- Query result limits and SQL injection prevention

### Review Workflow
- Three-column comparison view: Original, AI Suggested, Manual Edit
- Error highlighting with detailed validation messages
- Individual and bulk approval capabilities
- Audit trail for approved records

### Analytics and Monitoring
- Executive dashboard with processing statistics
- Data quality metrics and quarantine rates
- Real-time AI cost tracking based on actual token usage
- Geographic distribution and data visualization

### Data Export
- Multiple export formats: CSV, Excel, JSON
- Filtered exports by file or date range
- Production and quarantine data export options

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DataBridge AI                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │   Frontend   │    │   Backend    │    │       Worker         │  │
│  │  (Streamlit) │◄──►│  (FastAPI)   │◄──►│      (Celery)        │  │
│  │   Port 8501  │    │   Port 8000  │    │                      │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                              │                      │               │
│                              ▼                      ▼               │
│                      ┌──────────────┐       ┌──────────────┐       │
│                      │  PostgreSQL  │       │    Redis     │       │
│                      │   Port 5432  │       │  Port 6379   │       │
│                      └──────────────┘       └──────────────┘       │
│                                                                      │
│  External Services:                                                  │
│  - OpenAI API (GPT-4o-mini for mapping and auto-fix)                │
│  - Microsoft Presidio (PII detection)                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Streamlit | Interactive web interface |
| Backend API | FastAPI | RESTful API endpoints |
| Task Queue | Celery + Redis | Asynchronous job processing |
| Database | PostgreSQL | Data persistence with JSONB storage |
| AI/ML | OpenAI GPT-4o-mini | Schema inference and auto-fix |
| NLP | spaCy + Presidio | PII detection and masking |
| Data Processing | Pandas | DataFrame operations |

---

## Installation

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Minimum 4GB RAM recommended

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/DataBridgeAI.git
   cd DataBridgeAI
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. **Create required directories**
   ```bash
   mkdir -p data/uploads
   ```

4. **Start all services**
   ```bash
   docker-compose up --build -d
   ```

5. **Verify deployment**
   ```bash
   # Check service status
   docker-compose ps
   
   # Verify API health
   curl http://localhost:8000/health
   ```

6. **Access the application**
   - Web Interface: http://localhost:8501
   - API Documentation: http://localhost:8000/docs
   - API Endpoints: http://localhost:8000

### Windows Users

Convenience scripts are provided for Windows:
```batch
# Start all services
start.bat

# Stop all services
stop.bat
```

---

## Usage Guide

### Uploading Data

1. Navigate to the **Upload** tab in the web interface
2. Select an Excel or CSV file using the file picker
3. Click **Upload & Process** to initiate the ETL pipeline
4. Monitor progress in the **Status** tab using the provided task ID

### Reviewing Quarantined Data

1. Open the **Review** tab
2. Enter the file ID or leave blank to view all quarantined records
3. Click **Load Quarantine Rows** to retrieve failed records
4. For each record, review:
   - Original (Raw): The unmodified source data
   - AI Suggested Fix: Automatically generated corrections
   - Manual Edit: Override with custom values if needed
5. Approve individual records or use bulk approval for multiple selections

### Querying Data

The **Chat** tab provides natural language querying capabilities:
- Ask questions in plain English about your processed data
- The system generates safe, read-only SQL queries
- Results are displayed in tabular format with optional visualizations

### Exporting Data

Use the **Export** tab to download processed data:
- Select export format (CSV, Excel, or JSON)
- Choose data source (Production or Quarantine)
- Filter by file ID if needed
- Download the generated file

---

## API Reference

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload file and initiate ETL processing |
| `GET` | `/status/{task_id}` | Retrieve task progress and status |
| `GET` | `/review` | List quarantined rows with AI suggestions |
| `POST` | `/review/approve` | Approve quarantine rows for production |
| `POST` | `/chat` | Execute natural language queries |
| `GET` | `/dashboard/stats` | Retrieve processing statistics |
| `POST` | `/dashboard/reset` | Reset database (development only) |
| `GET` | `/export/{format}` | Export data in specified format |
| `GET` | `/health` | Service health check |

### Request/Response Examples

**Upload File**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@data.xlsx"
```

**Check Status**
```bash
curl http://localhost:8000/status/{task_id}
```

**Approve Records**
```bash
curl -X POST http://localhost:8000/review/approve \
  -H "Content-Type: application/json" \
  -d '{"row_ids": [1, 2, 3]}'
```

---

## Database Schema

### Tables

**raw_files**
- Stores file metadata and processing status
- Tracks upload timestamps and SHA256 checksums for deduplication

**production_rows**
- Contains validated and approved data records
- Uses JSONB for flexible schema storage
- Includes confidence scores from AI mapping

**quarantine_rows**
- Holds records that failed validation
- Stores original data, AI-suggested fixes, and error details
- Tracks fix confidence and approval status

**llm_cost_tracking**
- Records actual token usage for each AI operation
- Enables accurate cost monitoring and budgeting

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API authentication key | Required |
| `OPENAI_MODEL` | Model to use for AI operations | `gpt-4o-mini` |
| `DATABASE_URL` | PostgreSQL connection string | Set in docker-compose |
| `REDIS_URL` | Redis connection string | Set in docker-compose |

### Customization

**Adding Custom Validators**

Edit `backend/app/core/transform.py` to add new validation rules:
```python
def validate_and_convert(value: Any, data_type: DataType) -> Any:
    # Add custom validation logic here
    pass
```

**Modifying AI Prompts**

Edit `backend/app/core/llm_engine.py` to customize:
- Schema inference prompts
- SQL generation prompts

Edit `backend/app/core/auto_fix.py` to customize:
- Auto-fix prompt templates
- Rule-based fix patterns

---

## Project Structure

```
DataBridgeAI/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── worker.py            # Celery task definitions
│   │   ├── config.py            # Application settings
│   │   ├── core/
│   │   │   ├── llm_engine.py    # OpenAI integration
│   │   │   ├── auto_fix.py      # AI-powered data correction
│   │   │   ├── pii.py           # PII detection and masking
│   │   │   └── transform.py     # Data validation and transformation
│   │   ├── db/
│   │   │   ├── models.py        # SQLAlchemy models
│   │   │   ├── engine.py        # Database connection
│   │   │   └── session.py       # Session management
│   │   ├── routers/
│   │   │   ├── upload.py        # File upload endpoints
│   │   │   ├── status.py        # Task status endpoints
│   │   │   ├── review.py        # Quarantine review endpoints
│   │   │   ├── chat.py          # Text-to-SQL endpoints
│   │   │   ├── dashboard.py     # Statistics endpoints
│   │   │   └── export.py        # Data export endpoints
│   │   └── schemas/
│   │       ├── base.py          # Request/Response models
│   │       └── mapping.py       # Mapping specification models
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit application
│   ├── api_client.py            # Backend API wrapper
│   ├── Dockerfile
│   └── requirements.txt
├── data/
│   └── uploads/                 # Shared volume for uploaded files
├── docker-compose.yml
├── start.bat                    # Windows start script
├── stop.bat                     # Windows stop script
├── .env.example                 # Environment template
└── README.md
```

---

## Troubleshooting

### Common Issues

**Services fail to start**
- Ensure Docker daemon is running
- Verify port availability (5432, 6379, 8000, 8501)
- Check available disk space and memory

**File upload fails**
- Verify the `data/uploads` directory exists and is writable
- Check file size limits in your environment
- Ensure the file format is supported (xlsx, xls, csv)

**Worker tasks remain pending**
- Verify Redis connectivity: `docker-compose logs redis`
- Check worker logs: `docker-compose logs worker`
- Ensure OpenAI API key is valid

**High AI costs reported**
- The system now tracks actual token usage from OpenAI API
- Review the cost breakdown in the Dashboard tab
- Consider reducing batch sizes for large files

**PII detection errors**
- Verify spaCy model is installed: check worker startup logs
- The model download occurs during container build

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f worker
docker-compose logs -f frontend
```

### Database Access

```bash
docker exec -it databridge_postgres psql -U databridge_user -d databridge
```

---

## Security Considerations

- **API Key Protection**: Store OpenAI API keys in environment variables, never in code
- **PII Handling**: All data is masked before being sent to external AI services
- **SQL Injection Prevention**: Text-to-SQL queries are restricted to SELECT operations on specific tables
- **Query Limits**: Result sets are limited to prevent resource exhaustion
- **Network Isolation**: Services communicate through an internal Docker network

---

## Performance Notes

- Processing speed depends on the number of quarantined rows requiring AI fixes
- Rule-based fixes are applied first to minimize AI API calls
- Batch commits occur every 10 rows to balance performance and reliability
- Consider disabling AI auto-fix for very large files to reduce processing time

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome. Please ensure:
- Code follows existing patterns and style
- New features include appropriate tests
- Documentation is updated accordingly

For major changes, please open an issue first to discuss the proposed modifications.
