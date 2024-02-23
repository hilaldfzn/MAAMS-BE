# MAAMS (PBL Plus)

[![Production](https://gitlab.cs.ui.ac.id/maams-ppl/maams-be/badges/main/pipeline.svg?key_text=production&key_width=75)](https://gitlab.cs.ui.ac.id/maams-ppl/maams-be/-/pipelines?ref=main)
[![Staging](https://gitlab.cs.ui.ac.id/maams-ppl/maams-be/badges/ci-cd/pipeline.svg?key_text=staging)](https://gitlab.cs.ui.ac.id/maams-ppl/maams-be/-/pipelines?ref=staging)
[![Code Coverage](https://sonarcloud.io/api/project_badges/measure?project=maams-ppl_maams-be&metric=coverage)](https://sonarcloud.io/summary/new_code?id=maams-ppl_maams-be)

**Kelompok-2 PPL C**

[[_TOC_]]

---

## Members

1. 2106752306 Adly Renadi Raksanagara
2. 2106638324 Naila Shafirni Hidayat
3. 2106750313 Raditya Aditama
4. 2106708904 Bagas Shalahuddin Wahid
5. 2106752294 Nicholas Sidharta
6. 2106650222 Rania Maharani Narendra
7. 2106705644 Rayhan Putra Randi

## About

- Metode untuk menelusuri sebab-musabab paling awal/dalam suatu masalah dan memberikan solusi yang mendasar. (Terutama keadaan bermasalah yang akan dipulihkan atau dinormalkan, bukan dilipatgandakan).
- Sejenis Root Cause Analysis
- Inspirasi konseptual menyusun MAAMS ini berasal dari analisis Aristoteles tentang kekhususan filsafat yakni “mencari sebab-sebab yang terdalam dari seluruh realitas” (Lorens Bagus, 1991).

## Links

- [API Staging](http://34.87.36.56/)
- [API Prod](http://34.143.155.67/)

## Environment Setup

1. Create and activate virtual environment (Python 3.8, 3.9, 3.10, 3.11)

    ```pwsh
    python -m venv .venv
    .venv\Scripts\activate.bat
    ```

2. Install required packages

    ```pwsh
    pip install -r requirements.txt
    ```

3. Create `.env` and `.env.dev` file to specify active development environment variables.

    `.env`:

    ```.env
    # ACTIVE ENVIRONMENT
    ENVIRONMENT=DEVELOPMENT
    ```

    `.env.dev`:

    ```.env.dev
    # Settings
    ALLOWED_HOSTS="localhost,127.0.0.1"
    SECRET_KEY=
    DEBUG=True

    # Database credentials
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_NAME=postgres
    DB_SCHEMA=maams
    ```

4. Initialize database tables

    ```pwsh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run local server

    ```pwsh
    python manage.py runserver
    ```

## Testing

1. Run `coverage` package testing library

    ```pwsh
    coverage run -m unittest
    ```

2. Export testing results to HTML/XML

    ```pwsh
    coverage html
    # or
    coverage xml
    ```
