from sqlalchemy import Column, Integer

class StatsMixin(object):
    mistakes = Column(Integer)
    corrects = Column(Integer)

    @property
    def totalCount(self):
        return self.mistakes + self.corrects

    @property
    def mistakeRatio(self):
        if not self.totalCount:
            return None
        return self.mistakes / self.totalCount

    @property
    def correctRatio(self):
        if not self.totalCount:
            return None
        return self.corrects / self.totalCount
