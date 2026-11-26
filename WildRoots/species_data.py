"""species_data.py - the 20 predefined species and the function that loads them
into the Linked List. (A tuple list is only used here to LOAD data once;
all storage and searching happens inside the Linked List.)"""

from linked_list import LinkedList

# name, scientific, type, habitat, temperature, pollution, water, climate, emoji, description
_RAW = [
    ("Neem", "Azadirachta indica", "Plant", "Forest", "Hot", "High", "Low", "Tropical", "🌳", "Hardy medicinal tree that thrives in heat and polluted air."),
    ("Banyan", "Ficus benghalensis", "Plant", "Forest", "Hot", "Medium", "Medium", "Tropical", "🌴", "Giant fig whose aerial roots grow into new trunks."),
    ("Cactus", "Cactaceae", "Plant", "Desert", "Hot", "Medium", "Low", "Dry", "🌵", "Stores water in its stem to survive long droughts."),
    ("Lotus", "Nelumbo nucifera", "Plant", "Wetland", "Hot", "Medium", "High", "Tropical", "🪷", "Sacred aquatic flower rising from muddy, still water."),
    ("Mangrove", "Rhizophora mangle", "Plant", "Wetland", "Hot", "High", "High", "Tropical", "🌿", "Salt-tolerant coastal tree that protects shorelines."),
    ("Pine", "Pinus", "Plant", "Mountain", "Cold", "Low", "Medium", "Temperate", "🌲", "Evergreen conifer with needle leaves made for cold slopes."),
    ("Sunflower", "Helianthus annuus", "Plant", "Grassland", "Moderate", "Medium", "Medium", "Temperate", "🌻", "Tall flower whose head follows the sun across the day."),
    ("Bamboo", "Bambusoideae", "Plant", "Forest", "Moderate", "Medium", "High", "Tropical", "🎋", "One of the fastest-growing plants on Earth."),
    ("Oak", "Quercus", "Plant", "Forest", "Moderate", "Low", "Medium", "Temperate", "🍂", "Long-lived hardwood that feeds many animals with acorns."),
    ("Water Lily", "Nymphaea", "Plant", "Aquatic", "Moderate", "Low", "High", "Temperate", "💮", "Floating leaves and flowers on calm, clean ponds."),
    ("Bengal Tiger", "Panthera tigris tigris", "Animal", "Forest", "Hot", "Low", "Medium", "Tropical", "🐅", "Powerful striped predator of dense forests."),
    ("Asian Elephant", "Elephas maximus", "Animal", "Grassland", "Hot", "Medium", "High", "Tropical", "🐘", "Large herbivore that needs lots of water and food daily."),
    ("Camel", "Camelus dromedarius", "Animal", "Desert", "Hot", "Medium", "Low", "Dry", "🐪", "Desert traveller that can go days without drinking."),
    ("Polar Bear", "Ursus maritimus", "Animal", "Aquatic", "Cold", "Low", "Medium", "Polar", "🐻‍❄️", "Arctic hunter that lives and hunts on sea ice."),
    ("Dolphin", "Delphinus", "Animal", "Aquatic", "Moderate", "Low", "High", "Temperate", "🐬", "Intelligent marine mammal that lives in social pods."),
    ("Red Fox", "Vulpes vulpes", "Animal", "Mountain", "Cold", "Medium", "Medium", "Temperate", "🦊", "Clever, adaptable hunter found in many habitats."),
    ("Frog", "Anura", "Animal", "Wetland", "Moderate", "Low", "High", "Tropical", "🐸", "Amphibian whose skin makes it sensitive to pollution."),
    ("Penguin", "Spheniscidae", "Animal", "Aquatic", "Cold", "Low", "High", "Polar", "🐧", "Flightless seabird built for swimming in icy water."),
    ("Deer", "Cervidae", "Animal", "Forest", "Moderate", "Low", "Medium", "Temperate", "🦌", "Graceful grazer of forest edges and clearings."),
    ("Crocodile", "Crocodylus", "Animal", "Wetland", "Hot", "Medium", "High", "Tropical", "🐊", "Ancient ambush predator of rivers and swamps."),
]

KEYS = ["name", "scientific_name", "type", "habitat", "temperature",
        "pollution", "water", "climate", "emoji", "description"]


def load_species():
    """Create the Linked List and append all 20 species to it."""
    species_list = LinkedList()
    for row in _RAW:
        data = dict(zip(KEYS, row))
        # Put a photo named like the species in static/images/ (e.g. neem.jpg).
        # If the file is missing, the page shows the emoji tile instead.
        data["image"] = "/static/images/" + data["name"].lower().replace(" ", "_") + ".jpg"
        species_list.append(data)
    return species_list
