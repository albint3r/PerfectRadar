import csv
from geopy import distance
import pandas as pd
from ..perfectradar.col_creator import segment_sector_inmo

class PerfectRadar:
    """Find the nearest listing of a coordinate in your city (Data Base)."""

    RADIO = 1.5  # <- Radio of 1.5 km

    def __init__(self, project_name: str,  *cvs_file_path: csv):
        """This are the initialize values to create a instance.

        Need to add the name of the project and a list of CSV tables, that contains longitud and latitud columns.

        Parameters
        ----------
        project_name: str
            This is the name of the project. It doesn't affect on any of the behavior of the program.

        cvs_file_path: list/CSV
            This is a list of CSV tables to analyze. The table must have latitud and longitud columns to work.
            Can add a single file, if you add more than one it must be in the same format, because it will concatenate
            all the tables in one single result.
        """
        self.project_name = project_name
        self.csv = cvs_file_path  # <- Can add multiple paths of Listings CVS
        self.df = None
        self.lat = None
        self.long = None

    def __repr__(self):
        return self.project_name

    def config_columns(self, id : str, lat_col: str, lon_col: str, type_of_listing_col: str,
                       type_of_offer_col: str, price_col: str, rent_value: str):
        """Setup the value names of the columns inside the DataFrame Table.
        
        This is to personalize the names of the columns in the table to work correctly. The information data is saved as
        a dictionary, call it: 'config_columns'.

        Parameters
        ----------
        id : str :
            Is the Identifier for apply the drop duplicates (Example: SKU or Id)
            
        lat_col : str :
            Is the Latitude of the main location

        lon_col : str :
            Is the Longitude of the main location

        type_of_listing_col : str :
            Is the name of the column with the values of the type of listings (Example: Home, Department)

        type_of_offer_col : str :
            Is the name of the column with the values of the type of offer (Example: Sale, Rent)

        price_col : str :
            Is the name of the column with the values of the price (Example: $$$$)

        rent_value : str :
            Is the name of the value inside of the Column 'type_of_offer_col' to identify the Rent property

        Returns
        ----------
        """

        self.config_columns = dict()

        self.config_columns['ID'] = id
        self.config_columns['LAT'] = lat_col
        self.config_columns['LON'] = lon_col
        self.config_columns['TYPE_OF_LISTING'] = type_of_listing_col
        self.config_columns['TYPE_OF_OFFER'] = type_of_offer_col
        self.config_columns['PRICE'] = price_col
        self.config_columns['RENT'] = rent_value # <- This is the only single value in the config

    def assign_coordinates(self, main_lat: float, main_lon: float):
        """Create the main coordinates of the listing

        Parameters
        ----------
        main_lat : float :
            Is the Latitude of the main location
            
        main_lon : float :
            Is the Longitude of the main location
            
        main_lat: float :
            Is the Latitude that would be compare with the main Latitude
            
        main_lon: float :
            Is the Longitude that would be compare with the main Longitude

        Returns
        ----------
        """

        self.lat = main_lat
        self.long = main_lon

    def cvs_to_df(self):
        """Convert a CSV to a DataFrame

        Parameters
        ----------

        Returns
        ----------
        """

        list_csv = [pd.read_csv(csv) for csv in self.csv]
        self.df = pd.concat(list_csv)

        return self.df


    def create_col_sector_inmo(self):
        """Create a new column call it 'sector_inmo'. This column contain a string of the socioeconomic real estate
         segment.

         This segmentation apply in Mexico.

        Parameters
        ----------

        Returns
        ----------
        DataFrame
        """

        df = self.df

        type_of_offer_col = self.config_columns['TYPE_OF_OFFER']
        price_col = self.config_columns['PRICE']

        # Validate the existence of a DataFrame
        if df is None:
            raise 'You need to apply the method csv_to_df first to make this action'

        df['sector_inmo'] = df.apply(lambda row: segment_sector_inmo(row.loc[type_of_offer_col],
                                                                     row.loc[price_col]), axis= 1)
        return df

    def subset_by_type(self, type_of_listing: str = 'Casa', type_of_offer: str = 'Buy'):
        """Create a Subset of the DataFrame by type of listing and type of offer.
        
        The function identify if is a Sale or Rent property. If is a Sale property it creates a new attribute call it:
        'self.subset_by_type_rent'; this attribute works to calculate the average rental in the zone. But, if is
        a Rental it wouldn't do this, because is redundant.

        Parameters
        ----------
        type_of_listing : str
            Is the type of listing inside the column self.config['type_of_listing_col'] (Casa or Departamento).
            (Default value = 'Casa')

        type_of_offer : str
            Is the type of offer of the listing inside the column self.config['type_of_offer_col'] (Buy or rent).
            (Default value = 'Buy')

        type_of_listing : str :
            (Default value = 'Casa')

        type_of_offer : str :
            (Default value = 'Buy')

        type_of_listing: str :
             (Default value = 'Casa')

        type_of_offer: str :
             (Default value = 'Buy')

        Returns
        -------
        """

        # Are the values to subset and evaluate
        get_type_listing = self.config_columns.get('TYPE_OF_LISTING')
        get_type_offer = self.config_columns.get('TYPE_OF_OFFER')
        get_rent = self.config_columns.get('RENT')

        # Validate if the Config_column is setup
        if not hasattr(PerfectRadar, 'config_columns'):
            raise('You must setup the config_columns values of the DataFrame Columns names. '
                  'Use the config_columns method to do this!!!.')

        # Create a General Subset: Sale / Rent
        self.subset_by_type = self.df[
            (self.df[get_type_listing] == type_of_listing) &
            (self.df[get_type_offer] == type_of_offer)]

        # Create a copy, because without this it have a conflict with the DataBase
        self.subset_by_type = self.subset_by_type.copy()

        # If is A sale it creates a new DF for Rentals.
        if type_of_offer != get_rent:

            self.subset_by_type_rent = self.df[
                (self.df[get_type_listing] == type_of_listing) &
                (self.df[get_type_offer] == get_rent)] # <-- Rental

            # Copy a new DataFrame from Rentals
            self.subset_by_type_rent = self.subset_by_type.copy()

            # Return two Copy subsets: Sales & Rentals of the same zone.
            return self.subset_by_type, self.subset_by_type_rent

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

        Parameters
        ----------

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

        Parameters
        ----------

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

        show_describe : bool
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