# Scott Ouellette
# refineryApp

from app import app
import os

#Jinja2 enviornment filters that splits descriptions if they are too long
def splitCatDesc(string):
	desc = str(string)
	if len(desc) > 75:
		return desc[:75], desc[75:]
	else:
		return desc,""
def splitDesc(string):
	desc = str(string)
	if len(desc) > 65:
		return desc[:65], desc[65:]
	else:
		return desc,""

#injecting css directly into Jinja2 template as a string
def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

#remove sqilite db on server restart
os.remove("refineryApp.db")

#adding sample data to db
from app import db

from app.refineryApp.models import *

db.create_all()

from app import db
from app.refineryApp.models import Category, Workflow

a = Category('DNA-Seq Tools', 'Workflows designed for analysis of short read DNA sequencing data.')
b = Category('RNA-Seq Tools', 'Workflows designed for analysis of short read DNA sequencing data.')

db.session.add(a)
db.session.add(b)

db.session.commit()

a1 = Workflow(1, 'Quality Control', 'Perform quality control analysis of short read data with FastQC.', 1)
a2 = Workflow(1, 'Read Mapping with BWA', 'Align short reads using BWA.', 2)
a3 = Workflow(1, 'Read Mapping with Bowtie', 'Align short reads using Bowtie.', 2)
a4 = Workflow(1, 'Variant Calling with GATK', 'Call SNPs and short indels using the GATK toolkit (version 2).', 6)
  
b1 = Workflow(2, 'Quality Control', 'Perform quality control analysis of short read data with FastQC.', 1)
b2 = Workflow(2, 'Read Mapping with Bowtie', 'Align short reads using Bowtie.', 2)
b3 = Workflow(2, 'Quantification (RSEM)', 'Quantify mRNA levels using RSEM.', 2)
b4 = Workflow(2, 'Quantification with cuffdiff', 'mRNA levels using cuffdiff.', 1)

db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.add(a4)

db.session.add(b1)
db.session.add(b2)
db.session.add(b3)
db.session.add(b4)

db.session.commit()

if __name__ == '__main__':
	app.jinja_env.filters['splitDesc'] = splitDesc
	app.jinja_env.filters['splitCatDesc'] = splitCatDesc
	app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string
	app.run(debug=True)