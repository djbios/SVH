#!/bin/bash

exec celery worker -A svh -l info -B
