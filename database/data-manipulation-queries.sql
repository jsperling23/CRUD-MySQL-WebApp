-- Customers
-- Insert a new customer
INSERT INTO
    Customers (name, email, phoneNumber, address)
VALUES
    (
        :nameInput,
        :emailInput,
        :phoneNumberInput,
        :addressInput
    );

-- get all customers for the browse Customers page
SELECT
    *
FROM
    Customers;

-- update a customer's data based on submission of the Update Customer form 
SELECT
    *
FROM
    Customers
WHERE
    id = :customer_ID_selected_from_browse_customer_page
UPDATE
    Customers
SET
    name = :nameInput,
    email = :emailInput,
    phoneNumber = :phoneNumberInput,
    address = :addressInput
WHERE
    id = :customer_ID_from_the_update_form;

-- delete a customer
DELETE FROM
    Customers
WHERE
    id = :customer_ID_selected_from_browse_customer_page;

-----------------------------------------------------------------------------
-- Products
-- Insert a new product
INSERT INTO
    Products(description, price, brand)
VALUES
    (
        :descriptionInput,
        :priceInput,
        :brandInput
    );

-- get all products for the browse Products page
SELECT
    *
FROM
    Products;

-- update a products data based on submission of the Update Product form 
SELECT
    *
FROM
    Products
WHERE
    id = :product_ID_selected_from_browse_product_page
UPDATE
    Products
SET
    description = :descriptionInput,
    price = :priceInput,
    brand = :brandInput
WHERE
    id = :product_ID_from_the_update_form;

-- delete a product
DELETE FROM
    Products
WHERE
    id = :product_ID_selected_from_browse_product_page;

-----------------------------------------------------------------------------
-- Locations
-- Insert a new location
INSERT INTO
    Locations(address, phoneNumber)
VALUES
    (
        :addressInput,
        :phoneNumberInput
    );

-- get all locations for the browse Locations page
SELECT
    *
FROM
    Locations;

-- update a locations data based on submission of the Update Location form 
SELECT
    *
FROM
    Locations
WHERE
    id = :location_ID_selected_from_browse_location_page
UPDATE
    Locations
SET
    address = :addressInput,
    phoneNumber = :phoneNumberInput,
WHERE
    id = :location_ID_from_the_update_form;

-- delete a location
DELETE FROM
    Locations
WHERE
    id = :location_ID_selected_from_browse_location_page;

-----------------------------------------------------------------------------
-- Sales
-- Insert a new sale
INSERT INTO
    Sales(customerID, date, locationID)
VALUES
    (
        :customerIDInput,
        :dateInput,
        :locationIDInput
    );
-- Sale dropdown menus
-- dropdown menus
SELECT customerID, name FROM Customers;
SELECT locationID, address FROM Locations;
-- get all sales for the browse sales page, include customer name and location address
SELECT DISTINCT Sales.customerID, Customers.name FROM Sales INNER JOIN Customers ON Sales.customerID = Customers.customerID;

-- get all sales for the selected customerID
SELECT
    Sales.saleID,
    Sales.customerID,
    Sales.date,
    Sales.locationID
FROM
    Sales
WHERE
    Sales.customerID = :selected_customerID;

-- get all sales for the browse sales page filtered by customerID
SELECT
    *
FROM
    Sales
WHERE
    id = :sale_ID_selected_from_browse_sale_page;

-- update a Sales data based on submission of the Update Sale form 
SELECT
    *
FROM
    Sales
WHERE
    id = :sale_ID_selected_from_browse_sale_page
UPDATE
    Sales
SET
    customerID = :customerIDInput,
    date = :dateInput,
    location = :locationIDInput
WHERE
    id = :sale_ID_from_the_update_form;
-- update sale dropdown menus
SELECT Sales.saleID, Sales.customerID, Sales.date, Sales.locationID, Customers.name, Locations.address FROM Sales INNER JOIN Customers ON Sales.customerID = Customers.customerID INNER JOIN Locations ON Sales.locationID = Locations.locationID WHERE saleID = :currentSaleID;
Select customerID, name FROM Customers WHERE customerID != :currentCustomerID
-- delete a sale
DELETE FROM
    Sales
WHERE
    id = :sale_ID_selected_from_browse_sale_page;

-----------------------------------------------------------------------------
-- ProductsSales
-- Insert a new product sale
INSERT INTO
    ProductsSales(saleID, productID, quantity)
VALUES
    (
        (
            SELECT
                saleID
            FROM
                Sales
            WHERE
                saleID = :saleIDInput
        ),
        (
            SELECT
                productID
            FROM
                Products
            WHERE
                productID = :productIDInput
        ),
        :quantityInput
    ); -- get all product sales for the browse Products Sales page
SELECT
    ProductsSales.saleID,
    ProductsSales.productID,
    ProductsSales.quantity,
    Products.description,
    Sales.date
FROM
    ProductsSales
    JOIN Products ON ProductsSales.productID = Products.productID
    JOIN Sales ON ProductsSales.saleID = Sales.saleID;

-- update a products sales data based on submission of the Update Product Sale form 
SELECT
    *
FROM
    Products
WHERE
    id = :product_ID_selected_from_browse_product_page
UPDATE
    Products
SET
    saleID = :saleIDInput,
    productID = :productIDInput,
    quantity = :quantityInput
WHERE
    id = :product_ID_from_the_update_form;

-- delete a product sale
DELETE FROM
    ProductsSales
WHERE
    id = :product_ID_selected_from_browse_product_sale_page;
