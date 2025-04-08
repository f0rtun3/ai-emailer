# ai-emailer
Pet project for an AI email processing and response script. This is based of an imaginary e-commerce store.
 - The assumption here is that there is already a database with an `email_response` table. If not, update your `.env` file to contain the `DATABASE_URL` and create the table as per the `db.sql` query. Tests will be added over time.

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

