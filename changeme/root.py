from flask import Blueprint
from flask import current_app as app
from flask import jsonify, url_for

root = Blueprint("root", __name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@root.route("/")
def hello():
    """ hello func """
    return jsonify({"msg": "Hi there!"})


@root.route("/routes")
def show_routes():
    """shows urls info
    """
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples

    return jsonify(links)
