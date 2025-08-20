from flask import Flask, render_template, request, redirect, jsonify, session
from functools import wraps

from services import UrlShortenerService, AuthService


class UrlController:
    def __init__(self, url_service: UrlShortenerService):
        self.url_service = url_service

    def index(self):
        if request.method == 'POST':
            try:
                long_url = request.form.get['long_url']
                if not long_url:
                    return render_template('index.html', error='Please enter a long url')

                url = self.url_service.create_short_url(long_url)
                urls = self.url_service.get_all_urls()
                return render_template('index.html', links=urls, success=f"Short URL created: {url.short_url}")
            except Exception as e:
                return render_template('index.html', error=e)

        try:
            urls = self.url_service.get_all_urls()
            return render_template('index.html', links=urls)
        except Exception as e:
            return render_template('index.html', error=e)

    def redirect_short(self, short_url: str):
        try:
            long_url = self.url_service.get_long_url(short_url)
            if long_url:
                return redirect(long_url, code=302)
            else:
                return "URL not found", 404
        except Exception:
            return "Internal Server Error", 500

    def update(self, url_id: int):
        if request.method in ['POST', 'PUT']:
            try:
                short_url = request.form.get('short_url')
                long_url = request.form.get('long_url')

                if not short_url or not long_url:
                    return render_template('404.html', error="Both short_url and long_url are required")

                updated_url = self.url_service.update_url(url_id, short_url, long_url)
                if not updated_url:
                    return render_template('404.html')

                return render_template('update.html', link=updated_url, success=f"Short URL updated: {short_url}")

            except ValueError as e:
                url = self.url_service.get_url_by_id(url_id)
                return render_template('update.html', link=url, error=e)
            except Exception as e:
                return render_template('update.html', error=e)

        try:
            url = self.url_service.get_url_by_id(url_id)
            if not url:
                return render_template('404.html')
            return render_template('update.html', link=url)
        except Exception:
            return render_template('404.html')

    def delete(self, url_id: int):
        try:
            if self.url_service.delete_url(url_id):
                return render_template('success_delete.html')
            else:
                return render_template('404.html', error="URL not found")
        except Exception as e:
            return render_template('delete.html', error=e)


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                return jsonify({'error': 'Please enter username and password'})

            token = self.auth_service.authenticate(username, password)
            if token:
                session['logged_in'] = True
                return jsonify({'token': token})
            else:
                return jsonify({'error': 'Invalid username or password'})

        return render_template('login.html')

    def home(self):
        if not session.get('logged_in'):
            return render_template('login.html')
        return 'Logged in currently'

    def public(self):
        return 'For public'

    def protected(self):
        return 'JWT is verified. Welcome to your dashboard'

def create_token_required_decorator(auth_service: AuthService):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'error': 'Please provide a token'})

            user = auth_service.validate_token(token)
            if not user:
                return jsonify({'error': 'Invalid token'})

            return f(*args, **kwargs)
        return decorated
    return token_required