#!/bin/bash
.PHONY: default
.SILENT:


default:

start:
	gunicorn --bind localhost:8000 \
             --reload \
             --capture-output \
             warhammer.wsgi:application