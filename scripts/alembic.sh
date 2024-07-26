#!/bin/sh

alembic revision --autogenerate -m "Initial"
alembic upgrade head