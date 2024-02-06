import os

# currently as constant, will be some kind of import from disk or config file eventually
MAP_IDENTIFIERS_EXISTENCE = {
    "Space_Borg_Battleship_Raidisode_Sibrian_Elite_Initial": "Infected_Space_Elite",
    "Space_Borg_Dreadnought_Raidisode_Sibrian_Final_Boss": "Infected_Space",
    "Mission_Space_Romulan_Colony_Flagship_Lleiset": "Azure_Nebula",
    "Space_Klingon_Dreadnought_Dsc_Sarcophagus": "Battle_At_The_Binary_Stars",
    "Event_Procyon_5_Queue_Krenim_Dreadnaught_Annorax": "Battle_At_Procyon_V",
    "Mission_Space_Borg_Queen_Diamond_Brg_Queue_Liberation": "Borg_Disconnected",
    "Mission_Starbase_Mirror_Ds9_Mu_Queue": "Counterpoint",
    "Space_Crystalline_Entity_2018": "Crystalline_Entity",
    "Event_Ico_Qonos_Space_Herald_Dreadnaught": "Gateway_To_Grethor",
    "Mission_Space_Federation_Science_Herald_Sphere": "Herald_Sphere",
    "Msn_Dsc_Priors_System_Tfo_Orbital_Platform_1_Fed_Dsc": "Operation_Riposte",
    "Space_Borg_Dreadnought_R02": "Cure_Found",
    "Space_Klingon_Tos_X3_Battlecruiser": "Days_Of_Doom",
    "Msn_Luk_Colony_Dranuur_Queue_System_Upgradeable_Satellite": "Dranuur_Gauntlet",
    "Space_Borg_Dreadnought_Raidisode_Khitomer_Intro_Boss": "Khitomer_Space",
    "Mission_Spire_Space_Voth_Frigate": "Storming_The_Spire",
    "Space_Drantzuli_Alpha_Battleship": "Swarm",
    "Mission_Beta_Lankal_Destructible_Reactor": "To_Hell_With_Honor",
    "Space_Federation_Dreadnought_Jupiter_Class_Carrier": "Gravity_Kills",
    "Msn_Luk_Hypermass_Queue_System_Tzk_Protomatter_Facility": "Gravity_Kills",
    "Space_Borg_Dreadnought_Hive_Intro": "Hive_Space",
    "Mission_Space_Borg_Battleship_Queen_1_0f_2": "Hive_Space",
    "Msn_Kcw_Rura_Penthe_System_Tfo_Dilithium_Hauler": "Best_Served_Cold",
    "Ground_Federation_Capt_Mirror_Runabout_Tfo": "Operation_Wolf"
    }

def get_combat_log_data(path:str):
    if not (os.path.exists(path) and os.path.isfile(path)):
        raise FileNotFoundError(f'Invalid Path: {path}')
    lines_list = list()
    with open(path, 'r', encoding='utf-8') as file:
        lines_list = file.readlines()
    if len(lines_list) < 1 or not lines_list[0].strip():
        raise TypeError('File must contain at least one not-empty line')
    if not '::' in lines_list[0] or not ',' in lines_list[0]:
        raise TypeError("First line invalid. First line may not be empty and must contain '::' and ','.")
    return lines_list