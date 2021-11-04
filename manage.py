from app import server, db, Filter


def create_all():
    with server.app_context():
        db.create_all()


def delete_filter(filter_name):
    with server.app_context():
        filter_ = Filter.query.filter_by(name=filter_name).first()
        if filter_:
            db.session.delete(filter_)
            db.session.commit()
            print(f"Successfully deleted filter '{filter_name}'.")
        else:
            print(f"No filter '{filter_name}' found.")
