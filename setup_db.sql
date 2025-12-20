-- Create robo_trade database and user
CREATE DATABASE robo_trade ENCODING 'UTF8';

-- Create user
CREATE USER robo_user WITH ENCRYPTED PASSWORD 'robo_trade_2025';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE robo_trade TO robo_user;

-- Connect to the database and create schema
\c robo_trade;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO robo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO robo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO robo_user;
