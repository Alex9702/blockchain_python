class Printable:
    ''' A class which implements printing functionality.'''
    def __repr__(self):
        return str(self.__dict__)