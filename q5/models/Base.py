import pandas as pd


class Base:
    def __init__(self, df):
        self.df = df

    @classmethod
    def from_csv(cls, filename):
        df = pd.read_csv(filename)
        return cls(df)

    def to_csv(self, filename):
        self.df.to_csv(filename)