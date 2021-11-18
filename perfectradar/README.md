# Perfect Radar

A package that find the closes coordinates points in an area that you chose.

This package was created by [Alberto Ortiz](https://www.linkedin.com/in/alberto-ortiz-06935784/) from [Perfect Deals](https://www.perfectdeals.com.mx/).

### Features
- **Measure the distances between two points** to determine the which ones are the most proximate

### Usage 

````
import perfectradar
````

# Find the closes points in a Data Base
Add a list of CSV that contains Latitude and longitud columns.
Then specify your main coordinates and the name of the columns that you want to filter.
For last, you need to add the Outliers values columns you want to filter to run the program.

### Example
````
def perfect_factory():
    """This is the factory function to create the simplest version of 
    the PerfectRadar """

    # 1) Create Instances of Perfect Radar
    p = PerfectRadar(r'./listing_csv')  # <- Add CSV

    p.config_columns( id = 'sku_nombre',  # <- Config Columns
              lat_col = 'lat_name' ,
              lon_col='long_name',
              type_of_listing_col='tipo_inmueble',
              type_of_offer_col='tipo_oferta_nombre'
             )

    # 2) Add the coordinates you want to analyze
    p.assign_coordinates(20.6948693,
                -103.4108069)  # Add <- Coordinates

    # 3) Convert list of cvs into a DataFrame
    p.cvs_to_df()

    # 4) Filter the DataFrame by the type of the listing
    p.subset_by_type() # <- Add type of listing and type of Offer

    # 5) Create a new Column in the DataFrame to compare 
    # the distance between properties
    p.mesure_df_distances()

    # 6) Create a subset by the nearest distance between 
    # the main location an the closes listings.
    p.subset_by_km()

    # 7) Remove the the Outliers of your chose
    df_result = p.rm_outliers('precio_name',
                              'm2_terreno_name',
                              'm2_construccion_name',
                               show_describe = True) 

    return df_result

if __name__ == '__main__':
    df = perfect_factory()
````