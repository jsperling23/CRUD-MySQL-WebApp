"""
Citation for the following file:
Date: 02/29/2024
Based on osu-cs340-ecampus/flask-starter-app/bsg_people_app
Used the bsg_people_app/app.py as a template for our app.py
Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
"""

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "####"
app.config["MYSQL_PASSWORD"] = "####"
app.config["MYSQL_DB"] = "####"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
# Routes 

#Homepage routing
@app.route("/index")
@app.route("/")
def home():
    return render_template("index.j2")

# customers table browse and create routing
@app.route("/customers", methods=["POST", "GET"])
def customers():
    if request.method == "GET":
        # mySQL query to grab all the people in customers
        query = "SELECT * FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        return render_template("customers.j2", customers=data)
    
    if request.method == "POST":
        if request.form.get("addCustomer"):
            # grab user form inputs
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            phoneNumber = request.form["phoneNumber"]

            #execute the query
            query = "INSERT INTO Customers (name, email, address, phoneNumber) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, email, address, phoneNumber))
            mysql.connection.commit()
        
        return redirect("/customers")

# route for deleting from the customers table
@app.route("/delete_customer/<int:id>")
def delete_customer(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to customers page
    return redirect("/customers")

# edit a Customer
@app.route("/edit_customer/<int:id>", methods = ["POST", "GET"])
def update_customer(id):
    # render the edit page with the selected customerID
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Customers WHERE customerID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("customer_edit.j2", customers=data)

    # query and execution to edit the customer
    if request.method == "POST":
        # get user form input
        customerID = id
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]
        phoneNumber = request.form["phoneNumber"]

        #update customer
        query = "UPDATE Customers SET name = %s, email = %s, address = %s, phoneNumber = %s WHERE customerID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, email, address, phoneNumber, customerID))
        mysql.connection.commit()
        return redirect("/customers")
 
 
# display productsSales page and add new productsSales
@app.route("/productsSales", methods=["POST", "GET"])
def productsSales():
    if request.method == "GET":
        # mySQL query to grab all data for browse
        query = "SELECT Products.productID, Products.description, Sales.date, Sales.saleID, quantity FROM ProductsSales INNER JOIN Products ON ProductsSales.productID = Products.productID INNER JOIN Sales ON ProductsSales.saleID = Sales.saleID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # sales id
        query2 = "SELECT DISTINCT saleID FROM Sales"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        salesData = cur.fetchall()

        # product and description
        query3 = "SELECT DISTINCT productID, description FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        productsData = cur.fetchall()

        # render productsSales page passing our ProductsSales, Products, and Sales data to the productsSales template
        return render_template("productsSales.j2", productsSales=data, salesData=salesData, productsData=productsData)
    
    if request.method == "POST":
        if request.form.get("addProductSale"):
            # grab user form inputs
            saleID = request.form["saleID"]
            productID = request.form["productID"]
            quantity = request.form["quantity"]
            
            # add a new row to ProductsSales
            query = "INSERT INTO ProductsSales (saleID, productID, quantity) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (saleID, productID, quantity))
            mysql.connection.commit()
        
        return redirect("/productsSales")
    


    
#Delete from ProductsSales 
@app.route("/delete_productSale/<int:sale_id>/<int:product_id>")
def delete_productSale(sale_id, product_id):
    # mySQL query to delete a row
    query = "DELETE FROM ProductsSales WHERE saleID = %s AND productID = %s;"
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query, (sale_id, product_id,))
    mysql.connection.commit()

    # redirect back to productsSales page
    return redirect("/productsSales")

