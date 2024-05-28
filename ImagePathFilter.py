import os
import json
import logging
from Utils import Utils


class ImagePathFilter:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.SET_YEAR = self.config.get("SCHEDULE_TIME", {}).get("SET_YEAR")
        self.SET_MONTH = self.config.get("SCHEDULE_TIME", {}).get("SET_MONTH")
        self.SET_DAY = self.config.get("SCHEDULE_TIME", {}).get("SET_DAY")
        self.SET_HOUR = self.config.get("SCHEDULE_TIME", {}).get("SET_HOUR")

    def load_config(self, config_path):
        try:
            return Utils.load_config_file(config_path)
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            logging.error(f"Error loading configuration: {e}")
            return {}

    def filter_image_paths(self, folder_path, filter_func):
        try:
            results = Utils.GetAllImageDate(folder_path)
            return [list(result.keys())[0] for result in results if filter_func(result)]
        except Exception as e:
            logging.error(f"Error filtering image paths: {e}")
            return []

    @staticmethod
    def size_filter(path):
        try:
            return os.path.getsize(path) > 1 * 1024 * 1024
        except Exception as e:
            logging.error(f"Error in size_filter: {e}")
            return False

    def time_filter(self, image_data):
        try:
            if not image_data:
                return False

            values = list(image_data.values())[0]
            key = list(image_data.keys())[0]

            if int(values["year"]) > self.SET_YEAR:
                return key
            elif int(values["year"]) == self.SET_YEAR:
                if int(values["month"]) > self.SET_MONTH:
                    return key
                elif int(values["month"]) == self.SET_MONTH:
                    if int(values["day"]) > self.SET_DAY:
                        return key
                    elif int(values["day"]) == self.SET_DAY:
                        if int(values["hour"]) >= self.SET_HOUR:
                            return key
            return False
        except Exception as e:
            logging.error(f"Error in time_filter: {e}")
            return False

    def filter_image(self, folder_path, filter_func=True):
        img_paths = []
        if filter_func:
            img_path_filters = self.filter_image_paths(folder_path, filter_func=self.time_filter)
        else:
            img_path_filters = os.listdir(folder_path)

        for img_path_filter in img_path_filters:
            if os.name == 'nt':  # Windows
                img_paths.append(f"{folder_path}\\{img_path_filter}")
            else:  # Unix/Linux
                img_paths.append(f"{folder_path}/{img_path_filter}")

        return img_paths

