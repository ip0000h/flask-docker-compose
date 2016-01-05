# -*- coding: utf-8 -*-
from flask import request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask.ext.login import current_user


class UserView(ModelView):
    can_delete = False
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
