#!/bin/bash

exec celery worker -A common -l info -B
