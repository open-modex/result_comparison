from app import server, db, Filter, Colors, Labels, Scenarios
from data import dev


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


def delete_scenarios(scenario):
    delete_entry(Scenarios, scenario)


def delete_label(label):
    delete_entry(Labels, label)


def download_scenarios(scenarios_raw):
    scenarios = scenarios_raw.split(",")
    for i, id_ in enumerate(scenarios):
        print(f"Getting {i + 1}/{len(scenarios)}: ID #{id_}")
        dev.create_dummy_data(id_)
