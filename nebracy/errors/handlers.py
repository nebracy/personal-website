from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title="Page Not Found"), 404


@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title="Internal Server Error"), 500
