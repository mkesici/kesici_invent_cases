class Features:
    def __init__(self, p_features, b_features, s_features):
        self.p_features = p_features
        self.b_features = b_features 
        self.s_features = s_features

    def form_features(self):
        return (
            self.p_features.df
            .sort_values(['product', 'store', 'date'])
            .merge(
                self.b_features.df,
                on=['brand', 'store', 'date'],
                how='left'
            ).rename(
                columns={'quantity_x': 'sales_product', 'quantity_y': 'sales_brand'}
            ).merge(
                self.s_features.df,
                on=['store', 'date'],
                how='left'
            ).rename(
                columns={'quantity': 'sales_store'}
            ).rename(
                columns={'product': 'product_id', 'brand': 'brand_id', 'store': 'store_id'}
            )
        )