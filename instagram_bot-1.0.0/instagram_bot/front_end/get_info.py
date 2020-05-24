#!/usr/bin/python3.8



class JavaScriptObject(dict):
    
    def __getattribute__(self, item):
        try:
            try:
                if self[item]:
                    return self[item]
            except KeyError:
                return super().__getattribute__(item)
        except AttributeError:
            return f"Java script object has no attribute {item}"






