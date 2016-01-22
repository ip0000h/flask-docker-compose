# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from users.decorators import requires_login


main_blueprint = Blueprint('', __name__)


@main_blueprint.route('/')
def index():
    return render_template('index.html', page=u"It's working!")


@main_blueprint.route('/secret')
@requires_login
def secret():
    return render_template('index.html', page=u"Secret page!")
