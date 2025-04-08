CREATE TABLE IF NOT EXISTS email_responses (
    id SERIAL PRIMARY KEY,
    sender TEXT,
    subject TEXT,
    body TEXT,
    category TEXT,
    issue_summary TEXT,
    suggested_response TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);