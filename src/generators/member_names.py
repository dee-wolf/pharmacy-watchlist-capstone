import random
from itertools import product

first_names = ["Andrew",
    "Raven", "Dominic",
    "Nicholas", "Becca",
    "David", "Dee",
    "John", "Paul",
    "George", "Ringo",
    "Mickey", "Minnie",
    "Fabian", "Gorgug",
    "Riz", "Fig",
    "Adaine", "Kristen",
    "Tula", "Jaysohn",
    "Viola", "Ava",
    "Lila", "Thorn Vale",
    "Jawbone", "Gorthulax",
    "Gilear", "William",
    "Bimothy", "Benjamin",
    "Geoffrey", "Kenji",
    "Olliver", "Bennet",
    "Sybil", "Lukas",
    "Beatrix", "Kevin",
    "Sandra", "Brennan",
    "Sam"]

last_names = ["Smith",
    "Brown", "Seacaster",
    "Mouse", "Lennon",
    "Gukgak", "Thistlespring",
    "Abernant", "Applebees",
    "Faeth", "Mulligan",
    "Stoat", "Young",
    "White", "Starr",
    "Dock", "Ellis",
    "Swanson", "Lightbourne",
    "Browne", "Fille",
    "Ferne", "Reich",
    "Chestang", "Knowles",
    "Roan", "Apple",
    "Cooke", "Musek",
    "Claudio", "Hero",
    "Benedictus", "Lastname",
    "Dosney", "Allis",
    "Drumpf", "Sonck",
    "Chien", "Colbort",
    "Kemmil", "Sompsin",
    "Knipe", "Porkins",
    "Loudgate", "Dryer",
    "Prott", "Evins",
    "Homswrith", "Diwney",
    "Wolf"]

def generate_member_names(num_members=1000, seed=84):
    if isinstance(num_members, bool) or not isinstance(num_members, int):
        raise TypeError("Please enter a whole number for the number of members.")
    if num_members <= 0:
        raise ValueError("Please enter a whole number greater than zero for the number of members.")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("Please enter a whole number for the seed.")
    member_combos = product(first_names, last_names)
    all_member_names = [
        f"{first_name} {last_name}"
        for first_name, last_name in member_combos]
    if num_members > len(all_member_names):
        raise ValueError(
            f"Please create no more than {len(all_member_names)} members.")
    name_rng = random.Random(seed)
    member_names = name_rng.sample(all_member_names, k=num_members)
    return member_names
