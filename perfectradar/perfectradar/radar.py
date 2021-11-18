import csv
from geopy import distance
import pandas as pd

class PerfectRadar:
    """Find the nearest listing of a coordinate in your city (Data Base). """

    RADIO = 1.5  # <- Radio of 1.5 km

    def __init__(self, project_name: str,  *cvs_file_path: csv):
        self.project_name = project_name
        self.csv = cvs_file_path  # <- Can add multiple paths of Listings CVS
        self.df = None
        self.lat = None
        self.long = None

    def __repr__(self):
        return self.project_name

    def config_columns(self, id : str, lat_col: str, lon_col: str, type_of_listing_col: str, type_of_offer_col: str):
        """Setup the value names of the columns inside the DataFrame Table.

        This is to personalize the names of the columns in the table to work correctly. The information data is saved as
        a dictionary, call it: 'config_columns'.

        Parameters
        ----------
        id: str
            This could be a regular ID or SKU identifier

        lat_col: str
            Latitude Column name in the DataFrame

        lon_col: str
            Longitude Column name in the DataFrame

        type_of_listing_col: str
            Type of listing column name

        type_of_offer_col: str
            Type of offer column name
        """

        self.config_columns = dict()

        self.config_columns['ID'] = id
        self.config_columns['LAT'] = lat_col
        self.config_columns['LON'] = lon_col
        self.config_columns['TYPE_OF_LISTING'] = type_of_listing_col
        self.config_columns['TYPE_OF_OFFER'] = type_of_offer_col

    def assign_coordinates(self, main_lat: float, main_lon: float):
        """Create the main coordinates of the listing

        Parameters
        ----------
        main_lat : float
            This is latitud of the main location of the area it will be analyze

        main_lon : float
            This is longitud of the main location of the area it will be analyze
        """

        self.lat = main_lat
        self.long = main_lon

    def cvs_to_df(self):
        """Convert Multiple CVS to DataFrame and then concatenate all in one"""

        list_csv = [pd.read_csv(csv) for csv in self.csv]
        self.df = pd.concat(list_csv)
        return self.df

    def subset_by_type(self, type_of_listing: str = 'Casa', type_of_offer: str = 'Buy'):
        """Create a Subset of the DataFrame by type of listing and type of offer.

        Parameters
        ----------
        type_of_listing : str
            Is the type of listing inside the column self.config['type_of_listing_col'] (Casa or Departamento).
            (Default value = 'Casa')

        type_of_offer : str
            Is the type of offer of the listing inside the column self.config['type_of_offer_col'] (Buy or rent).
            (Default value = 'Buy')

        Raises
        -------
        raise:
            The user must first configurate the name of the columns inside the DataFrame.

        Returns
        -------
        DataFrame
        """

        # Validate if the Config_column is setup
        if not hasattr(PerfectRadar, 'config_columns'):
            raise('You must setup the config_columns values of the DataFrame Columns names. '
                  'Use the config_columns method to do this!!!.')

        self.subset_by_type = self.df[
            (self.df[self.config_columns.get('TYPE_OF_LISTING')] == type_of_listing) &
            (self.df[self.config_columns.get('TYPE_OF_OFFER')] == type_of_offer)]

        self.subset_by_type = self.subset_by_type.copy()

        return self.subset_by_type

    def mesure_distance(self, lat: float = None, long: float = None):
        """Mesure the distance between one to one coordinates.

        Apply the distance formula to mesure the distance between the main latitude and longitude with
        other coordinates.

        Parameters
        ----------
        lat : float
            This is the latitud of the location you want to mesure vs your main location
            (Default value = None)

        long : float
            This is the longitud of the location you want to mesure vs your main location
            (Default value = None)

        Returns
        -------
        Distance
        """

        if self.lat is None and self.long is None:
            raise 'You need to add the main coordinates. Apply "assign_coordinates" function to do that =)'

        return distance.distance((self.lat, self.long), (lat, long))

    def mesure_df_distances(self):
        """Mesure the distance between one to many coordinates.

        Apply the 'Mesure distance function' on multiple rows of the self.subset_by_type (DataFrame) and create
        a new Column named: Distancia. Each result represent the distance of the main coordinates with a single
        listing in the Data.

        Returns
        -------
        DataFrame
        """

        if self.subset_by_type is None:
            raise 'Apply the subset_by_type function first.'

        self.subset_by_type['distancia'] = self.subset_by_type.apply(
            lambda row: self.mesure_distance(row.loc[self.config_columns.get
            ('LAT')], row.loc[self.config_columns.get('LON')]), axis=1)

        return self.subset_by_type

    def subset_by_km(self):
        """Crete a new subset base on the nearest distance of the main coordinates an the listings.

        By default use 1.5 radius, this is equal to 3km. The listings less than 1.5 in the distancia column of
        would be added to this new subset.

        Returns
        -------
        DataFrame
        """

        self.subset_by_type = self.subset_by_type[self.subset_by_type['distancia'] <= self.RADIO]

        return self.subset_by_type

    def rm_outliers(self, *values_to_rm: str, show_describe: bool = False):
        """Remove the Outliers values in the DataFrame.

        The most commune values to remove are: price, land size and
        construction size. By default it suggests to delete the price of the DataFrame, because the prices is one of
        the most sensitive information for the user.

        Parameters
        ----------
        *values_to_rm : str
            This is a list of the names of columns values that will be removed from the Subset DataFrame.

        show_describe: bool
            This apply the describe method of pandas to show a resume of the final result.
            (Default value = None, optional)

        Returns
        -------
        DataFrame
        """

        if not bool(values_to_rm):  # <- Validate if is a empty list
            raise ('You need to add Values to the "rm_outliers" function. For example: price,'
                   'land_size or construction_size')

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
        self.subset_by_type = self.subset_by_type.drop_duplicates(subset=self.config_columns.get('ID'), keep='first')

        # Show the a resume of the data result.
        if show_describe:
            print(f'The function run correctly! Total results near: {len(self.subset_by_type)}\n')
            print(self.subset_by_type[['precio_name', 'm2_terreno_name', 'm2_construccion_name']].describe(). \
                  apply(lambda x: x.apply('{:.2f}'.format)))

        return self.subset_by_type