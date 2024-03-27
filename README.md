# votigo
Learning practical event sourcing with a sample project.

## Folders

### client
JS / HTML project that renders the frontend

### auth
Helpers for login

### filter
Filter aggregate and associated code

### option
Option aggregate and related

### vote
The main aggregate of this app

### votigo
The application level code

### Honorable Mention: main.py
Entry-point for ASGI servers

## Architecture
Event-sourced.

Vote -> base data of votes
Options -> data of options that can be picked in votes
Filters -> object trees that determine who can and can't vote
