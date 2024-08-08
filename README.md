# CockroachDB-Retail-Demo

This demo simulates a multi-region ecommerce application using CockroachDB as the backend database. The application showcases key features including user management, product cataloging, inventory tracking, shopping cart functionalities, and order processing. Users from different regions interact with the system by browsing products, adding items to their carts, and completing orders with payment details recorded. The demo emphasizes the seamless handling of multi-region data, real-time inventory updates, and consistent user experiences, illustrating CockroachDB's capabilities in supporting distributed, high-availability ecommerce applications.

# Walkthrough of the demo
## Setup
### Database Setup

This demo requires CockroachDB to be setup in multiple regions and use the multi-region regions. It needs to be setup to survive a region failure. Although this demo and readme is based on CockroachDB Serverless Multi-region, you can also use CockroachDB Self Hosted, Dedicated or Serverless for the demo. The CockroachDB Serverless cluster has been setup in the following regions on Google Cloud Platform: us-central1(PRIMARY REGION), us-east1, us-west2

![](/docs/cockroachdbcloud-multiregion.png)

**Create Tables and Load database with demo data**

Assuming you are using a cloud instance, eg, a linux ec2 machine, configure git and clone the repo:

```
sudo yum install -y git
git clone https://github.com/harshn08/CockroachDB-Retail-Demo.git
```

To create the Tables use the import.sql. Go to the git directory and run the following command:

```
cat import.sql | cockroachd sql --url "postgresql://<user>:<password>@<hostname>:26257/defaultdb?sslmode=verify-full"
```

To load the demo data, you need to make edits to the datagen.py file and configure the database connection parameters. After thats done, make sure you have your machine configured with python and pip and any additional requirements installed. If you are running this on cloud instances, eg, a linux ec2 machine, run the following commands to install python and other dependencies manually or you can run the install_prerequisites.sh script:

```
sudo yum install -y python3
sudo yum install -y python3-pip
sudo pip3 install psycopg2-binary
sudo pip3 install faker
sudo pip3 install datetime
```
After thats done run the configured datagen.py file using the following command:

```
python datagen.py
```

Depending on your instance, it may take some time to generate the data for the demo.

### CockroachDB Data Model

Here is how we have the database setup for this demo:

![](/docs/RoachShop-ERD.jpg)

#### Table Details ####
Here are some details on the role of each table for this demo:

Users
* Role: Stores information about customers, including personal details and contact information. It identifies the users participating in transactions.

Cart
* Role: Represents shopping carts associated with users, tracking the status (active, inactive, or canceled) and creation details.

Cart_Items
* Role: Contains the products added to a user's cart, including the quantity and price at the time of addition.

Orders
* Role: Records completed orders placed by users, including order status, total amount, and timestamps.

Order_Items
* Role: Details the specific products and quantities included in each order, linked to the Orders table.

Payment_Details
* Role: Captures payment information for orders, including payment method, status, transaction ID, and the amount paid.

Inventory
* Role: Tracks the stock levels of products across different warehouse locations, including quantities and last update times.

Products
* Role: Contains details about the products available for sale, including names, descriptions, prices, and associated categories.

Categories
* Role: Defines the categories for organizing products, such as Electronics, Clothing, Home & Kitchen, etc.

### Simulating the demo

Next, create a virtual instance in three diffrerent regions that correspond with the three regions of your database. It doesn't have to be exactly the same regions in case you are using a different cloud provider than where your database was setup but as long as its close enough it works for the demo. The reason why we are taking this approach is because we want to simulate the data from each of those regions to get it to resemble a real workload. 

On each of those instances, download the git repo and configure them with the required dependencies:

```
sudo yum install -y git
git clone https://github.com/harshn08/CockroachDB-Retail-Demo.git
sudo yum install -y python3
sudo yum install -y python3-pip
sudo pip3 install psycopg2-binary
sudo pip3 install faker
sudo pip3 install datetime
```

There are 3 simulator files in the repo, one corresponding to each region. Configure the simulator files(eg: roachshop_workload_west.py) with the database connection parameters. Once that is complete, you can start the corresponding simulator files in the instances in the corresponding regions using the following command:

```
python roachshop_workload_west.py
```

And here is what a sample output looks like when the simulator is running as intended:

```
User 35376663-6112-4008-b8e9-c8a5b996a1d0 from us-west placed an order 92bbea5c-99dd-49aa-b8f8-d836d9e9ca08 with status completed.
User 9759479c-e650-4b0b-9fa0-ff425262dcbb from us-west placed an order f15da975-23c9-4128-92cb-fabd09e47db5 with status completed.
User 61a3f232-b084-4b01-afe7-c23819eee749 from us-west placed an order 28a3c2ad-7d61-4327-b535-04cc721d982a with status completed.
User 7879bd3a-a106-49fc-b968-a39d71819f80 from us-west placed an order b3e80f6b-e5cf-4887-9a70-a628abb84f21 with status completed.
....
....
```

### Logical Flow of the Demo ###

#### High-Level Workflow Outline ####

For each user in the selected region simulate Adding Items to Cart:
* Create a new cart for the user.
* Randomly select products and quantities to add to the cart.
* Check if the products are in stock. If not, update the cart status to 'canceled'. 


Check Cart Items:
* If the cart contains items, proceed to checkout.
* If the cart is empty, skip to the next user.

Simulate Checkout:
* Process the cart for checkout, creating an order and corresponding order items.
* Update the cart status to 'inactive' if the order is completed, or 'canceled' if the order fails.
* Record payment details, including payment method, status, and transaction ID.

Process Order:
* Update inventory quantities based on the completed order.

Log Order Information
* Output details of each order, including user ID, order ID, and order status.

![](/docs/RoachShop-FlowChart.jpg)

### Contributing ###

Reach out to Harsh Shah for details on this project and supporting material. Feel free to submit issues and pull requests. Contributions are welcome!
