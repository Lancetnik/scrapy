This is the Django Rest Framework template with loguru (logging & debug), dotenv (loading env vars from file), djoser & jwt auth, django-filters, swagger auto docs, cors headers politics
# Setup
1. install with `pip install loguru python-dotenv psycopg2 django djangorestframework djoser djangorestframework_simplejwt django-filter drf-yasg django-cors-headers==3.5.0` or use `pip install -r requirements.txt`
2. Create from backend/example.env => backend/.env with yours settings 
3. from backend/ run server `python manage.py migrate` and `python manage.py runserver`
 
 # Auth methods
1. Use `post` - `/auth/token/login/` - `{username: '', password: ''}` for log in and getting your auth token
2. Use `post` - `/auth/token/logout/` for out and deactivate token
3. Use `post` - `/auth/users/` - `{username: '', password: '', email: ''}` for create new user and send code on his email
4. Use `post` - `/auth/users/activation/` - `{uid: '', token: ''}` for activate new user (link from his email)

### JWT Auth
1. Use `post` - `/api/token/` - `{username: '', password: ''}` for log in and getting your auth tokens (pair)
2. Use `post` - `/api/token/refresh/` - `{refresh: 'your refresh token'}` to refresh access token
