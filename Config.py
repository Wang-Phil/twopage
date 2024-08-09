import configparser
import json


class Config:

    @staticmethod
    def get_api_key():
        config = configparser.ConfigParser()
        config.read("config.ini",encoding='utf-8')
        api_key = config.get('DEFAULT', 'api_key')
        print(api_key)
        return api_key

    @staticmethod
    def get_app_list():
        config = configparser.ConfigParser()
        config.read("config.ini",encoding='utf-8')
        data = config.get('DEFAULT', 'app_list')
        app_list = json.loads(data)
        return app_list

    @staticmethod
    def get_local_model():
        config = configparser.ConfigParser()
        config.read("config.ini",encoding='utf-8')
        local_model = config.get('DEFAULT', 'local_model')
        # print(local_model)
        return local_model

    @staticmethod
    def get_ALIBABA_CLOUD_ACCESS_KEY_ID():
        config = configparser.ConfigParser()
        config.read("config.ini",encoding='utf-8')
        access_key_id = config.get('DEFAULT', 'access_key_id')
        # print(local_model)
        return access_key_id

    @staticmethod
    def get_ALIBABA_CLOUD_ACCESS_KEY_SECRET():
        config = configparser.ConfigParser()
        config.read("config.ini",encoding='utf-8')
        access_key_secret = config.get('DEFAULT', 'access_key_secret')
        # print(local_model)
        return access_key_secret

    @staticmethod
    def get_app_key():
        config = configparser.ConfigParser()
        config.read("config.ini",encoding='utf-8')
        app_key = config.get('DEFAULT', 'app_key')
        # print(local_model)
        return app_key

    import configparser

    @staticmethod
    def set_api_key(api_key):
        try:
            config = configparser.ConfigParser()
            with open("config.ini", "r", encoding="utf-8") as configfile:
                config.read_file(configfile)
            config.set('DEFAULT', 'api_key', api_key)
            with open("config.ini", "w", encoding="utf-8") as configfile:
                config.write(configfile)
            return True
        except Exception as e:
            print(f"Failed to set API Key: {e}")
            return False

    @staticmethod
    def set_app_key(app_key):
        try:
            config = configparser.ConfigParser()
            with open("config.ini", "r", encoding="utf-8") as configfile:
                config.read_file(configfile)
            config.set('DEFAULT', 'app_key', app_key)
            with open("config.ini", "w", encoding="utf-8") as configfile:
                config.write(configfile)
            return True
        except Exception as e:
            print(f"Failed to set App Key: {e}")
            return False

    @staticmethod
    def set_ALIBABA_CLOUD_ACCESS_KEY_ID(access_key_id):
        try:
            config = configparser.ConfigParser()
            with open("config.ini", "r", encoding="utf-8") as configfile:
                config.read_file(configfile)
            config.set('DEFAULT', 'access_key_id', access_key_id)
            with open("config.ini", "w", encoding="utf-8") as configfile:
                config.write(configfile)
            return True
        except Exception as e:
            print(f"Failed to set Alibaba Cloud Access Key ID: {e}")
            return False

    @staticmethod
    def set_ALIBABA_CLOUD_ACCESS_KEY_SECRET(access_key_secret):
        try:
            config = configparser.ConfigParser()
            with open("config.ini", "r", encoding="utf-8") as configfile:
                config.read_file(configfile)
            config.set('DEFAULT', 'access_key_secret', access_key_secret)
            with open("config.ini", "w", encoding="utf-8") as configfile:
                config.write(configfile)
            return True
        except Exception as e:
            print(f"Failed to set Alibaba Cloud Access Key Secret: {e}")
            return False
