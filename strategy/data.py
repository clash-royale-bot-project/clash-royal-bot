# todo https://github.com/PirateIncognito/ClashRoyale-unit-data-CSV ?

units_price = {'knight': 3,
               'archers': 3,
               'goblins': 2,
               'giant': 5,
               'pekka': 7,
               'minion': 3,
               'balloon': 5,
               'witch': 5,
               'barbarians': 5,
               'golem': 8,
               'skeletons': 1,
               'valkyrie': 4,
               'skeleton_horde': 3,
               'bomber': 3,
               'musketeer': 4,
               'baby_dragon': 4,
               'prince': 5,
               'wizard': 5,
               'mini_pekka': 4,
               'goblin_archer': 2,
               'giant_skeleton': 6,
               'hog_rider': 4,
               'minion_horde': 5,
               'ice_wizard': 3,
               'royal_giant': 6,
               'skeleton_warriors': 3,
               'princess': 3,
               'dark_prince': 4,
               'three_musketeers': 9,
               'lava_hound': 7,
               'snow_spirits': 1,
               'fire_spirits': 2,
               'miner': 3,
               'zapMachine': 6,
               'bowler': 5,
               'rage_barbarian': 4,
               'battle_ram': 4,
               'inferno_dragon': 4,
               'ice_golem': 2,
               'mega_minion': 3,
               'blowdart_goblin': 3,
               'goblin_gang': 3,
               'electro_wizard': 4,
               'angry_barbarian': 6,
               'hunter': 4,
               'executioner': 5,
               'bandit': 3,
               'dark_witch': 4,
               'bats': 2,
               'ghost': 3,
               'zappies': 4,
               'cannon_cart': 5,
               'mega_knight': 7,
               'skeleton_balloon': 3,
               'flying_machine': 4,
               'magic_archer': 4}

builds_price = {
    'chaos_cannon': 3,
    'fire_furnace': 5,
    'building_mortar': 4,
    'building_inferno': 5,
    'bomb_tower': 5,
    'barbarian_hut': 7,
    'building_tesla': 4,
    'building_elixir_collector': 6,
    'building_xbow': 6,
    'tombstone': 3,
    'firespirit_hut': 4
}

spells_price = {
    'fireball': 4,
    'arrows': 3,
    'rage': 2,
    'rocket': 6,
    'goblin_barrel': 3,
    'freeze': 4,
    'mirror': 1,
    'lightning': 6,
    'zap': 2,
    'poison': 4,
    'graveyard': 5,
    'log': 2,
    'tornado': 3,
    'clone': 3,
    'barb_barrel': 3,
    'heal': 3
}

def unit_type(name):
    if name in units_price:
        return 'unit'
    elif name in builds_price:
        return 'build'
    elif name in spells_price:
        return 'spell'
    else:
        return None

cards_price = {**units_price, **builds_price, **spells_price}