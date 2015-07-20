# Scott Ouellette
# refineryApp

from flask import Blueprint, request, g, redirect, url_for, abort, \
                  render_template
from flask.views import MethodView
from wtforms.ext.sqlalchemy.orm import model_form
from app import db
from .models import Category, Workflow

#Blueprint allows for all viewsto be prefixed with "/refineryApp/"
refineryApp = Blueprint('refineryApp', __name__, template_folder='templates')


class ViewHelper(MethodView):
    Categories_template = 'refineryApp/Categories.html'
    Workflows_template = 'refineryApp/Workflows.html'
    refineryApp_template = 'refineryApp/refineryApp.html'
    edit_template = 'refineryApp/Edit.html'

    def __init__(self, model, endpoint, Categories_template=None, Workflows_template = None,refineryApp_template=None,
                 edit_template=None, exclude=None, filters=None):
        self.model = model
        self.endpoint = endpoint
        # so we can generate a url relevant to this
        # endpoint, for example if we utilize this CRUD object
        # to enpoint workflows the path generated will be
        # /refineryApp/workflows/
        self.path = url_for('.%s' % self.endpoint)

        if self.endpoint == "/refineryApp/category/":
            self.Categories_template = Categories_template
        if self.endpoint == "/refineryApp/workflows/":
            self.Workflows_template = Workflows_template
        if self.endpoint == "/refineryApp/":
            self.refineryApp_template = refineryApp_template
        if edit_template:
            self.edit_template = edit_template
        self.filters = filters or {}
        self.ObjForm = model_form(self.model, db.session, exclude=exclude)

    def render_edit(self, **kwargs):
        return render_template(self.edit_template, path=self.path, **kwargs)

    def render_Category(self, **kwargs):
        return render_template(self.Categories_template, path=self.path,
                               filters=self.filters, **kwargs)
    def render_Workflows(self, **kwargs):
        return render_template(self.Workflows_template, path=self.path,
                               filters=self.filters, **kwargs)
    def render_refineryApp(self, **kwargs):
        return render_template(self.refineryApp_template, path=self.path,
                               filters=self.filters, **kwargs)
    def get(self, obj_id='', operation='', filter_name=''):
        if operation == 'new':
            #  we just want an empty form
            form = self.ObjForm()
            action = self.path
            return self.render_edit(form=form, action=action)
            
        if operation == 'delete':
            obj = self.model.query.get(obj_id)
            db.session.delete(obj)
            db.session.commit()
            return redirect(self.path)

        if obj_id:
            # this creates the form fields base on the model
            # so we don't have to do them one by one
            ObjForm = model_form(self.model, db.session)

            obj = self.model.query.get(obj_id)
            # populate the form with our category data
            form = self.ObjForm(obj=obj)
            # action is the url that we will later use
            # to do post, the same url with obj_id in this case
            action = request.path
            return self.render_edit(form=form, action=action)
        print self.path
        obj = self.model.query.order_by(self.model.date_Created.desc()).all()
        if self.path == "/refineryApp/":
            return self.render_refineryApp(obj=obj)
        elif "Category" in str(obj):
            return self.render_Category(obj=obj)
        elif "Workflow" in str(obj):
            return self.render_Workflows(obj=obj)
        

    def post(self, obj_id=''):
        # either load and object to update if obj_id is given
        # else initiate a new object, this will be helpfull
        # when we want to create a new object instead of just
        # editing existing one
        if obj_id:
            obj = self.model.query.get(obj_id)
        else:
            obj = self.model()

        ObjForm = model_form(self.model, db.session)
        # populate the form with the request data
        form = self.ObjForm(request.form)
        # this actually populates the obj (the category post)
        # from the form, that we have populated from the request post
        form.populate_obj(obj)

        db.session.add(obj)
        db.session.commit()

        return redirect(self.path)


def register_ViewHelper(app, url, endpoint, model, decorators=[], **kwargs):
    view = ViewHelper.as_view(endpoint, endpoint=endpoint,
                            model=model, **kwargs)

    for decorator in decorators:
        view = decorator(view)

    app.add_url_rule('%s/' % url, view_func=view, methods=['GET', 'POST'])
    app.add_url_rule('%s/<int:obj_id>/' % url, view_func=view)
    app.add_url_rule('%s/<operation>/' % url, view_func=view, methods=['GET'])
    app.add_url_rule('%s/<operation>/<int:obj_id>/' % url, view_func=view,
                     methods=['GET'])
    app.add_url_rule('%s/<operation>/<filter_name>/' % url, view_func=view,
                     methods=['GET'])

category_filters = {
    'created_asc': lambda model: model.query.order_by(model.date_Created.asc()),
    'updated_desc': lambda model: model.query.order_by(model.last_Modified.desc())
}
workflow_filters = {
    'created_asc': lambda model: model.query.order_by(model.date_Created.asc()),
    'updated_desc': lambda model: model.query.order_by(model.last_Modified.desc())
}

register_ViewHelper(refineryApp, '/', 'refineryApp', Category, filters=category_filters)
register_ViewHelper(refineryApp, '/categories', 'categories', Category, filters=category_filters)
register_ViewHelper(refineryApp, '/workflows', 'workflows', Workflow, filters=workflow_filters)