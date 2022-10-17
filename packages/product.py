class Product:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        print("Product created")

    def to_dict(self):
        return {self.uid: {"name": self.name}}