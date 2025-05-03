import pandas as pd

from q5.models.Base import Base


class Sale(Base):
    def __init__(self, df):
        super().__init__(df)


    def create_full_init_df(self, min_date, max_date):
        """
        Creates a complete dataframe with all combinations of products, stores and dates in the given date range so while calculating MA and LAG there will be no miss.
        
        Args:
            min_date (str): Start date of the range in YYYY-MM-DD format
            max_date (str): End date of the range in YYYY-MM-DD format
            
        Returns:
            Sale: A new Sale object containing the complete dataframe with all dates
            
        The function:
        1. Creates a date range from min_date to max_date
        2. Gets unique products and stores
        3. Creates a MultiIndex with all possible combinations
        4. Reindexes the original dataframe to include all combinations
        """
        df_copy = self.df.copy()

        # Group by product, store and date to aggregate quantities, in case there are multiple entries for same combination
        # This procedure may change depending on the source data processing types.
        df_copy = df_copy.groupby(['product', 'store', 'date'])['quantity'].sum().reset_index()

        df_copy['date'] = pd.to_datetime(df_copy['date'])
        
        products = df_copy['product'].unique()
        stores = df_copy['store'].unique()
        date_range = pd.date_range(min_date, max_date)

        full_index = pd.MultiIndex.from_product(
            [products, stores, date_range],
            names=['product', 'store', 'date']
        )
        
        df_copy = (
                    df_copy
                         .set_index(['product', 'store', 'date'])
                         .reindex(full_index)
                         .fillna({'quantity': 0}) # Since the data is a sale data filling with 0 is more appropriate
                   )

        df_copy.reset_index(inplace=True)
        
        return Sale(df_copy)

    def calculate_MAP_and_LAG(self, group_cols, ref_value, map_col, lag_col) :
        """
        Calculate MAP (Moving Average Price) and LAG (Lagged Sales) columns grouped by group_col
        Args:
            group_cols: Column name to group by
            ref_value: Column name containing the values to calculate MAP and LAG from
            map_col: Name of the new column to store MAP values
            lag_col: Name of the new column to store LAG values
        Returns:
            New Sale object with MAP and LAG columns added
        """

        df_copy = self.df.copy()

        df_copy = df_copy.groupby(group_cols + ['date'])[ref_value].sum().reset_index()

        df_copy[map_col] = df_copy.groupby(group_cols)[ref_value].transform(lambda x: x.rolling(window=7, min_periods=1).mean())

        df_copy[lag_col] = df_copy.groupby(group_cols)[ref_value].shift(7)

        return Sale(df_copy)

    def merge_brand_id(self, product_brand_mapping):
        """
        Merges brand IDs from product-brand mapping into the sales dataframe.

        Args:
            product_brand_mapping (pd.DataFrame): DataFrame containing product_id to brand_id mapping

        Returns:
            Sale: A new Sale object with brand IDs merged into the dataframe
            
        The function:
        1. Merges the sales data with product-brand mapping on product ID
        2. Drops redundant product_id column from the merge
        3. Renames brand_id column to brand for consistency
        """
        df_copy = self.df.copy()

        df_copy = (
                    df_copy
                       .merge(
                            product_brand_mapping,
                            left_on = 'product',
                            right_on = 'product_id',
                        )
                       .drop("product_id", axis=1)
                       .rename(columns={'brand_id': 'brand'})
                   )

        return Sale(df_copy)