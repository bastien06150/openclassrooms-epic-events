from app.models import Event


class EventRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Event).all()

    def get_by_id(self, event_id: int):
        return self.session.query(Event).filter_by(id=event_id).first()

    def create(self, event: Event):
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def update(self, event: Event):
        self.session.commit()
        self.session.refresh(event)
        return event

    def delete(self, event):
        self.session.delete(event)
        self.session.commit()
