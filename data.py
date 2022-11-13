class UserInfo():
    surname = ''
    name = ''
    lastname = ''
    mail = ''
    phone = ''


class Data():
    phone = 0
    code = 0
    
    map_lon = 0
    map_lat = 0
    
    search_object = {}
    parse_list = []
    
    request = ''

    input_surname = ''
    input_name = ''
    input_lastname = ''
    input_mail = ''
    input_phone = 0

    number_rule = 0
    number_penalties = 0

    stateMap = 'Street'
    screen_history = []
    parse_list = []
    
    polygon_text = None
    is_polygon = False
    urlToPenalti = ""
    fish_number = 0
    
    map_src = True
    satellite_src = True
    hybrid_src = True
    
    data_fish = None
    data_weapons = None
    data_base_chill = None
    data_equipment = None
    data_bait = None
    data_buy_fish = None
    data_fishing_disallowed = None
    data_user = None
    data_recipe = None
    fish_catalog_name = None
    fish_name = None
    base_chill_name = None
    equipment_name = None
    bait_name = None
    buy_fish_name = None
    recipe_name = None
    object_map_lon = None
    object_map_lat = None

    db = []

    def save_info(self, surname, name, lastname, mail, phone):
        try:
            input_phone = int(phone)
        except:
            pass
        finally:
            input_phone = ''
        self.input_surname = surname
        self.input_name = name
        self.input_lastname = lastname
        self.input_mail = mail
        self.input_phone = input_phone

user_info = UserInfo()
