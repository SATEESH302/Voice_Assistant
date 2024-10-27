--step1
CREATE SCHEMA IF NOT EXISTS interview_assist;

--step2
CREATE TABLE interview_assist.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

--step3
INSERT INTO interview_assist.users (email) VALUES ('yvasu143@gmail.com');
