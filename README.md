# Farmsupp-BE

Farmsupp is a platform built for the agricultural sector that uses AI models to provides expert advice to farmers on crop management, market insights, and real-time problem-solving as well as provide agricultural knowledge updates, weather forecasts, and pest alerts. Farmsupp provides farmers with a platform to post agricultural related articles as well as manage produce listings.

## Requirements

- [Python](https://www.python.org/) is a high-level, general-purpose programming language. It is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library
- [Postgres](https://www.postgresql.org/) is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
- [Fastapi](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. Its key features are high performance, speed to develop features, reduction in bugs, ease of use, robustness.

## How to setup locally

- Clone repository using `git clone `
- Create a virtual environment in the project root folder and create a virtual environment using `python -m venv venv`
- Setup virtual environment by typing `source venv\Scripts\activate`
- Install requirements using `pip install -r requirements.txt`
- Run development server by typing `bash run_dev_server.sh`

## Useful commands

- `alembic revision --autogenerate` to automatically generate migrations
- `alembic upgrade head` to run migrations

## Author

[Alahira Jeffrey](https://github.com/alahirajeffrey)
