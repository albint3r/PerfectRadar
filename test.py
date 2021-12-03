import pytest
from perfectradar.perfectradar.col_creator import segment_sector_inmo, avg_price_m2, avg_price_m2_const

def test_segment_sector_inmo_interes_social():
    """Test the sector_inmo works well when it creates the new columns
    on the DataFrame"""
    
    # English version 
    assert segment_sector_inmo('Buy', 1) == 'Interés Social'
    assert segment_sector_inmo('Buy', 1000000) == 'Interés Social'
    
    
    assert segment_sector_inmo('Rent', 1) == 'Interés Social'
    assert segment_sector_inmo('Rent', 5000) == 'Interés Social'
    
    # None Version 
    assert segment_sector_inmo('', 1000000) == 'Unknown'
    
    # Spanish version 

    assert segment_sector_inmo('Venta', 1) == 'Interés Social'
    assert segment_sector_inmo('Venta', 1000000) == 'Interés Social'

    assert segment_sector_inmo('Renta', 1) == 'Interés Social'
    assert segment_sector_inmo('Renta', 5000) == 'Interés Social'


def test_segment_sector_inmo_interes_medio():
    """Test the sector_inmo works well when it creates the new columns
        on the DataFrame"""

    # English version
    # Buy
    assert segment_sector_inmo('Buy', 1000001) == 'Interés Medio'
    assert segment_sector_inmo('Buy', 3000000) == 'Interés Medio'
    #Rent
    assert segment_sector_inmo('Rent', 5001) == 'Interés Medio'
    assert segment_sector_inmo('Rent', 10000) == 'Interés Medio'
    
    # None Version 
    assert segment_sector_inmo('', 3000000) == 'Unknown'

    # Spanish Version
    # Venta
    assert segment_sector_inmo('Venta', 1000001) == 'Interés Medio'
    assert segment_sector_inmo('Venta', 3000000) == 'Interés Medio'

    # Renta
    assert segment_sector_inmo('Renta', 5001) == 'Interés Medio'
    assert segment_sector_inmo('Renta', 10000) == 'Interés Medio'

def test_segment_sector_inmo_residencial():
    """Test the sector_inmo works well when it creates the new columns
        on the DataFrame"""
    
    # English version
    # Buy
    assert segment_sector_inmo('Buy', 3000001) == 'Residencial'
    assert segment_sector_inmo('Buy', 7000000) == 'Residencial'
    
    # None Version 
    assert segment_sector_inmo('', 7000000) == 'Unknown'
    
    # Rent
    assert segment_sector_inmo('Rent', 10001) == 'Residencial'
    assert segment_sector_inmo('Rent', 15000) == 'Residencial'
    
    # Spanish Version
    # Venta
    assert segment_sector_inmo('Venta', 3000001) == 'Residencial'
    assert segment_sector_inmo('Venta', 7000000) == 'Residencial'
    #Renta
    assert segment_sector_inmo('Renta', 10001) == 'Residencial'
    assert segment_sector_inmo('Renta', 15000) == 'Residencial'

def test_segment_sector_inmo_residencial_premum():
    """Test the sector_inmo works well when it creates the new columns
        on the DataFrame"""
    # English Version
    # Buy
    assert segment_sector_inmo('Buy', 7000001) == 'Residencial Plus'
    assert segment_sector_inmo('Buy', 15000000) == 'Residencial Plus'
    
    # None Version 
    assert segment_sector_inmo('', 15000000) == 'Unknown'
    
    # Rent
    assert segment_sector_inmo('Rent', 15001) == 'Residencial Plus'
    assert segment_sector_inmo('Rent', 30000) == 'Residencial Plus'
    
    # Spanish Version
    # Venta
    assert segment_sector_inmo('Venta', 7000001) == 'Residencial Plus'
    assert segment_sector_inmo('Venta', 15000000) == 'Residencial Plus'
    # Renta
    assert segment_sector_inmo('Renta', 15001) == 'Residencial Plus'
    assert segment_sector_inmo('Renta', 30000) == 'Residencial Plus'
    
def test_segment_sector_inmo_premium():
    """Test the sector_inmo works well when it creates the new columns
        on the DataFrame"""
    
    # English version
    #Buy
    assert segment_sector_inmo('Buy', 15000001) == 'Premium'
    
    # None Version 
    assert segment_sector_inmo('', 15000001) == 'Unknown'
    
    # Rent
    assert segment_sector_inmo('Rent', 30001) == 'Premium'
    
    # Spanish Version
    # Buy
    assert segment_sector_inmo('Venta', 15000001) == 'Premium'
    # Renta
    assert segment_sector_inmo('Renta', 30001) == 'Premium'

def test_avg_price_m2_house():
    """Test the create average column creator"""
    

    # English version
    assert avg_price_m2(6500000, 150, 'House') == 43333
    assert avg_price_m2(6500000, 140, 'House') != 43333 # <- Not correct result test
    # Spanish version
    assert avg_price_m2(6500000, 150, 'Casa') == 43333
    assert avg_price_m2(6500000, 140, 'Casa') != 43333 # <- Not correct result test
    # Zero Division erro
    assert avg_price_m2(0, 140, 'Casa') == 0  # <- Not correct result test
    assert avg_price_m2(0, 140, 'House') == 0  # <- Not correct result test


def test_avg_price_m2_department():
    """Test the create average column creator"""

    # English version
    assert avg_price_m2(6500000, 150, 'Department') == 0
    assert avg_price_m2(6500000, 140, 'Department') == 0  # <- Not correct result test
    # Spanish version
    assert avg_price_m2(6500000, 150, 'Departamento') == 0
    assert avg_price_m2(6500000, 140, 'Departamento') == 0  # <- Not correct result test

def test_avg_price_m2_no_value():
    """Test when the listing don't have any type of property type"""
    assert avg_price_m2(6500000, 150, '') == 0
    
def test_avg_price_m2_const():
    """Test the function create new col avg construction price"""
    # Expected information
    assert avg_price_m2_const(6500000, 150) == 43333
    # ZeroDivision Error expected
    assert avg_price_m2_const(0, 150) == 0