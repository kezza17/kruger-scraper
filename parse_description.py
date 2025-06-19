import re
from text_utils import find_phrase

activities = {
    "otm": ["on the move with kill", "otm", "on the move", "moving", "on the moove", "on the mpve"],
    "mating": ["mating"],
    "kill": ["in a tree with kill", "eating a kill", "on a kill", "with kill"],
    "in a tree": ["stationary in a tree","in a tree", "back in tree"],
    "stat": ["stationary", "stat", "resting", "lying down"],
    "hunting": ["hunting", "chasing"],
    "grazing": ["grazing"],
    "feeding": ["feeding in a tree", "eating", "feeding"],
    "crossed road": ["crossed the road", "crossed road", "crosssed road", "crosse road", "crossing road"],
    "sleeping": ["sleeping"],
    "flying": ["flying"],
    "swimming": ["swimming"],
    "drinking": ["drinking", "drining"],
    "running": ["running"],
    "playing": ["playing"],
    "fighting": ["fighting"],
    "bathing": ["bathing"],
    "blocking road": ["blocking road", "roadblock", "blocking the road", "causing a roadblock"],
    "courting": ["courting"],
    "fishing": ["fishing"],
    "marking territory": ["marking territory"],
    "scratching": ["scratching"],
    "suckling": ["suckling"],
    "in river bed": ["in the river bed"],
    "singing": ["singing"],
    "injured": ["injured"],
    "calling": ["calling"],
    "browsing": ["browsing", "browzing"],
    "carcass": ["carcass"],
    "chilling": ["chilling"],
    "crossing the river": ["crossing the river"],
    "moved off": ["moved off"],
    "foraging": ["foraging"]
}

