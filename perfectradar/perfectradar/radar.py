import csv
from geopy import distance
import pandas as pd
from typing import Union
from ..perfectradar.col_creator import segment_sector_inmo, avg_price_m2, avg_price_m2_const

float_int = Union[float, int]

class PerfectRadar:
    """Find the nearest listing of a coordinate in your city (Data Base)."""

    RADIO = 1.5  # <- Is the distance it will be calculated between The main location and other.
    RENTAL_MINIMAL_DATA = 5 # <- Is the minimal amount of rows in Rent DataFrame to accepts.

    def __init__(self, project_name: str, *cvs_file_path: csv):
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

    def config_columns(self, id: str, lat_col: str, lon_col: str, type_of_listing_col: str,
                       type_of_offer_col: str, price_col: str, land_size_col: str, rent_value: str) -> None:
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
            Is the name of the column with the values of the type of listings (Values Examples: Home, Department)

        type_of_offer_col : str :
            Is the name of the column with the values of the type of offer (Values Examples: Sale, Rent)

        price_col : str :
            Is the name of the column with the values of the price (Value Example: $ 75000000)

        rent_value : str :
            Is the name of the value inside of the Column 'type_of_offer_col' to identify the Rent property
            # TODO Improve this comment
        Returns
        ----------
        None
        """

        self.config_columns = dict()

        self.config_columns['ID'] = id
        self.config_columns['LAT'] = lat_col
        self.config_columns['LON'] = lon_col
        self.config_columns['TYPE_OF_LISTING'] = type_of_listing_col
        self.config_columns['TYPE_OF_OFFER'] = type_of_offer_col
        self.config_columns['PRICE'] = price_col
        self.config_columns['LAND_SIZE'] = land_size_col
        self.config_columns['RENT'] = rent_value  # <-This is not a Column Name. It refers a Value inside a Column Val.

    def set_coordinates(self, main_lat: float, main_lon: float) -> None:
        """Set the main coordinates of the point you want to analyze.

        It will create a Circle of 3 Km or the equivalent of 1.5 radio (GLOBAL DEFAULT VALUE). With this circumference
        it will select all the other assigned coordinates points there are inside it.

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
        None
        """

        self.lat = main_lat
        self.long = main_lon

    def cvs_to_df(self) -> pd.core.frame.DataFrame:
        """Convert a CSV to a DataFrame

        Parameters
        ----------

        Returns
        ----------
        DataFrame -> pd.core.frame.DataFrame
        """

        list_csv = [pd.read_csv(csv) for csv in self.csv]
        self.df = pd.concat(list_csv)
        return self.df

    def set_col_sector_inmo(self) -> pd.core.frame.DataFrame:
        """Create a new column call it 'sector_inmo'. This column contain a string of the socioeconomic real estate
         segment.

         This segmentation apply in Mexico.

        Parameters
        ----------

        Returns
        ----------
        DataFrame -> pd.core.frame.DataFrame
        """


        df = self.df
        type_of_offer_col = self.config_columns['TYPE_OF_OFFER'] # <- Just for make more readable the code
        price_col = self.config_columns['PRICE']

        # Validate if the method csv_to_df was applied before.
        if df is None:
            raise 'You need to apply the method csv_to_df first to make this action'

        # Create the Column that contain the category by price of the listing.
        df['sector_inmo'] = df.apply(lambda row: segment_sector_inmo(row.loc[type_of_offer_col],
                                                                     row.loc[price_col]), axis=1)
        return df

    def set_avg_pricem2_col(self) -> pd.core.frame.DataFrame:
        """Set a new column that contains the Average Price of the construction of a property.

        Returns
        ----------
        pd.core.frame.DataFrame
        """

        df = self.df

        land_size_m2 = self.config_columns['LAND_SIZE']
        price = self.config_columns['PRICE']
        type_of_listing_col = self.config_columns['TYPE_OF_LISTING']

        # Validate the existence of a DataFrame
        if df is None:
            raise 'You need to apply the method csv_to_df first to make this action'

        # Crete the Column with the average price of land size
        df['avg_price_m2'] = df.apply(lambda row: avg_price_m2(row.loc[price],
                                                               row.loc[land_size_m2],
                                                               row.loc[type_of_listing_col]), axis=1)

        return df

    def set_avg_priceconst_col(self) -> pd.core.frame.DataFrame:
        """Set a new column that contains the average price of construction of a property.

        Returns
        ----------
        pd.core.frame.DataFrame
        """

        df = self.df

        land_size_m2 = self.config_columns['LAND_SIZE']
        price = self.config_columns['PRICE']

        # Validate the existence of a DataFrame
        if df is None:
            raise 'You need to apply the method csv_to_df first to make this action'

        # Create the column with the average price
        df['avg_price_const'] = df.apply(lambda row: avg_price_m2_const(row.loc[price], row.loc[land_size_m2]), axis=1)

        return df

    def set_sim_val(self, price: float_int, m2_terr: float_int,
                    m2_const: float_int, rooms: int, bathrooms: int, cars: int) -> None:
        """Assign information values to the attributes  to simulates a Listing.

        This is convenient to use when you what to calculate the Financial CAT value of the listing.

        Parameters
        ----------
        price: float_int:
            Is the Price of the simulate listing.

        m2_terr: float_int:
            Is the Land Size of the simulate listing.

        m2_const: float_int:
            Is the Construction of the simulate listing.

        rooms: int:
            Is the # of rooms of the simulate listing.

        bathrooms: int:
            Is the # of bathrooms of the simulate listing.
        cars: int:
            Is the # cars of the simulate listing.

        Returns
        ----------
        None
        """

        self.price = price
        self.m2_terr = m2_terr
        self.m2_cosnt = m2_const
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.cars = cars

        # Change this Global Value to true to apply the simulation
        self.sim_data = True

    def subset_by_type(self, type_of_listing: str = 'Casa', type_of_offer: str = 'Buy') -> pd.core.frame.DataFrame:
        """Create a Subset of the DataFrame by type of listing and type of offer.
        
        The function identify if is a Sale or Rent property. If is a Sale property it creates a new attribute call it:
        'self.subset_by_type_rent'; this attribute works to calculate the average rental in the zone. But, if is
        a Rental it wouldn't do this, because is redundant. This function all ways return two DataFrames. But,
        have some exceptions. 1) First: If is a Buy Listing it will return two DF. 2) Second: If is a Rental it will
        return One DF and a None Value. The none Value reference to the Rent DataFrame that want create, because
        it ineficiente calculate Buy if the user select Only rent.

        Is probably that in next version it will all ways return 2 DataFrames with information. To calculate both sides!

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
        DataFrame -> pd.core.frame.DataFrame
        """

        # Are the values to subset and evaluate
        get_type_listing = self.config_columns.get('TYPE_OF_LISTING')
        get_type_offer = self.config_columns.get('TYPE_OF_OFFER') # Just to make more readable the code
        rent_val = self.config_columns.get('RENT')

        # Validate if the Config_column is setup
        if not hasattr(self, 'config_columns'):  # <- Validate attribute exist
            raise ('You must setup the config_columns values of the DataFrame Columns names. '
                   'Use the config_columns method to do this!!!.')

        # Create a General Subset: Sale / Rent
        self.subset_by_type = self.df[
            (self.df[get_type_listing] == type_of_listing) &
            (self.df[get_type_offer] == type_of_offer)]

        # Create a copy, because without this it have a conflict with the DataBase
        self.subset_by_type = self.subset_by_type.copy()

        # Assign the Rent Attribute the None Value, The avoid conflict in the mesure method
        self.subset_by_type_rent = None
        # If is A sale it creates a new DF for Rentals.
        if type_of_offer != rent_val:
            self.subset_by_type_rent = self.df[
                (self.df[get_type_listing] == type_of_listing) &
                (self.df[get_type_offer] == rent_val)]  # <-- Rental

            # Copy a new DataFrame from Rentals
            self.subset_by_type_rent = self.subset_by_type_rent.copy()

        return self.subset_by_type, self.subset_by_type_rent  # <- Sales and Rental Result

    def set_subset_sector_inmo(self) -> pd.core.frame.DataFrame:
        """Validate if the Rent Subset have enough data to be significant to create a Subset with this data.

        It applies a if condition counting the rows in de DF. If doesn't have more than 3 rows (default)
         it would return false. And then Only would considerate the Average price and m2 construction
         price from the Main Subset.

        Parameters
        ----------

        Returns
        -------
        DataFrame
        """

        # Validate is func set_sim_val was used before
        if not hasattr(self, 'sim_data'):
            raise 'First you need to apply the "set_sim_val" method to use this method.'

        rent_subset = self.subset_by_type_rent

        # Validate rent_subset exist
        if rent_subset is None:
            raise 'set_subset_sector_inmo: This function only apply for Buy properties.Change the argument to "buy" in the statement: type_of_offer'

        # Assign the social segment of the real estate property
        self.sector_inmo = segment_sector_inmo('Buy', self.price)


        # Create the subset
        self.subset_by_type_rent = rent_subset[rent_subset['sector_inmo'] == self.sector_inmo]

        return self.subset_by_type_rent

    def mesure_distance(self, lat: float = None, long: float = None) -> distance.geodesic:
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
        Distance -> distance.geodesic
        """

        if self.lat is None and self.long is None:
            raise 'You need to add the main coordinates. Apply "set_coordinates" function to do that =)'

        return distance.distance((self.lat, self.long), (lat, long))

    def mesure_df_distances(self) -> pd.core.frame.DataFrame:
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

        main_subset = self.subset_by_type
        rent_subset = self.subset_by_type_rent if self.subset_by_type_rent is not None else None # Validate if Rent DF
        lat = self.config_columns.get('LAT')  # <- The name of the Lat Col
        long = self.config_columns.get('LON')  # <- The name of the Long Col

        # Validate Main subset exist
        if main_subset is None:
            raise 'Apply the subset_by_type function first.'

        main_subset['distancia'] = main_subset.apply(
            lambda row: self.mesure_distance(row.loc[lat], row.loc[long]), axis=1)

        # Validate if Rent Subset exist
        if rent_subset is not None:
            rent_subset['distancia'] = rent_subset.apply(
                lambda row: self.mesure_distance(row.loc[lat], row.loc[long]), axis=1)

        return main_subset, rent_subset

    def subset_by_km(self) -> pd.core.frame.DataFrame:
        """Crete a new subset base on the nearest distance of the main coordinates an the listings.
        
        By default use 1.5 radius, this is equal to 3km. The listings less than 1.5 in the distancia column of the
        Table would be added to this new subset.

        Parameters
        ----------

        Returns
        -------
        DataFrame
        """

        main_df = self.subset_by_type # Just make more readable the code

        self.subset_by_type = main_df[main_df['distancia'] <= self.RADIO]

        # Validate if Rent Subset Exist
        if self.subset_by_type_rent is not None:
            self.subset_by_type_rent = self.subset_by_type_rent[self.subset_by_type_rent['distancia'] <= self.RADIO]

        return self.subset_by_type, self.subset_by_type_rent

    def rm_outliers(self, dataframe: pd.core.frame.DataFrame,
                    show_describe: bool = False, *values_to_rm: str) -> pd.core.frame.DataFrame:
        """Remove the Outliers values in the DataFrame.
        
        The most commune values to remove are: price, land size and
        construction size. By default it suggests to delete the price of the DataFrame, because the prices is one of
        the most sensitive information for the user.

        Parameters
        ----------
        show_describe : boolean "
            This apply the describe method of pandas to show a resume of the final result.
            (Default value = None, optional)

        dataframe : pd.core.frame.DataFrame :
            This is the attribute that contains the DataFrame it would remove the outliers
            (Example: self.subset_by_type')

        *values_to_rm : str :
            This is a list of the names of columns values that will be removed from the Subset DataFrame.

        Returns
        -------
        DataFrame
        """

        if not values_to_rm:  # <- Validate if is a empty list
            raise ('You need to add Values to the "rm_outliers" function. For example: price,'
                   'land_size or construction_size')

        df_without_outliers = []
        for val in values_to_rm:
            val_to_rm = dataframe[val]

            # Create a Subset of the Outliers values (Min and Max).
            q_low = val_to_rm.quantile(0.01)
            q_high = val_to_rm.quantile(0.99)

            # Concatenate The subset to have all rows DF
            dataframe = dataframe[(val_to_rm < q_high) & (val_to_rm > q_low)]

            df_without_outliers.append(dataframe)

        # Because it creates a new Table for each value introduced before is important to concat all tables.
        dataframe = pd.concat(df_without_outliers)

        # And Drop the duplicate values for is ID (Example: SKU).
        dataframe = dataframe.drop_duplicates(subset=self.config_columns.get('ID'), keep='first')

        # Show the a resume of the data result.
        if show_describe:
            print(f'The function run correctly! Total results near: {len(dataframe)}\n')
            print(dataframe[['precio_name', 'm2_terreno_name', 'm2_construccion_name']].describe(). \
                  apply(lambda x: x.apply('{:.2f}'.format)))

        return dataframe
