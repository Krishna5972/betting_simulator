from simulator import db
from simulator.models import *
db.drop_all()
db.create_all()