from perfectradar.perfectradar.radar import PerfectRadar
import csv

def perfect_factory():
    """This is the factory function to create the simplest version of the PerfectRadar """

    # 1) Create Instances of Perfect Radar
    p = PerfectRadar(r'./listing_csv')  # <- Add CSV

    p.config_columns( id = 'sku_nombre',
              lat_col = 'lat_name' ,
              lon_col='long_name',
              type_of_listing_col='tipo_inmueble',
              type_of_offer_col='tipo_oferta_nombre'
             )

    # 2) Add the coordinates you want to analyze
    p.assign_coordinates(20.6948693, -103.4108069)  # Add <- Coordinates

    # 3) Convert list of cvs into a DataFrame
    p.cvs_to_df()

    # 4) Filter the DataFrame by the type of the listing
    p.subset_by_type() # <- Add type of listing and type of Offer

    # 5) Create a new Column in the DataFrame to compare the distance between properties
    p.mesure_df_distances()

    # 6) Create a subset by the nearest distance between the main location an the closes listings.
    p.subset_by_km()

    # 7) Remove the the Outliers of your chose
    df_result = p.rm_outliers('precio_name', 'm2_terreno_name',
                              'm2_construccion_name', show_describe = True)  # <- Add list of values (str)

    return df_result

if __name__ == '__main__':
    df = perfect_factory()
