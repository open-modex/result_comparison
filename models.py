
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_model_options(model):
    instances = model.query.all()
    return [{"label": instance.name, "value": instance.name} for instance in instances]


class Filter(db.Model):
    name = db.Column(db.String, primary_key=True)
    filters = db.Column(db.JSON(), nullable=True)
    scalar_graph_options = db.Column(db.JSON())
    ts_graph_options = db.Column(db.JSON())

    def __repr__(self):
        return '<Filter %r>' % self.name


class Colors(db.Model):
    name = db.Column(db.String, primary_key=True)
    colors = db.Column(db.JSON(), nullable=True)

    def __repr__(self):
        return '<Color %r>' % self.name


class Labels(db.Model):
    name = db.Column(db.String, primary_key=True)
    labels = db.Column(db.JSON(), nullable=True)

    def __repr__(self):
        return '<Label %r>' % self.name
