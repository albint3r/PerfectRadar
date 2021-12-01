from perfectradar.perfectradar.radar import PerfectRadar
import csv


def perfect_factory():
    """This is the factory function to create the simplest version of the PerfectRadar """

    # 1) Create Instances of Perfect Radar
    p = PerfectRadar('Test_project', './demo_data/deptos_venta', './demo_data/deptos_renta',
                     './demo_data/casa_venta', './demo_data/casa_renta')  # <- Add CSV

    # 2) Config the name of the columns in the DB
    p.config_columns(id='sku_nombre',
                     lat_col='lat_name',
                     lon_col='long_name',
                     type_of_listing_col='tipo_inmueble',
                     type_of_offer_col='tipo_oferta_nombre',
                     price_col='precio_name',
                     land_size_col= 'm2_terreno_name',
                     rent_value='Rent',
                     )

    # 3) Add the coordinates you want to analyze
    p.set_coordinates(20.6953967, -103.4134952)  # Add <- Coordinates

    # 4) Convert list of cvs into a DataFrame
    p.cvs_to_df()

    # 5) Filter the DataFrame by the type of the listing
    p.set_col_sector_inmo()  # <- Add type of listing and type of Offer
    p.set_avg_pricem2_col()  # <- Add col avg_price_m2
    p.set_avg_priceconst_col()  # <- Add col avg_price_construction

    # 6) Filter the DataFrame by the type of the listing
    p.subset_by_type(type_of_listing = 'Casa', type_of_offer= 'Buy')  # <- Add type of listing and type of Offer

    # 6.1) Set the Listing Simulator
    p.set_sim_val(6500000, 150, 150, 3, 3, 2.5)

    # 6.2) Create a subset by the type of socioeconomically segment of the rents table.
    p.set_subset_sector_inmo()

    # 7) Create a new Column in the DataFrame to compare the distance between properties
    p.mesure_df_distances()

    # 8) Create a subset by the nearest distance between the main location an the closes listings.
    p.subset_by_km()

    # 9) Remove the the Outliers of your chose
    main_df_result = p.rm_outliers(p.subset_by_type, True, 'precio_name', 'm2_terreno_name',
                              'm2_construccion_name' )  # <- Add list of values (str)

    # 9.1) Remove the the Outliers of your chose
    rent_df_result = p.rm_outliers(p.subset_by_type_rent, True, 'precio_name', 'm2_terreno_name',
                              'm2_construccion_name')  # <- Add list of values (str)

    return main_df_result, rent_df_result

if __name__ == '__main__':
    main_df_result, rent_df_result = perfect_factory()



