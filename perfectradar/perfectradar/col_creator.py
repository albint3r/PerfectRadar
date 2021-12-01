def segment_sector_inmo(type_of_offer_col: str, price_col: int):
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
    sector_inmo = None

    # Validate if is a Sale
    if type_of_offer == 'Venta' or 'Buy':

        # Depend of the price_col of the listing assign a value.
        if 1000000 >= price_col:
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
    if type_of_offer == 'Renta' or 'Rent':

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