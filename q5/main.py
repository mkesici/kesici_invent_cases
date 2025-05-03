from q5.models.Features import Features
from q5.models.Brand import Brand
from q5.models.Mape import Mape
from q5.models.Product import Product
from q5.models.Sale import Sale
from q5.helper import parse_args


if __name__ == '__main__':
    args = parse_args()

    base_sales = Sale.from_csv("src/sales.csv")
    full_date_sales = base_sales.create_full_init_df(args.min_date, args.max_date)

    product_brand_mapping = Product.from_csv("src/product.csv").get_brand_id_mapping(Brand.from_csv("src/brand.csv"))
    full_date_sales_with_brand = full_date_sales.merge_brand_id(product_brand_mapping)

    p_feat = (
        full_date_sales_with_brand
            .calculate_MAP_and_LAG(
                ["product", "store", "brand"],
                map_col="MA7_P", lag_col="LAG7_P")
    )

    b_feat = (
        full_date_sales_with_brand
            .calculate_MAP_and_LAG(
            ["brand","store"],
            map_col="MA7_B", lag_col="LAG7_B"
        )
    )

    s_feat = (
        b_feat
            .calculate_MAP_and_LAG(
             ["store"],
             map_col="MA7_S", lag_col="LAG7_S"
        )
    )

    features = Features(p_feat, b_feat, s_feat)
    features.form_features().to_csv("output/features.csv")

    mape = Mape(p_feat.df)
    mape.calculate(args.top).to_csv("output/mapes.csv")