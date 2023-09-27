"""
This Python file defines a SQLAlchemy-based database model for a finance application.
 The key components of this code include:

1. Importing necessary modules such as 'hashlib,' 'sqlalchemy,' 'datetime,' 'passlib.hash,' and 'cryptography.fernet'
 for database modeling, password hashing, and encryption.

2. Creating an SQLite database engine using SQLAlchemy with the filename 'finance_app.db.'

3. Defining a base class 'Base' using SQLAlchemy's 'declarative_base()' to serve as a base class
 for database model classes.

4. Defining several database model classes:
   - 'User': Represents user information, including username, name, email, date of birth,
    and relationships with other tables.
   - 'Password': Stores hashed user passwords and provides methods for setting and verifying passwords.
   - 'Subscription': Tracks user subscriptions, payment status, and subscription dates.
   - 'PasswordResetRequest': Manages user password reset requests, including tokens and timestamps.
   - 'CreditCard': Stores encrypted credit card information and provides methods
    for setting and retrieving card details.

5. The code includes relationships between these tables, allowing for easy retrieval of related data.

6. The 'set_password' method in the 'Password' class uses bcrypt to hash user passwords, enhancing security.

7. The 'set_credit_card_info' and 'get_credit_card_info' methods in the 'CreditCard' class encrypt
 and decrypt credit card information using Fernet symmetric encryption.

8. A Fernet key is generated and used for encryption and decryption of sensitive data.

9. The database schema is created using the 'Base.metadata.create_all(engine)' command,
 which sets up the database tables based on the defined models.

This code serves as the database model for the finance application, defining the structure of the database and
 how user data, passwords, subscriptions, and credit card information are stored and managed.
"""

from sqlalchemy import Column, String, create_engine, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from passlib.hash import bcrypt
from cryptography.fernet import Fernet


engine = create_engine("sqlite:///finance_app.db")
Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    id = Column(String(36), primary_key=True, unique=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    dob = Column(String)
    created = Column(DateTime, default=datetime.now)
    password = relationship("Password", back_populates="userpass", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="usersubs", cascade="all, delete-orphan")
    requests = relationship("PasswordResetRequest", back_populates="userpassreq", cascade="all, delete-orphan")
    creditcards = relationship("CreditCard", back_populates="usercreditcard", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates='userinv')


class Password(Base):
    __tablename__ = "Password"
    id = Column(Integer, primary_key=True)
    hash_password = Column(String, nullable=True)
    user_id = Column(String(36), ForeignKey("Users.id"), unique=True)
    userpass = relationship("User", back_populates="password")

    def set_password(self, password):
        self.hash_password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.hash_password)


class Subscription(Base):
    __tablename__ = "Subscription"
    id = Column(Integer, primary_key=True)
    payment = Column(Boolean, default=False)
    date = Column(DateTime, default=None)
    user_id = Column(String(36), ForeignKey("Users.id"), unique=True)
    usersubs = relationship("User", back_populates="subscription")


class PasswordResetRequest(Base):
    __tablename__ = "PasswordResetRequests"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), ForeignKey("Users.id"), unique=True)
    token = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.now)
    userpassreq = relationship("User", back_populates="requests")


class CreditCard(Base):
    __tablename__ = "CreditCards"
    id = Column(Integer, primary_key=True)
    encrypted_number = Column(String)
    encrypted_expiry_date = Column(String)
    encrypted_cvv = Column(String)
    encrypted_name = Column(String)
    encrypted_address = Column(String)

    user_id = Column(String(36), ForeignKey("Users.id"), unique=True)
    usercreditcard = relationship("User", back_populates="creditcards")

    def set_credit_card_info(self, number, expiry_date, cvv, name, address):
        fernet = Fernet(key)
        self.encrypted_number = fernet.encrypt(number.encode())
        self.encrypted_expiry_date = fernet.encrypt(expiry_date.encode())
        self.encrypted_cvv = fernet.encrypt(cvv.encode())
        self.encrypted_name = fernet.encrypt(name.encode())
        self.encrypted_address = fernet.encrypt(address.encode())

    def get_credit_card_info(self):
        fernet = Fernet(key)
        number = fernet.decrypt(self.encrypted_number).decode()
        expiry_date = fernet.decrypt(self.encrypted_expiry_date).decode()
        cvv = fernet.decrypt(self.encrypted_cvv).decode()
        name = fernet.decrypt(self.encrypted_name).decode()
        address = fernet.decrypt(self.encrypted_address).decode()
        return number, expiry_date, cvv, name, address


class Invoice(Base):
    __tablename__ = "Invoice"
    id = Column(String(36), primary_key=True, unique=True)
    username = Column(String, ForeignKey('Users.username'))
    date = Column(DateTime, default=datetime.now)
    userinv = relationship("User", back_populates="invoices")


key = Fernet.generate_key()


Base.metadata.create_all(engine)
