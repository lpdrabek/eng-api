#!/bin/bash

uwsgi --socket :8000 --mount /=app:app #--daemonize ./log/log.log
