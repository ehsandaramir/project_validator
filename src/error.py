
class Error:

    def __init__(self, category: str, sub_category: str, source: str, message: str=None):
        self.category = category
        self.sub_category = sub_category
        self.source = source
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'Error<{}::{}: {}>'.format(self.category, self.sub_category, self.source)
        else:
            return 'Error<{}::{}: {}\n\tmessage: {}>'.format(self.category, self.sub_category, self.source, self.message)

    def __repr__(self):
        return self.__str__()
