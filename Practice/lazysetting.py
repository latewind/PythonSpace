class LazySetting():
    def __init__(self):
        pass

    def __getattr__(self, item):
        print("getArrt")



setting = LazySetting()
