from flask import Flask
from repositories import SQLiteUrlRepository, InMemoryAuthRepository
from services import UrlShortenerService, AuthService, JWTService
from controllers import UrlController, AuthController, create_token_required_decorator
from utils import create_token_required_decorator

def create_app(config=None):
    app = Flask(__name__)

    # Configuration
    if config:
        app.config.update(config)
    else:
        app.config.update({
            'SECRET_KEY': '17d12f754a0b418eaab9eb3ef876165e',
            'DATABASE_PATH': 'urls.db'
        })

    # Dependency Injection
    url_repository = SQLiteUrlRepository(app.config['DATABASE_PATH'])
    auth_repository = InMemoryAuthRepository()
    jwt_service = JWTService(app.config['SECRET_KEY'])

    url_service = UrlShortenerService(url_repository)
    auth_service = AuthService(auth_repository, jwt_service)

    url_controller = UrlController(url_service)
    auth_controller = AuthController(auth_service)

    token_required = create_token_required_decorator(auth_service)

    # Routes
    @app.route('/')
    def home():
        return auth_controller.home()

    @app.route('/public')
    def public():
        return auth_controller.public()

    @app.route('/auth')
    def auth():
        return auth_controller.protected()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return auth_controller.login()

    @app.route('/link', methods=['GET', 'POST'])
    def index():
        return url_controller.index()

    @app.route('/link/<short_url>')
    def redirect_short(short_url):
        return url_controller.redirect_short(short_url)

    @app.route('/link/<int:url_id>', methods=['GET', 'POST', 'PUT'])
    def update(url_id):
        return url_controller.update(url_id)

    @app.route('/link/del/<int:url_id>', methods=['GET', 'POST', 'DELETE'])
    def delete(url_id):
        return url_controller.delete(url_id)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)