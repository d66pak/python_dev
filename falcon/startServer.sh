#!/usr/bin/env bash

gunicorn -b 0.0.0.0:9090 things:app --reload