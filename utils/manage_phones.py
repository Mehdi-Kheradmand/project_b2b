import random
from phones.models import Phone


def add_phone(phones_to_add: int = 10) -> str:
    for c in range(0, phones_to_add):
        random_num = random.randint(100000000, 999999999)
        Phone.objects.create(number="09" + str(random_num))
    return f"{phones_to_add} Phones added"


def remove_all() -> str:
    phones = Phone.objects.all()
    counter = phones.count()
    phones.delete()
    return f"{counter} Phones deleted"
