SET
    FOREIGN_KEY_CHECKS = 0;
SET
    AUTOCOMMIT = 0;

-- Setup Customers Table
CREATE
OR REPLACE TABLE Customers(
    customerID int AUTO_INCREMENT NOT NULL UNIQUE,
    name varchar(45) NOT NULL,
    email varchar(145) NOT NULL UNIQUE,
    phoneNumber varchar(15) NOT NULL,
    address varchar(145) NOT NULL,
    PRIMARY KEY (customerID)
);

-- Setup Locations Table
CREATE
OR REPLACE TABLE Locations(
    locationID int AUTO_INCREMENT NOT NULL UNIQUE,
    address varchar(145) NOT NULL UNIQUE,
    phoneNumber varchar(15) NOT NULL UNIQUE,
    PRIMARY KEY (locationID)
);

-- Setup Products Table
CREATE
OR REPLACE TABLE Products(
    productID int AUTO_INCREMENT NOT NULL UNIQUE,
    description varchar(255) NOT NULL,
    price decimal(10, 2) NOT NULL,
    brand varchar(145) NOT NULL,
    PRIMARY KEY (productID)
);

-- Setup Sales Table
CREATE
OR REPLACE TABLE Sales(
    saleID int AUTO_INCREMENT NOT NULL UNIQUE,
    customerID int NULL,
    date date NOT NULL,
    locationID int NULL,
    PRIMARY KEY (saleID),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
    ON DELETE SET NULL,
    FOREIGN KEY (locationID) REFERENCES Locations(locationID)
    ON DELETE SET NULL
);

-- Setup intersection table between Products and Sales
CREATE
OR REPLACE TABLE ProductsSales(
    saleID INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (saleID, ProductID),
    CONSTRAINT FK_SALESID FOREIGN KEY (saleID) REFERENCES Sales(saleID) ON DELETE CASCADE,
    CONSTRAINT FK_PRODUCTID FOREIGN KEY (productID) REFERENCES Products(productID)
    ON DELETE CASCADE
);

-- Fill the Customers table
INSERT INTO
    Customers(name, email, phoneNumber, address)
VALUES
    (
        "Gerry Lopez",
        "gerry.shaka.brah@gmail.com",
        "5556668121",
        "42 Wallaby Way, Syndey, Australia"
    ),
    (
        "Sharon Sharon",
        "sharon.sharon@gmail.com",
        "4205692310",
        "55 Straight St., Nowhere, CA, 94253"
    ),
    (
        "Eugene Krabs",
        "kru$tyboi@hotmail.com",
        "2345439102",
        "15 Coral Ave., Bikini Bottom, Pacific Ocean"
    );

-- Fill Locations Table
INSERT INTO
    Locations(address, phoneNumber)
VALUES
    (
        "16th Street, Portland, OR, 92014",
        "1234567891"
    ),
    (
        "Long Street, Longsville, ID, 21492",
        "(241)556-9301"
    ),
    (
        "Longer Street, Longestville, ID, 29102",
        "5920192102"
    );

-- Fill products table
INSERT INTO
    Products(description, price, brand)
VALUES
    (
        "Skis",
        250.53,
        "Rossignol"
    ),
    (
        "Snow Boots",
        172.21,
        "LL Bean"
    ),
    (
        "Chalk Bag",
        15.99,
        "Patagonia"
    );

-- Fill Sales Table
INSERT INTO
    Sales(customerID, date, locationID)
VALUES
    (
        (
            SELECT
                customerID
            from
                Customers
            WHERE
                customerID = 1
        ),
        20240501,
        (
            SELECT
                locationID
            from
                Locations
            WHERE
                LocationID = 3
        )
    ),
    (
        (
            SELECT
                customerID
            from
                Customers
            WHERE
                customerID = 2
        ),
        20220331,
        (
            SELECT
                locationID
            from
                Locations
            WHERE
                LocationID = 1
        )
    ),
    (
        (
            SELECT
                customerID
            from
                Customers
            WHERE
                customerID = 3
        ),
        17230522,
        (
            SELECT
                locationID
            from
                Locations
            WHERE
                LocationID = 2
        )
    );

-- Fill ProductsSales Table
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
                saleID = 1
        ),
        (
            SELECT
                productID
            FROM
                Products
            WHERE
                productID = 1
        ),
        4
    ),
    (
        (
            SELECT
                saleID
            FROM
                Sales
            WHERE
                saleID = 2
        ),
        (
            SELECT
                productID
            FROM
                Products
            WHERE
                productID = 1
        ),
        1
    ),
    (
        (
            SELECT
                saleID
            FROM
                Sales
            WHERE
                saleID = 2
        ),
        (
            SELECT
                productID
            FROM
                Products
            WHERE
                productID = 3
        ),
        2
    );

SELECT
    *
FROM
    Customers;

SELECT
    *
FROM
    Locations;

SELECT
    *
FROM
    Products;

SELECT
    *
FROM
    Sales;

SELECT
    *
FROM
    ProductsSales;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;