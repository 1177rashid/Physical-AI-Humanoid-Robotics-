-- This file is used to initialize the PostgreSQL database
-- It will be executed when the PostgreSQL container starts for the first time

-- Create any initial tables or data here if needed
-- For now, we'll just create the extension for UUID generation which is often needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Additional initialization can be added here as needed