species = {
    "tortoise": ["leopard tortoise", "tortoise"],
    "leopard": ["leopard cubs", "leopards", "leopard", "leiopard"],
    "hyena": ["spotted hyenas", "spotted hyena", "sppotted hyena" "hyenas", "hyena"],
    "lion": ["lions", "lion"],
    "elephant": ["elephants", "elephant", "elephannt"],
    "wild dog": ["wild dogs", "wild dog"],
    "cheetah": ["cheetah cubs", "cheetahs", "cheetah", "chetah"],
    "buffalo": ["buffaloes", "buffalos", "buffalo", "bufalo", "bufffalo"],
    "giraffe": ["giraffes", "giraffe"],
    "caracal": ["caracals", "caracal"],
    "zebra": ["burchells zebra", "burchell zebra" 'zebra'],
    "impala": ["impalas", "impala"],
    "side striped jackal": ["side striped jackals", "side striped jackal"],
    "black backed jackal": ["black backed jackals", "black backed jackal", "balck backed jackal", "black backek jackal", "black backed jacka" "jackals", "jackal"],
    "warthog": ["warthogs", "warthog"],
    "hippo": ["hippopotami", "hippos", "hippo", "hippopotamus"],
    "southern ground hornbill": ["southern ground hornbills", "southern ground hornbill", "ground hornbill"],
    "tawny eagle": ["tawny eagles", "tawny eagle"],
    "black chested snake eagle": ["black chested snake eagle"],
    "brown snake eagle": ["brown snake eagle", "snake eagle"],
    "martial eagle": ["martial eagles", "martial eagle"],
    "crowned eagle": ["african crowned eagle", "crowned eagle"],
    "african fish eagle": ["african fish eagles", "african fish eagle", "fish eagle"],
    "water monitor": ["water monitor", "monitor lizard"],
    "verreaux's eagle-owl": ["verreauxs eagle owls", "verreauxs eagle owl"],
    "saddle billed stork": ["saddle billed storks", "saddle billed stork"],
    "tsessebe": ["tsessebe"],
    "white backed vulture": ["white backed vultures", "white backed vulture"],
    "white headed vulture": ["white headed vultures", "white headed vulture"],
    "cape vulture": ["cape vultures", "cape vulture"],
    "african fish eagle": ["african fish eagle"],
    "bateleur": ["bateleurs", "bateleur", "bateluer"],
    "african finfoot": ["african finfoot"],
    "african wild cat": ["african wild cat"],
    "pangolin": ["pangolin"],
    "honey badger": ["honey badgers", "honey badger"],
    "brown headed parrot": ["brown headed parrot"],
    "klipspringer": ["klipsprngers", "klipspringer"],
    "small spotted genet": ["small spotted genet"],
    "sable antelope": ["sable antelope"],
    "stripe-bellied sand snake": ["stripe bellied sand snake"],
    "spotted bush snake": ["spotted bush snake"],
    "eland": ["elands", "eland"],
    "baboon": ["chacma baboon", "chacma baboons", "baboons", "baboon"],
    "crocodile": ["crocodiles", "crocodile", "crocodle"],
    "roan antelope": ["roan antelope"],
    "kori bustards": ["kori bustards", "kori bustard"],
    "secretary bird": ["secretary birds", "secretary bird"],
    "red-crested korhaan": ["red crested korhaans", "red crested korhaan"],
    "common reedbuck": ["common reedbucks", "common reedbuck"],
    "dwarf mongoose": ["dwarf mongoose"],
    "civet": ["african civet", "civet"],
    "african harrier hawk": ["african harrier hawks", "african harrier hawk", "gymnogene"],
    "african hawk eagle": ["african hawk eagle", "african hark eagle"],
    "african skimmer": ["african skimmer"],
    "banded mongoose": ["banded mongoose"],
    "barbels": ["barbels"],
    "southern carmine bee eater": ["southern carmine bee-eater", "carmine bee eater"],
    "white fronted bee eater": ["white fronted bee eater"],
    "black mamba": ["black mamba"],
    "black winged kite": ["black winged kite"],
    "cape clawless otter": ["cape clawless otter"],
    "chameleon": ["flap necked chameleon", "chameleon"],
    "common ostrich": ["common ostrichs", "common ostrich", "ostriches", "ostrich"],
    "crowned plover": ["crowned plover"],
    "dark chanting goshawk": ["dark chanting goshawk"],
    "eagle": ["eagles", "eagle"],
    "european roller": ["european roller"],
    "village indigobird": ["village indigobird"],
    "giant kingfisher": ["giant kingfishers", "giant kingfisher"],
    "woodland kingfisher": ["woodland kingfisher"],
    "pied kingfisher": ["pied kingfisher"],
    "giant african snail": ["giant african snail"],
    "giant legless skink": ["giant legless skink"],
    "giant plated lizard": ["giant plated lizard"],
    "kudu": ["kudu"],
    "grey heron": ["grey heron"],
    "large spotted genet": ["large spotted genet"],
    "lilac breasted roller": ["lilac breasted roller", "roller"],
    "marabou stork": ["marabou storks", "marabou stork"],
    "mozambique spitting cobra": ["mozambique spitting cobra"],
    "nyala": ["nyala"],
    "osprey": ["osprey"],
    "puff adder": ["puff adder"],
    "southern african rock python": ["southern african rock python", "african rock python", "python"],
    "rock monitor": ["rock monitor"],
    "scrub hare": ["scrub hare"],
    "serval": ["serval"],
    "hinged terrapin": ["hinged terrapins", "hinged terrapin", "terrapin"],
    "trumpeter hornbill": ["trumpeter hornbill"],
    "waterbuck": ["waterbucks", "waterbuck"],
    "aardvark": ["aardvark", "advaark"],
    "african scops owl": ["african scops owl"],
    "african barred owlet": ["african barred owlette", "african barred owlet", "african barred owl"],
    "african bullfrog": ["african bullfrog"],
    "african comb duck": ["comb ducks", "african comb duck"],
    "african darter": ["african darter", "darter"],
    "african green pigeon": ["african green pigeon"],
    "african grey hornbill": ["african grey hornbill"],
    "african hoopoe": ["african hoopoe"],
    "african openbill": ["african openbills", "african openbill"],
    "african pied wagtail": ["african pied wagtail"],
    "african stonechat": ["african stonechat"],
    "bearded woodpecker": ["bearded woodpecker"],
    "bibron's blind snake": ["bibrons blind snake"],
    "black heron": ["black heron"],
    "black bellied bustard": ["black bellied bustard"],
    "blacksmith lapwing": ["blacksmith lapwing"],
    "blue waxbill": ["blue waxbill"],
    "blue wildebeest": ["blue wildebeests", "blue wildebeest", "blue wildbeest", "wildebeest"],
    "boomslang": ["boomslang"],
    "brown hooded kingfisher": ["brown hooded kingfisher"],
    "bush babies": ["bush babies", "bush baby", "bushbaby"],
    "bushbuck": ["bushbuck"],
    "common duiker": ["common duiker"],
    "burchell's coucal": ["burchells coucal", "coucal"],
    "collared sunbird": ["collared sunbird"],
    "fruit bat": ["peters epauletted fruit bat"],
    "common flat lizard": ["common flat lizard"],
    "common slender mongoose": ["common slender mongoose"],
    "crested barbet": ["crested barbet"],
    "crested francolin": ["crested francolin"],
    "crested guineafowl": ["crested guinea fowl", "crested guineafowl"],
    "crowned hornbill": ["crowned hornbill"],
    "double banded sandgrouse": ["double banded sandgrouses", "double banded sandgrouse"],
    "dung beetle": ["dung beetles", "dung beetle"],
    "dwarf bittern": ["dwarf bitterns", "dwarf bittern"],
    "eastern natal green snake": ["eastern natal green snake"],
    "egyptian goose": ["egyptian geese", "egyptian goose"],
    "european bee eater": ["european bee eater"],
    "european honey buzzard": ["european honey buzzard"],


    "kingfisher": ["kingfisher"],
    "snake": ["snake"],
    "heron": ["heron"],
    "mongoose": ["mongoose"],
    "guineafowl": ["guineafowl"],
    "cobra": ["cobra"],
    "vulture": ["vultures", "vulture"],
    "bee eater": ["bee eater"],
    "duiker": ["duiker"],
    "genet": ["genet"]
    
    # Add more as needed
}

