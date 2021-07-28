# PROJECT NAME

(introduction + key features)

## Table of Contents

*   [Installation](#installation)
*   [Features and Design Considerations](#features-and-design-considerations)
    *   [Front-End](#front-end)
    *   [Back-End](#back-end)
    *   [Database](#database)
*   [Screenshots](#screenshots)
*   [Potential Improvements](#potential-improvements)]

## Installation

1. Install the required packages with `pip install -r requirements.txt`
2. (database setup)
3. (create a superuser)
4. Run the development server with `python manage.py runserver` (TODO change to setup for running a real server, or maybe even give instructions for a docker setup)

## Features and Design Considerations

### Front-End

### Back-End

### Database

## Screenshots

## Potential Improvements

*   Currently everything is being run from the main Postgres database. This is not ideal in terms of scaling as for example getting live notifications is quite db intensive. A better design would be to have a separate database, which is optimised for performance (for example Redis), for things that need to be accessed frequently.