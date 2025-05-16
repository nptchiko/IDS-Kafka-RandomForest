import hashlib
import json


class SocketService:
    previous_hash = None

    previous_ids = {
        "status_info": set(),
    }

    @staticmethod
    def genarateHashValue(inputData):
        string_data = json.dumps(inputData, sort_keys=True)
        return hashlib.sha256(string_data.encode()).hexdigest()

    @classmethod
    def is_data_changed(cls, new_data):
        new_hash = cls.genarateHashValue(new_data)

        if new_hash != cls.previous_hash:
            cls.previous_hash = new_hash
            return True

        return False

    @staticmethod
    def extract_new_records(collection_name, current_data):
        # Get current dictionary
        current_ids = set(str(doc["_id"]) for doc in current_data)

        # Compare previous data
        old_ids = SocketService.previous_ids.get(collection_name, set())
        new_ids = current_ids - old_ids

        # Update dictionary previous id
        SocketService.previous_ids[collection_name] = current_ids

        # Return new data
        return [doc for doc in current_data if str(doc["_id"]) in new_ids]
    
    @staticmethod
    def extract_data_from_db(status_data):
        newest_info = status_data[len(status_data)-1]
        return newest_info
