import datetime
import functools
import flask
import werkzeug
from ..dependencies import *
from ..services import *
from ..application.login import *
from ..application.logout import *
from ..application.page_get import *
from ..application.page_save import *
from ..domain.models.page import *
from ..domain.models.password import *
from ..domain.models.session import *
from ..domain.repositories.isession_repository import *


app = flask.Flask(
    __name__,
    template_folder='views/templates',
    static_folder='views/static'
)


def login_required(api:bool=False, redirect:str=''):
    def decorator(f):
        @functools.wraps(f)
        def decorated_func(*args, **kwargs):
            if flask.g.session is None:
                if api:
                    raise werkzeug.exceptions.NotAuthorized()
                else:
                    return flask.redirect(flask.url_for('page', path=redirect))
            return f(*args, **kwargs)
        return decorated_func
    return decorator


@app.before_request
def before_request():
    session_repository = Dependency.resolve(ISessionRepository)
    session_id = SessionId(flask.request.cookies.get('session_id', ''))
    try:
        flask.g.session = session_repository.get(session_id)
    except SessionError:
        flask.g.session = None


@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        password = Password(flask.request.form['password'])
        request = LoginRequest(password=password)
        response = Service.call(request)
        return flask.jsonify({
            'session_id': response.session.session_id.value,
            'expires': response.session.expires.value.timestamp()
        })
    except (KeyError, ValueError, TypeError, LoginError):
        raise werkzeug.exceptions.BadRequest()


@app.route('/api/logout', methods=['POST'])
@login_required(api=True)
def api_logout():
    try:
        session_id = SessionId(flask.request.form['session_id'])
        request = LogoutRequest(session_id=session_id)
        response = Service.call(request)
        return flask.jsonify({})
    except (KeyError, ValueError, TypeError):
        raise werkzeug.exceptions.BadRequest()


@app.route('/api/page/', methods=['GET'], defaults={'path': 'index'})
@app.route('/api/page/<string:path>', methods=['GET', 'POST'])
@login_required(api=True)
def api_page(path: str):
    if flask.request.method == 'POST':
        try:
            page_id = PageId(path)
            title = PageTitle(flask.request.form['title'])
            body = PageBody(flask.request.form['body'])
            lastmodified = PageLastModified(
                datetime.datetime.now(datetime.timezone.utc))
            version = PageVersion(int(flask.request.form['version']))
            page = Page(
                page_id=page_id,
                title=title,
                body=body,
                lastmodified=lastmodified,
                version=version
            )
            request = PageSaveRequest(page=page)
            response = Service.call(request)
        except (KeyError, ValueError, TypeError, PageError):
            raise werkzeug.exceptions.BadRequest()
    request = PageGetRequest(PageId(path))
    response = Service.call(request)
    return flask.jsonify({
        'page_id': response.page.page_id.value,
        'title': response.page.title.value,
        'body': response.page.body.value,
        'lastmodified': response.page.lastmodified.value.timestamp(),
        'version': response.page.version.value
    })


@app.route('/login', methods=['GET'])
def login():
    if flask.g.session is not None:
        return flask.redirect(flask.url_for('page', path=''))
    return flask.render_template('page.html', view='login')


@app.route('/', methods=['GET', 'POST'], defaults={'path': 'index'})
@app.route('/<string:path>', methods=['GET', 'POST'])
def page(path: str):
    request = PageGetRequest(PageId(path))
    response = Service.call(request)
    if 'edit' in flask.request.values:
        if flask.g.session is None:
            return flask.redirect(flask.url_for('page', path=path))
        return flask.render_template(
            'page.html',
            view='edit', session=flask.g.session, page=response.page)
    return flask.render_template('page.html',
        view='page', session=flask.g.session, page=response.page)
