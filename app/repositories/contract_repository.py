from app.models import Contract


class ContractRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Contract).all()

    def get_by_id(self, contract_id: int):
        return self.session.query(Contract).filter_by(id=contract_id).first()

    def create(self, contract: Contract):
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        return contract

    def update(self, contract: Contract):
        self.session.commit()
        self.session.refresh(contract)
        return contract

    def delete(self, contract):
        self.session.delete(contract)
        self.session.commit()
