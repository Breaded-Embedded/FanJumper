import random

PREFIXES = [
    "Sky", "Air", "Prop", "Spin", "Jet", "Fly",
    "Zip", "Hop", "Buzz", "Glide", "Wing", "Cloud"
]

CORES = [
    "Boy", "Kid", "Ace", "Dash", "Loop",
    "Hop", "Run", "Flip", "Zoom", "Surf"
]

def generate_username():
    name = random.choice(PREFIXES) + random.choice(CORES)

    # Occasionally add a short number
    if random.random() < 0.3:
        name += str(random.randint(1, 99))

    return name