"""
Models for Account Service

This module contains the data models for the Account Service
"""
from datetime import date
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an error in the data validation """


class Account(db.Model):
    """
    Class that represents an Account
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))
    date_joined = db.Column(db.Date(), nullable=False, default=db.func.current_date())

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates an Account to the database
        """
        Account.app.logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Account to the database
        """
        Account.app.logger.info("Updating %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes an Account from the data store"""
        Account.app.logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data: dict):
        """
        Deserializes an Account from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")

            # Fix: Correctly parse the isoformat date string
            date_joined_str = data.get("date_joined")
            if date_joined_str:
                self.date_joined = date.fromisoformat(date_joined_str)

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid Account: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or invalid data "
                + error.args[0]
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls) -> list:
        """Returns all of the Accounts in the database"""
        cls.app.logger.info("Processing all Accounts")
        return cls.query.all()

    @classmethod
    def find(cls, by_id: int):
        """Finds an Account by its ID"""
        cls.app.logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Accounts with the given name

        Args:
            name (string): the name of the Accounts you want to match
        """
        cls.app.logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
        