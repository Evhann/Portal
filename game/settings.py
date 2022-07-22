import json, os.path

game_path = os.path.dirname(os.path.abspath(__file__))

with open(game_path+"/user/settings.json", "r", encoding="utf-8") as settings_file:
    class SETTINGS:
        SETTINGS_AS_JSON = json.load(settings_file)

    def add_attrs_to_settings(cls, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(cls, key, SETTINGS())
                add_attrs_to_settings(getattr(cls, key), value)
            else:
                setattr(cls, key, value)
    add_attrs_to_settings(SETTINGS, SETTINGS.SETTINGS_AS_JSON)
    del add_attrs_to_settings