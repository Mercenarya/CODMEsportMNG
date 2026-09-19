import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["dohona"]
# collection = db.create_collection("users")
# print(client.list_database_names())
# print(db.list_collection_names())


def list_collections():
    try:
        collections = db.list_collection_names()
        print(f"[INFO] Collections in database '{db.name}': {collections}")
        return collections
    except Exception as e:
        print(f"[ERROR] Failed to list collections: {str(e)}")
        return []
    
def insert_data(data:dict):
    try:
        pass
    except Exception as error:
        return error
    

def drop_data(name:str):
    try:
        data = db.list_collection_names()
        
        if name in data:
            db.drop_collection(name)
            print(f"[SUCCESS] Dropped collection: {name}")
       
    except Exception as e:
        print(f"[ERROR] Failed to drop collection {name}: {str(e)}")
        
        
if __name__ == "__main__":
    
    data_records = {
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    
    
    
    list_collections()
    drop_data("users")