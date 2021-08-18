from pymongo import MongoClient
from filesharing.common.globals import dummy_file, extensions
from random import randrange, randint

COUNT = randint(0, 92233720368)


class mongodbDAL:
    def __init__(self, db_name):
        self.connection_string = "mongodb+srv://ycipriani:1212@cluster0.ey0sv.mongodb.net/Tx?retryWrites=true&w=majority"
        self.client = MongoClient(self.connection_string)
        self.db = self.client[db_name]
        self.collection_names = self.db.list_collection_names()
        self.list_of_files_to_send = []

    def find_file_by_collection(self, file_name: str, file_location: str) -> bool:
        collection = self.db.get_collection(file_location).find()
        for item in collection:
            if file_name == item["file_name"]:
                print("FOUND")
                return True
        print("NOT FOUND")
        return False

    def find_file_in_collection(self, file_name) -> bool:
        for collection_name in self.collection_names:
            collection = self.db.get_collection(collection_name).find()
            for item in collection:
                if file_name == item["file_name"]:
                    return True
        return False

    def add_files_to_collection(self, collection_name):
        collection = self.db.get_collection(collection_name)
        collection.insert_many(self.list_of_files_to_send)
        self.list_of_files_to_send = []

    def add_dummy_file_to_file_list(self, collection_name):
        dummy_file['file_name'] = dummy_file['file_name'].split('.')[0] + str(COUNT) + extensions[
            randrange(len(extensions))]
        dummy_file['file_location'] = collection_name
        self.list_of_files_to_send.append(dummy_file)
