from app import server, db, Filter, Colors, Labels


def create_all():
    with server.app_context():
        db.create_all()


def delete_entry(model, name):
    with server.app_context():
        entry = model.query.filter_by(name=name).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            print(f"Successfully deleted entry '{name}'.")
        else:
            print(f"No entry '{name}' found.")


def delete_filter(filter_name):
    delete_entry(Filter, filter_name)


def delete_color_map(color_map):
    delete_entry(Colors, color_map)


def delete_label(label):
    delete_entry(Labels, label)
