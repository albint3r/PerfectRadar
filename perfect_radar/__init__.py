import csv
from geopy import distance
import pandas as pd


class PerfectRadar:
    RADIO = 1.5  # <- Radio de 1.5 km

    def __init__(self, *cvs_file_path: csv):
        self.cvs = cvs_file_path  # <- Can add multiple paths of Listings CVS
        self.df = None
        self.lat = None
        self.long = None

    def assign_coordinates(self, main_lat: float, main_lon: float):
        """Create the main coordinates of the listing"""
        self.lat = main_lat
        self.long = main_lon

    def cvs_to_df(self):
        """Convert Multiple CVS to DataFrame and then concatenate on one"""

        list_cvs = [pd.read_csv(cvs) for cvs in self.cvs]
        self.df = pd.concat(list_cvs)
        return self.df

    def subset_by_type(self, type_of_listing: str = 'Casa', type_of_offer: str = 'Buy'):

        """Create a Subset ont the DataFrame by type of listing and type of offer.
        :argument (type_of_listing: str): Is the type of listing inside the column 'Tipo de inmueble'
        (Casa or Departamento).

        :argument (type_of_offer: str): Is the type of offer inside the column 'Tipo de oferta' (Buy or Rent). The

        :returns (subset_df: DataFrame)
        """

        self.subset_by_type = self.df[
            (self.df['tipo_inmueble'] == type_of_listing) &
            (self.df['tipo_oferta_nombre'] == type_of_offer)]

        self.subset_by_type = self.subset_by_type.copy()

        return self.subset_by_type

    def mesure_distance(self, lat: float = None, long: float = None):
        """Apply the distance formula to mesure the distance between the main latitude and longitude with
        other coordinates
        :argument (lat: float) Thi is the latitud of the location you want to mesure vs your main location
        :argument (long: float) Thi is the longitud of the location you want to mesure vs your main location

        :return (float)
        """

        if self.lat is None and self.long is None:
            raise ('You need to add the main coordinates. Apply "assign_coordinates" function to do that =)')

        return distance.distance((self.lat, self.long), (lat, long))

    def mesure_df_distances(self):
        """ Apply the 'Mesure distance function' on multiple rows of the self.CSV and create a new Column
        named: Distancia. Each result represent the distance of the main coordinates with a single listing in the Data

        :returns (DataFrame)
        """

        if self.subset_by_type is None:
            raise ('Apply the subset_by_type function first.')

        self.subset_by_type['distancia'] = self.subset_by_type.apply(lambda row: self.mesure_distance(row.loc['lat_name'], row.loc['long_name']), axis=1)

        return self.subset_by_type


    def subset_by_km(self):
        """Crete a new subset base on the nearest distance of the main coordinates an the listings.
        By defualt use 1.5 radius, this is equal to 3km. The listings less than 1.5 in the distancia column of
        would be added to this new subset.

        :return (DataFrame)
        """

        self.subset_by_type = self.subset_by_type[self.subset_by_type['distancia'] <= self.RADIO]

        return self.subset_by_type

    def rm_outliers(self, *values_to_rm: str):
        """Remove the Outliers values in the DataFrame. The most comun values to remove are: price, land size and
        construction size. By default it sugets to delet the price of the DataFrame, because the prices is one of
        the most sensitive information for the user.

        :return (DataFrame)
        """

        if not bool(values_to_rm):  # <- Validate if is a empty list
            raise ('You need to add Values to the "rm_outliers" fucntion. For example: price,'
                   ' land_size or contruction_size')

        df_without_outliers = []
        for val in values_to_rm:
            val_to_rm = self.subset_by_type[val]

            # Create a Subset of the Outliers values
            q_low = val_to_rm.quantile(0.01)
            q_high = val_to_rm.quantile(0.99)

            self.subset_by_type = self.subset_by_type[(val_to_rm < q_high) & (val_to_rm > q_low)]

            df_without_outliers.append(self.subset_by_type)

        # Add df to list
        self.subset_by_type = pd.concat(df_without_outliers)

        # Drop Duplicate Rows by SKU
        self.subset_by_type = self.subset_by_type.drop_duplicates(subset='sku_nombre', keep='first')

        return self.subset_by_type
