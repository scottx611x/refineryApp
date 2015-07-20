# Scott Ouellette
# refineryApp

from datetime import datetime
from .. import db
from datetime import datetime
from .. import db


# DB Model for a Category -> Unique name, Description, creation date, last modified date
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	name = db.Column(db.Text(), unique=True)
	category_Description = db.Column(db.Text())
	date_Created = db.Column(db.DateTime(), default=datetime.utcnow)
	last_Modified = db.Column(db.DateTime(), default=datetime.utcnow,
										  onupdate=datetime.utcnow)

	def __init__(self, name='', category_Description=''):
		self.name = name
		self.category_Description = category_Description

	def __repr__(self):
		return 'Category: {}'.format(self.name)

# DB Model for a Workflow -> Unique name, Description, # of Steps, creation date, last modified date
class Workflow(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

	#Each workflow must be assigned to one or more categories
	category = db.relationship('Category', backref=db.backref('workflow',
													  lazy='dynamic'))
	name = db.Column(db.Text())
	workflow_Description = db.Column(db.Text())
	workflow_Steps = db.Column(db.Integer)
	date_Created = db.Column(db.DateTime(), default=datetime.utcnow)
	last_Modified = db.Column(db.DateTime(), default=datetime.utcnow,
										  onupdate=datetime.utcnow)
	def __init__(self, post='',name='', workflow_Description='', workflow_Steps=''):
		if post:
			self.category_id = post
		self.name = name
		self.workflow_Description = workflow_Description
		self.workflow_Steps = workflow_Steps

	def __repr__(self):
		#account for the pluralization of the word "Step"
		if (self.workflow_Steps > 1):
			return 'Workflow: {} [{} Steps] \n\n {}'.format(self.name, self.workflow_Steps, self.workflow_Description)
		else:
			return 'Workflow: {} [{} Step] \n\n {}'.format(self.name, self.workflow_Steps, self.workflow_Description)
