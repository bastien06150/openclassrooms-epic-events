from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="department")

    def __repr__(self):
        return f"Department(id={self.id}, name='{self.name}')"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employee_number = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    department = relationship("Department", back_populates="employees")
    clients = relationship(
        "Client", back_populates="sales_contact", foreign_keys="Client.sales_contact_id"
    )
    supported_events = relationship(
        "Event",
        back_populates="support_contact",
        foreign_keys="Event.support_contact_id",
    )

    def __repr__(self):
        return f"Employee(id={self.id}, full_name='{self.full_name}', email='{self.email}')"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(30), nullable=False)
    company_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sales_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    sales_contact = relationship(
        "Employee", back_populates="clients", foreign_keys=[sales_contact_id]
    )
    contracts = relationship("Contract", back_populates="client")

    def __repr__(self):
        return f"Client(id={self.id}, full_name='{self.full_name}', company_name='{self.company_name}')"


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    is_signed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")

    def __repr__(self):
        return f"Contract(id={self.id}, total_amount={self.total_amount}, is_signed={self.is_signed})"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    support_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    event_start = Column(DateTime, nullable=False)
    event_end = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="events")
    support_contact = relationship(
        "Employee", back_populates="supported_events", foreign_keys=[support_contact_id]
    )

    def __repr__(self):
        return f"Event(id={self.id}, name='{self.name}', location='{self.location}')"
