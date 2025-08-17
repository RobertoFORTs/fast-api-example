import asyncio
from uuid import uuid4
from datetime import date, timedelta
from decimal import Decimal
from faker import Faker

from simple_api.infra.models.booking import Booking
from simple_api.infra.models.property import Property
from simple_api.infra.db import get_db

fake = Faker()

NUM_PROPERTIES = 5
NUM_BOOKINGS = 10

async def init_properties():
    async with get_db() as session:
        properties = []
        for _ in range(NUM_PROPERTIES):
            p = Property(
                id=uuid4(),
                title=fake.sentence(nb_words=5),
                address_street=fake.street_name(),
                address_number=str(fake.random_int(min=1, max=200)),
                address_neighborhood=fake.city_suffix(),
                address_city=fake.city(),
                address_state=fake.state_abbr().upper(),
                country="BR",
                rooms=fake.random_int(min=1, max=5),
                capacity=fake.random_int(min=1, max=10),
                price_per_night=Decimal(fake.random_int(min=100, max=1000))
            )
            session.add(p)
            properties.append(p)
        await session.commit()
        return properties

async def init_bookings(properties):
    async with get_db() as session:
        for _ in range(NUM_BOOKINGS):
            prop = fake.random_element(properties)
            start = date.today() + timedelta(days=fake.random_int(1, 30))
            end = start + timedelta(days=fake.random_int(1, 7))
            b = Booking(
                id=uuid4(),
                property_id=prop.id,
                client_name=fake.name(),
                client_email=fake.email(),
                start_date=start,
                end_date=end,
                guests_quantity=fake.random_int(min=1, max=prop.capacity)
            )
            session.add(b)
        await session.commit()

async def main():
    properties = await init_properties()
    await init_bookings(properties)

if __name__ == "__main__":
    asyncio.run(main())