#!/usr/bin/env bash
service nginx   start
pytest --cov-report=term  --cov-report=html:coverage
uwsgi --ini uwsgi.ini