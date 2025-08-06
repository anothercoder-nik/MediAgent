#!/bin/bash
# Railway startup script
export PORT=${PORT:-5000}
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
