from models.Base import Base


class Product(Base):
    def __init__(self, df):
        super().__init__(df)

    def get_brand_id_mapping(self, brand):
        """
        Creates a mapping between product IDs and brand IDs by merging product and brand dataframes
        Args:
            brand: Brand object containing brand information
        Returns:
            DataFrame with product_id and brand_id columns
        """
        return (
            self.df.merge(
                brand.df,
                left_on='brand',
                right_on='name'
            )[['id_x', 'id_y']]
            .rename(columns={
                'id_x': 'product_id',
                'id_y': 'brand_id'
            })
        )