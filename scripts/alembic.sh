#!/bin/sh

## Repeat command until port 5431 on address db is not ready.
until
alembic revision --autogenerate -m "Initial"
alembic upgrade head
do
echo "Waiting for database connection for 5 seconds..."

## Wait for 5 seconds before check again.
sleep 5
done
echo "Database server ready..."