quantities = {
    "2": ["two", "pair", "duo", "couple of"],
    "3": ["three"],
    "multiple": [
        "group of", 
        "clan of", 
        "pack of", 
        "big pride of",
        "pride of", 
        "breeding herd of",
        "a massive herd of",
        "a small herd of",
        "a huge herd of",
        "a big herd of",  
        "extremely large herd of",
        "a large herd of", 
        "massive herd of",
        "small herd of",
        "huge herd of",
        "big herd of",
        "herds of",  
        "large herd of", 
        "herd of",
        "pod of",
        "crowd of",
        "tower of", 
        "flock of",
        "chan of",
        "coalition of",
        "coalitiion of",
        "committee of",
        "comittee of",
        "congregation of",
        "journey of"
        "family of",
        "float of",
        "colony of"
        "confusion of",
        "some",
        "wake of",
        "a few",
        "a lot of",
        "a mustering of",
        "a streak of",
        "bask of"
    ],
    "1": ["one", "single", "another", "beautiful", "huge male", "juvenile", "male", "adult"],
    # Extend for other group sizes
}

def extract_description_fields(description):
    original = description
    desc = description.lower()
    matched = {"quantity": None, "species": None, "activity": None}
    unmatched = []

    # 1. Quantity: handle "X plus" -> "X+" first
    plus_match = re.search(r'\b(\d+)\s+plus\b', desc, re.IGNORECASE)
    if plus_match:
        raw_number = plus_match.group(1)
        matched["quantity"] = raw_number + "+"
        desc = desc.replace(plus_match.group(0), "")
    else:
        # Now fallback to number or defined quantity phrases
        quantity_match = re.search(r'\b\d+\+?\b', desc)
        if quantity_match:
            matched["quantity"] = quantity_match.group()
            desc = desc.replace(matched["quantity"], "")
        else:
            key, phrase = find_phrase(quantities, desc)
            if key:
                matched["quantity"] = key
                desc = desc.replace(phrase, "")

    # 2. Species
    key, phrase = find_phrase(species, desc)
    if key:
        matched["species"] = key
        desc = desc.replace(phrase, "")

    # 3. Activity
    key, phrase = find_phrase(activities, desc)
    if key:
        matched["activity"] = key
        desc = desc.replace(phrase, "")

    # 4. Remaining unknown tokens
    words_left = desc.strip().replace(",", "").split()
    unmatched = [w for w in words_left if w.strip()]

    return {
        "value": original,
        "quantity": matched["quantity"],
        "species": matched["species"],
        "activity": matched["activity"],
        "unknown": unmatched
    }