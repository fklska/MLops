SELECT 'CREATE DATABASE worker' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'worker')\gexec