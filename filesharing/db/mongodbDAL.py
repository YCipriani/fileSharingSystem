from pymongo import MongoClient


class mongodbDAL:
    def __init__(self, db_name):
        self.connection_string = "mongodb+srv://ycipriani:1212@cluster0.ey0sv.mongodb.net/Tx?retryWrites=true&w=majority"
        self.client = MongoClient(self.connection_string)
        self.db = self.client[db_name]
        self.collection_names = self.db.list_collection_names()

    def find_file_by_collection(self, file_name: str, file_location: str) -> bool:
        collection = self.db.get_collection(file_location).find()
        for item in collection:
            if file_name == item["file_name"]:
                return True
        return False

    def find_file_in_collection(self, file_name) -> bool:
        for collection_name in self.collection_names:
            collection = self.db.get_collection(collection_name).find()
            for item in collection:
                if file_name == item["file_name"]:
                    return True
        return False

    def move_file(self, file_name, old_location, new_location):
        if self.find_file_by_collection(file_name, old_location):
            old_collection = self.db.get_collection(old_location)
            old_collection.delete_one({'file_name': file_name})
            new_collection = self.db.get_collection(new_location)
            new_collection.insert_one({'file_name': file_name, 'file_location': new_location})
