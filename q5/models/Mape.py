from q5.models.Base import Base


class Mape(Base):
    def __init__(self, df):
        super().__init__(df)

    def calculate(self, top):
        df_copy = self.df.copy()
        df_copy['diff'] = (df_copy['quantity'] - df_copy['MA7_P']).abs()
        df_copy = (
                df_copy
                    .groupby(['product', 'store', 'brand'])
                    .apply(lambda group: group['diff'].sum() / group['quantity'].sum() if group['quantity'].sum() != 0 else None)
                    .reset_index(name='WMAPE')
                    .sort_values(['WMAPE'], ascending=False)
                    .reset_index(drop=True)
                    .head(top)
                )

        return df_copy