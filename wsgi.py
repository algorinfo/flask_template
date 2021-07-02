# required by gunicorn
from werkzeug.middleware.proxy_fix import ProxyFix
# from werkzeug.middleware.profiler import ProfilerMiddleware # debug

from changeme import create_app

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
# app.config['PROFILE'] = True # debug
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30]) # debug

