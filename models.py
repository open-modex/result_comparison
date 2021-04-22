
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Filter(db.Model):
    name = db.Column(db.String, primary_key=True)
    filters = db.Column(db.JSON(), nullable=True)
    scalar_graph_options = db.Column(db.JSON())
    ts_graph_options = db.Column(db.JSON())

    def __repr__(self):
        return '<Filter %r>' % self.name
