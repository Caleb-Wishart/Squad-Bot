# UQCSC-Bot V2.0

[![Discord](https://img.shields.io/discord/809997432011882516?color=blue&label=UQCS%20Discord&logo=discord)](https://discord.gg/JpjaB2FNdW)

[![Python Version 3.10](https://img.shields.io/badge/python-3.10-blue.svg?logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/Caleb-Wishart/Squad-Bot/pulls)
![Works on my machine](https://img.shields.io/badge/WORKS%20ON-MY%20MACHINE-red)

A somewhat complete discord bot template with example cogs that uses a Postgresql server as a storage mechanism.

Primary used for the [UQCS Courses Discord Server](https://discord.gg/JpjaB2FNdW).

[![Docker](https://img.shields.io/badge/Docker-test?logo=docker&color=grey)](https://www.docker.com/)  
Docker files are included for easy deployment.

## Contributing

This repository uses the [Black code style](https://black.readthedocs.io/en/stable/) to format python files. \
The use of the [flake8](https://pypi.org/project/flake8/) and [isort](https://pypi.org/project/isort/) is highly prefered.

See [requirements-dev.txt](./bot/requirements-dev.txt).

## Main Features
 - Main bot
   - Configure with environment variables
   - File logging
   - PSQL Database connection
   - Cogs manager / default commands
 - Cogs
   - Administrative
     - manage cogs
     - clear messages
     - sync app commands
   - General
     - Fortune
     - Ping
     - Decide
   - Statistics
     - Determine how many times a particular message has been sent to a channel
     - Role based rewards
     - Leaderboard scoring system
     - Configurable by discord message
   - Reminders
     - Create / Delete repeating or once off reminders
   - Courses
     - Enrol / Drop courses (channels)
     - Auto delete empty channels
     - database storage