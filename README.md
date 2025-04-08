# ai-emailer
Pet project for an AI email processing and response. This is based of an imaginary e-commerce store business.


## Scope
Building an AI system that can:
- Ingest customer emails
- Categorize them (support, feedback, complaint, inquiry, etc.)
- Extract relevant info (order number, issue, product, etc.)
- Generate human-like responses
- Store conversation metadata (in a DB)

## Architecture design
- Backend API - Python FastAPI
- AI Model - OpenAI
- Database PostgreSQL
- Email Integration (IMAP)
- Queue - SQS

## Architecture
 ![ai mailer architecture diagram](/architecture/mailer-architecture.png)

