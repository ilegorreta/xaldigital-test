CREATE TABLE IF NOT EXISTS employee(
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    company_name VARCHAR(64) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(64) NOT NULL,
    state VARCHAR(64) NOT NULL,
    zip VARCHAR(64) NOT NULL,
    phone1 VARCHAR(10) NOT NULL,
    phone2 VARCHAR(10),
    email VARCHAR(64) NOT NULL,
    department VARCHAR(64) NOT NULL
);
