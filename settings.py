import uuid

class Settings():

    def __init__(self):

        # uuid filename
        self.__uuid_file_name = "uuid.txt"
        self.uuid = self.get_uuid()
        # Size of the board
        self.rows = 8
        self.cols = 8

        # Amount and length of ships
        self.shiplist = {
            'Aircraft Carrier' : 1,
            'Battle Ship' : 1,
            'Cruiser' : 1,
            'Destroyer' : 2,
            'Submarine' : 2
            }
        self.shiplength = {
            'Aircraft Carrier' : 5,
            'Battle Ship' : 4,
            'Cruiser' : 3,
            'Destroyer' : 2,
            'Submarine' : 1
            }

    def get_uuid(self):
        
        return str(uuid.uuid4())
        
        #try:
        #    with open(self.__uuid_file_name) as f:
        #        uuidhash = f.read()
        #except FileNotFoundError:
        #    new_uuid = str(uuid.uuid4())
        #    with open(self.__uuid_file_name, 'w') as f:
        #        f.write(new_uuid)
        #    print("uuid file created")
        #    uuidhash = new_uuid
        #else:
        #    print("uuid read from file")
        #return uuidhash
