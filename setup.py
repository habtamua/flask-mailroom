import random

from passlib.hash import pbkdf2_sha256
from model import db, Donor, Donation, User

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation])
db.create_tables([User, Donor, Donation])


alice = Donor(name="Alice")
alice.save()

bob = Donor(name="Bob")
bob.save()

charlie = Donor(name="Charlie")
charlie.save()

donors = [alice, bob, charlie]

for x in range(30):
    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()

User(username="admin", password=pbkdf2_sha256.hash("password123")).save()
User(username="bob", password=pbkdf2_sha256.hash("bobbob123")).save()