#Edit a ProductSale
@app.route("/edit_productSale/<int:sale_id>/<int:product_id>", methods = ["POST", "GET"])
def update_productSale(sale_id, product_id):
    if request.method == "GET":
        # mySQL query to grab the info of the row with our passed id
        query = "SELECT Products.productID, Products.description, Sales.date, Sales.saleID, quantity FROM ProductsSales INNER JOIN Products ON ProductsSales.productID = Products.productID INNER JOIN Sales ON ProductsSales.saleID = Sales.saleID WHERE ProductsSales.saleID = %s AND ProductsSales.productID = %s" % (sale_id, product_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("productSale_edit.j2", productsSales=data)
    
    if request.method == "POST":
        #get user form input
        saleID = sale_id
        productID = product_id
        quantity = request.form["quantity"]

        # query to edit a row in productsSales
        query = "UPDATE ProductsSales SET quantity = %s WHERE saleID = %s and productID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (quantity, saleID, productID))
        mysql.connection.commit()
        return redirect("/productsSales")
 
 
@app.route("/sales", methods = ["POST", "GET"])
def sales():
    if request.method == "GET":
        # mySQL query to grab all the people in Sales
        query1 = "SELECT Sales.saleID, Sales.customerID, Sales.date, Sales.locationID, Customers.name, Locations.address FROM `Sales` INNER JOIN Customers ON Sales.customerID = Customers.customerID INNER JOIN Locations ON Sales.locationID = Locations.locationID"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data1 = cur.fetchall()

        #dropdown query customerID
        query2 = "SELECT customerID, name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data2 = cur.fetchall()

        #dropdown query locationID
        query3 = "SELECT locationID, address FROM Locations;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        data3 = cur.fetchall()

        #dropdown query for filtering
        query4 = "SELECT DISTINCT Sales.customerID, Customers.name FROM Sales INNER JOIN Customers ON Sales.customerID = Customers.customerID"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        data4 = cur.fetchall()
        return render_template("sales.j2", sales=data1, customers=data2, locations=data3, dropdown=data4)
    
    if request.method == "POST":
        if request.form.get("addSale"):
            # grab user form inputs
            customerID = request.form["dropdownCust"]
            date = request.form["date"]
            locationID = request.form["dropdownLoc"]

            #add a new sale
            query = "INSERT INTO Sales (customerID, date, locationID) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (customerID, date, locationID))
            mysql.connection.commit()
        return redirect("/sales")

@app.route("/delete_sale/<int:id>")
def delete_sale(id):
    # mySQL query to delete the sale with our passed id
    query = "DELETE FROM Sales WHERE saleID = '%s';"
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to sales page
    return redirect("/sales") 

@app.route("/edit_sale/<int:id>/<int:customerID>&<int:locationID>", methods = ["POST", "GET"])
def update_sale(id, customerID, locationID):
    if request.method == "GET":
        # mySQL query to grab the info of the sale with our passed id
        query = "SELECT Sales.saleID, Sales.customerID, Sales.date, Sales.locationID, Customers.name, Locations.address FROM Sales INNER JOIN Customers ON Sales.customerID = Customers.customerID INNER JOIN Locations ON Sales.locationID = Locations.locationID WHERE saleID = %s;" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #dropdown query customerID
        query2 = "Select customerID, name FROM Customers WHERE customerID != %s" % (customerID)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data2 = cur.fetchall()

        #dropdown query locationID
        query3 = "SELECT locationID, address FROM Locations WHERE locationID !=%s;" % (locationID)
        cur = mysql.connection.cursor()
        cur.execute(query3)
        data3 = cur.fetchall()

        return render_template("sales_edit.j2", sales=data, customers=data2, locations=data3)
    
    if request.method == "POST":
        # get user inputs
        customerID = request.form["dropdownCust"]
        date = request.form["date"]
        locationID = request.form["dropdownLoc"]

        #update the row
        query = "UPDATE Sales SET customerID = %s, date = %s, locationID = %s WHERE saleID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (customerID, date, locationID, id))
        mysql.connection.commit()
        return redirect("/sales")
 
#Display products page and add new products
@app.route("/products", methods=["POST", "GET"])
def products():
    if request.method == "GET":
        # mySQL query to grab all rows from the products table
        query = "SELECT * FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render products page passing our query data 
        return render_template("products.j2", products=data)
    
    if request.method == "POST":
        if request.form.get("addProduct"):
            # grab user form inputs
            description = request.form["description"]
            price = request.form["price"]
            brand = request.form["brand"]

            #update product
            query = "INSERT INTO Products (description, price, brand) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (description, price, brand))
            mysql.connection.commit()
        
        return redirect("/products")
    
#Delete from Products 
@app.route("/delete_product/<int:id>")
def delete_product(id):
    # mySQL query to delete the product with our passed id
    query = "DELETE FROM Products WHERE productID = '%s';"
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to products page
    return redirect("/products")

#Edit a Product
@app.route("/edit_product/<int:id>", methods = ["POST", "GET"])
def update_product(id):
    if request.method == "GET":
        # mySQL query to grab the info of the product with our passed id
        query = "SELECT * FROM Products WHERE productID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("product_edit.j2", products=data)
    
    if request.method == "POST":
        # grab data based on input
        productID = id
        description = request.form["description"]
        price = request.form["price"]
        brand = request.form["brand"]

        #update the product
        query = "UPDATE Products SET description = %s, price = %s, brand = %s WHERE productID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (description, price, brand, productID))
        mysql.connection.commit()
        return redirect("/products")

#Display locations page and add new locations
@app.route("/locations", methods=["POST", "GET"])
def locations():
    if request.method == "GET":
        # mySQL query to grab all the rows in locations
        query = "SELECT * FROM Locations;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render locations page passing our query data 
        return render_template("locations.j2", locations=data)
    
    if request.method == "POST":
        if request.form.get("addLocation"):
            # grab user form inputs
            address = request.form["address"]
            phoneNumber = request.form["phoneNumber"]

            #add new location
            query = "INSERT INTO Locations (address, phoneNumber) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (address, phoneNumber))
            mysql.connection.commit()
        
        return redirect("/locations")

#Delete from Locations 
@app.route("/delete_location/<int:id>")
def delete_location(id):
    # mySQL query to delete the location with our passed id
    query = "DELETE FROM Locations WHERE locationID = '%s';"
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to locations page
    return redirect("/locations")

#Edit a Location
@app.route("/edit_location/<int:id>", methods = ["POST", "GET"])
def update_location(id):
    if request.method == "GET":
        # mySQL query to grab the info of the location with our passed id
        query = "SELECT * FROM Locations WHERE locationID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("location_edit.j2", locations=data)
    
    if request.method == "POST":
        # grab user form input
        locationID = id
        address = request.form["address"]
        phoneNumber = request.form["phoneNumber"]

        # update the location
        query = "UPDATE Locations SET address = %s, phoneNumber = %s WHERE locationID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (address, phoneNumber, locationID))
        mysql.connection.commit()
        return redirect("/locations")
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9113))
    app.run(port=port, debug=True)
