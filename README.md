# inversity-17-T13
Inversity Crown Estate challenge repo for team 13
# Project Title

A brief description of what this project does and who it's for.

## Description

This project is a full-stack web application utilizing Flask for the backend and Vue 3 with Vite for the frontend. It aims to provide a seamless integration between a Python-powered server and a modern JavaScript SPA (Single Page Application).

### Backend

The backend is built with Flask, a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

#### Features:

- RESTful API endpoints.
- Error handling.
- Serving static files and templates.

#### Getting Started

1. Navigate to the `back_end` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables:
   - Windows: `set FLASK_APP=wsgi.py`
   - macOS/Linux: `export FLASK_APP=wsgi.py`
6. Run the application: `flask run`

### Frontend

The frontend is built with Vue 3 and Vite. Vue 3 is the latest version of the Vue.js framework, offering improved performance and better composition API. Vite is a build tool that significantly improves the frontend development experience.

#### Features:

- Vue 3 `<script setup>` SFCs.
- Hot Module Replacement (HMR) for rapid development.
- Tailwind CSS for styling.

#### Getting Started

1. Navigate to the `front_end` directory.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## Deployment

This section should describe how to deploy this project on a live system.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## License

This project is licensed under the [MIT License](LICENSE.md) - see the file for details.