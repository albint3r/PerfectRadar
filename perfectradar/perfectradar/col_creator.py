def segment_sector_inmo(type_of_offer_col: str, price_col: int) -> int:
    """Create a New Column call it 'Sector_inmo'. This is a filter of the socioeconomic sectors in Mexico
    by the price_col of the property.

    Parameters
    ----------
    type_of_offer_col : str
            This is the name of the column with the type of offer values (Example: Buy, Rent)
    price_col : str
        This is the name of the column with the price values (Example: $$$)

    Returns
    -------
    str
    """

    type_of_offer = type_of_offer_col
    sector_inmo = 'Unknown'

    # Validate if is a Sale
    if 'Buy' == type_of_offer or type_of_offer == 'Venta':

        # Depend of the price_col of the listing assign a value.
        if price_col <= 1000000:
            sector_inmo = 'Interés Social'

        if 1000001 <= price_col <= 3000000:
            sector_inmo = 'Interés Medio'

        if 3000001 <= price_col <= 7000000:
            sector_inmo = 'Residencial'

        if 7000001 <= price_col <= 15000000:
            sector_inmo = 'Residencial Plus'

        if 15000001 <= price_col:
            sector_inmo = 'Premium'

    # Validate if is a Apartment 
    if type_of_offer == 'Rent' or type_of_offer == 'Renta' :

        # Depend of the price_col of the listing assign a value.
        if 5000 >= price_col:
            sector_inmo = 'Interés Social'

        if 5001 <= price_col <= 10000:
            sector_inmo = 'Interés Medio'

        if 10001 <= price_col <= 15000:
            sector_inmo = 'Residencial'

        if 15001 <= price_col <= 30000:
            sector_inmo = 'Residencial Plus'

        if 30001 <= price_col:
            sector_inmo = 'Premium'

    return sector_inmo

def avg_price_m2(price: float, land_size_m2: float, type_of_listing_col: str) -> float:
    """Creates a New Column call it mean_price_m2, that refer to the averange value
    of the meter in a listing property.

    Parameters
    ----------
        price : float :
            Is the price of the Main Listing

        land_size_m2 : float :
            Is the land size of the Main Listing

        type_of_listing_col: str
            Is the way to validate if is a house or apartment. In general Apartments don't have
            land size and it would cause a Zero Division error.

    Returns
    ----------
    Int
    """

    # validate if is a House
    if type_of_listing_col == 'Casa' or type_of_listing_col == 'House' :

        try:
            result = price / land_size_m2
        except ZeroDivisionError:
            result = 0

    elif type_of_listing_col == 'Departamento' or type_of_listing_col == 'Department':
        result = 0

    else:
        result = 0

    return round(result)


def avg_price_m2_const(price: float, m2_construction: float) -> float:
    """Creates a New Column call it mean_price_m2, that refer to the average value
    of the meter in a listing property.

    Parameters
    ----------
        price : float :
            Is the price of the Main Listing

        m2_construction : float :
            Is the Construction size of the Main Listing

    Returns
    ----------
    Int
    """
    try:
        result = price / m2_construction

    except ZeroDivisionError:

        result = 0

    return round(result)

if __name__ == '__main__':
    print(avg_price_m2(5000000, 120, 'Casa'))