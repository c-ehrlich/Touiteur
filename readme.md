# Touiteur

Touiteur is a feature-rich Twitter clone with Django + Postgres in the backend and HTML + CSS + JS + a small amount of Bootstrap in the frontend.

[Demo video](https://www.youtube.com/watch?v=2aNYwn2iMns)

[Live Demo on Heroku](https://touiteur-app.herokuapp.com/) (existing images might be broken as Heroku regularly deletes static/media files, also don't expect great performance as this is on a free heroku instance)

## Table of Contents

*   [Installation](#installation)
*   [Features and Design Considerations](#features-and-design-considerations)
    *   [Front-End](#front-end)
    *   [Back-End](#back-end)
    *   [Database](#database)
*   [Screenshots](#screenshots)
*   [Potential Improvements](#potential-improvements)

## Installation

### Debug Mode
1. Install the required packages with `pip install -r requirements.txt`
2. `./manage.py makemigrations`, `./manage.py migrate`
3. `django-admin compilemessages` to prepare the i18n files
4. Run the development server with `python manage.py runserver`

### Deployment
- The project can easily be deployed with Docker. This requires taking it out of debug mode, disabling Django Debug Toolbar, setting up static file serving, and creating separate containers for the app/db, as well as a (nginx-based) server for static files. 
- While it is possible to get it running on an Alpine image, I would recommend the standard Python image as this includes most of the dependencies.

## Features and Design Considerations

### Front-End
- [x] After creating a new account, there is an onboarding process where the user decides things such as their profile picture, language, theme, and privacy options.
- [x] The app is fully translated into three languages using i18n. Logged in users see the language they have selected as their preference. Logged out users see the language of their browser locale, or English if their locale is not available.
- [x] The app has light and dark mode. This is achieved by giving a class to the `<body>` element based on a user preference, and using CSS variables combined with a themes.css file to determine the color of elements.
- [x] There are live-updating notifications for mentions (which show up regardless of where the user is) as well as notifications for new posts in the current view.
- [x] Users can not see posts of users that they are blocked by
- [x] Posts by blocked accounts are hidden by default, but the user can click a button to reveal them. However they cannot reply.
- [x] Users can attach images to posts, and can delete their image / select a new one prior to sending the post
- [x] Users can edit their own posts
- [x] Each post has a slide-out reply panel that is activated or hidden by clicking the reply button in the post
- [x] The front-end is written entirely in Vanilla JS (in addition to HTML/Jinja/CSS). This was mostly a decision made for the sake of finding the limits of Vanilla JS.


### Back-End
- [x] All necessary routes are CSRF protected
- [x] All data is checked prior to processing to not create invalid database items
    - A user cannot follow a non-existing user, or a user that has blocked them, or themselves
    - Users can't have the same username (but can have the same display name)
    - Users cannot reply to posts of users who they have blocked or are blocked by
    - Nonexistent posts cannot be replied to
    - etc.
- [x] All API routes return the simplest possible Json objects

### Database
- [x] The database is normalized to 3NF
- [x] All ORM queries use Django features such as prefetch_related, select_related, annotate, etc. to improve performance. The SQL queries to load a page of posts including images, follow and block relationship information, reply counts, etc. typically take between 20-30ms.

## Screenshots
- Coming soon!

## Potential Improvements
- Currently everything is being run from the main Postgres database. This is not ideal in terms of scaling as for example getting live notifications is quite db intensive. A better design would be to have a separate database, which is optimised for performance (for example Redis), for things that need to be accessed frequently.
- Adding a Redis database would also allow some additional features that rely on very fast db queries, such as autocomplete/suggestions on usernames.
- There are some obvious additional features that could be implemented
  - Reporting posts
  - Letting admins ban users without having to delete the entire account
  - Switching from Pagination to infinite scrolling (the decision to use Pagination was based on the CS50web requirements)
- Vanilla JS is not the best choice in terms of maintainability for the front-end, but it was chosen due to the self-teaching aspect of the project.
