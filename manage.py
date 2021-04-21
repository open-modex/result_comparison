from app import server, db


def create_all():
    with server.app_context():
        db.create_all()


if __name__ == "__main__":
    create_all()
