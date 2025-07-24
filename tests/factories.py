import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from faker import Faker

from app.models import Client, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.first_name())
    surname = factory.LazyAttribute(lambda _: fake.last_name())
    credit_card = factory.LazyAttribute(
        lambda _: (
            fake.credit_card_number()
            if fake.boolean(chance_of_getting_true=70)
            else None
        )
    )
    car_number = factory.LazyAttribute(lambda _: fake.license_plate())


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    address = factory.LazyAttribute(lambda _: fake.address())
    opened = FuzzyChoice([True, False])
    count_places = FuzzyInteger(10, 100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
