# SQL inicial (Postgres)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  full_name VARCHAR(255),
  university VARCHAR(255),
  academic_level VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE theses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  title VARCHAR(255),
  topic VARCHAR(255),
  status VARCHAR(50),
  abstract TEXT,
  problem_statement TEXT,
  justification TEXT,
  research_questions TEXT,
  objectives TEXT,
  hypothesis TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chapters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thesis_id UUID REFERENCES theses(id),
  title VARCHAR(255),
  order_index INT,
  chapter_type VARCHAR(100),
  content TEXT,
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
