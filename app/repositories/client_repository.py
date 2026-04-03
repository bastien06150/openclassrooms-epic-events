from app.models import Client


class ClientRepository:
    def __init__(self, session):
        self.session = session

    def create(self, client: Client):
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def get_all(self):
        return self.session.query(Client).all()

    def get_by_id(self, client_id: int):
        return self.session.query(Client).filter_by(id=client_id).first()

    def delete(self, client):
        self.session.delete(client)
        self.session.commit()
