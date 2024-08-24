# FastAPI and PostgreSQL Setup Guide

This guide provides step-by-step instructions to set up a FastAPI application with a PostgreSQL database. Follow these instructions to create a virtual environment, install necessary dependencies, configure PostgreSQL, and run the FastAPI server.

## Setup Instructions

* **Create a Virtual Environment**  
  Create a virtual environment to manage project dependencies:

  ```bash
  py -3 -m venv venv
Change the Python Interpreter
Change the Python interpreter via View -> Command Palette -> Python: Select Interpreter in your code editor.

Activate the Virtual Environment
Activate the virtual environment:

Windows:
bash
Copy code
venv\Scripts\activate.bat
Install Dependencies
Install the required Python packages:

bash
Copy code
pip install fastapi
python.exe -m pip install --upgrade pip
pip install uvicorn
pip install bcrypt==4.2.0
pip install passlib==1.7.4
pip install email-validator
pip install python-jose[cryptography]
Check Installed Packages
To see the list of installed packages, run:

bash
Copy code
pip freeze
Run the FastAPI Server
To run the FastAPI server, use:

bash
Copy code
uvicorn main:app
To automatically restart the server after any changes, use:

bash
Copy code
uvicorn app.main:app --reload
Install Postman
Install Postman to test your API endpoints. Go to the Body section in Postman and select JSON to post some data.

Handling Errors in FastAPI
FastAPI processes requests from start to end, so be careful if you put any variable restrictions in your code.

Common error:

422 Unprocessable Entity: This occurs when incorrect data or data types are sent to the server.
User - DBMS - DB
The DBMS connects with the DB engine and provides the response.

Data Types

Numeric: int, decimal, precision
Text: varchar, text
Bool: boolean
Sequence: array
Add Limitations

Add a primary key to get all entities, like a user ID.
Make entries in a column unique with UNIQUE.
Ensure that entries are not null via NOT NULL.
PostgreSQL Configuration
Connect via Command Line
Connect to PostgreSQL using the command line:

bash
Copy code
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
Reset PostgreSQL Password

Open pg_hba.conf in a text editor with administrator privileges (e.g., Notepad) located at C:\Program Files\PostgreSQL\15\data\pg_hba.conf.
Update the following lines to allow local connections without a password:
sql
Copy code
local    all             all             127.0.0.1/32            trust
host     all             all             127.0.0.1/32            trust
host     all             all             ::1/128                 trust
Restart PostgreSQL:

Press Win + R

Search for services.msc

Restart the service named PostgreSQL-15

Connect to the server again:
bash
Copy code
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres
Reset the PostgreSQL password:
sql
Copy code
ALTER USER postgres PASSWORD 'newpassword';
Re-edit pg_hba.conf to secure the database again:
bash
Copy code
local    all             all             127.0.0.1/32           scram-sha-256
host     all             all             127.0.0.1/32           scram-sha-256
host     all             all             ::1/128                scram-sha-256
Connect to DB with New Password
Go to DB schema, table and create a table named products:

name = character varying, not null
price = integer, not null
bigint and smallint = specify the bit of the value
Create a Table in PostgreSQL

sql
Copy code
CREATE TABLE IF NOT EXISTS public.products
(
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Price" integer NOT NULL,
    id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),
    CONSTRAINT products_pkey PRIMARY KEY (id)
)
For the timestamp column, put now() under its default values.

Table Management in PostgreSQL
After creating the table, manage columns and constraints through table properties.

Query Editor in PostgreSQL
Open the query editor via right-clicking the DB and selecting "Query Tool".

SQL Commands
Basic SQL Commands for PostgreSQL
sql
Copy code
SELECT * FROM products;
SELECT "Name" FROM products;
SELECT "Name", id FROM products;
SELECT id AS products_id, "Name" FROM products LIMIT 5;
SELECT id AS products_id, "Name" FROM products WHERE id = 1;
SELECT * FROM products WHERE inventory = 5;
SELECT * FROM products WHERE "Name" = 'TV';
SELECT * FROM products WHERE inventory < 10;
SELECT * FROM products WHERE inventory != 0;
SELECT * FROM products WHERE inventory > 0 AND "Price" > 100;
SELECT * FROM products WHERE inventory > 0 OR "Price" > 100;
SELECT * FROM products WHERE "Price" > 100 AND "Price" < 1000;
SELECT * FROM products WHERE id = 7 OR id = 9 OR id = 10;
SELECT * FROM products WHERE id IN (7, 8, 9);
SELECT * FROM products WHERE "Name" LIKE 'TV%';
SELECT * FROM products WHERE "Name" NOT LIKE '%e';
SELECT * FROM products ORDER BY "Price" ASC;
SELECT * FROM products ORDER BY inventory DESC, "Price" ASC;
SELECT * FROM products ORDER BY timestamp;
SELECT * FROM products WHERE "Price" > 20 ORDER BY timestamp;
SELECT id AS products_id, "Name" FROM products LIMIT 5 OFFSET 2;
INSERT INTO products ("Name", "Price", is_sale, inventory) VALUES ('mouse', 4, true, 58) RETURNING id;
INSERT INTO products ("Name", "Price", is_sale, inventory) VALUES ('keyboard', 5, true, 680), ('table', 4, true, 50) RETURNING id, "Name";
DELETE FROM products WHERE id = 10;
DELETE FROM products WHERE id = 11 RETURNING *;
DELETE FROM products WHERE inventory = 0;
UPDATE products SET "Name" = 'House', "Price" = 1000000 WHERE id = 7;
UPDATE products SET is_sale = 'false' WHERE id = 12 RETURNING *;
UPDATE products SET is_sale = 'true' WHERE inventory < 10 RETURNING *;
Connecting to PostgreSQL with Python
Install psycopg2

bash
Copy code
pip3 install psycopg2
This library provides the RealDictCursor to handle query results.

Using SQLAlchemy ORM
Install SQLAlchemy

bash
Copy code
pip3 install sqlalchemy
SQLAlchemy Connection String
Configure the SQLAlchemy connection string in your application:

python
Copy code
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Tubelight1%40@localhost/postgres"
If you're using alembic for migrations, note that SQLAlchemy can't modify column attributes directly; you must use Alembic for that purpose.

SQL Joins
Example SQL join commands:

sql
Copy code
SELECT * FROM post LEFT JOIN users ON post.user_id = users.id;
SELECT title, content, email FROM post LEFT JOIN users ON post.user_id = users.id;
SELECT post.id, content, email FROM post LEFT JOIN users ON post.user_id = users.id;
SELECT post.*, content, email FROM post LEFT JOIN users ON post.user_id = users.id;
SELECT users.id, count(*) FROM post RIGHT JOIN users ON post.user_id = users.id GROUP BY users.id;
SELECT users.id, count(post.id) FROM post RIGHT JOIN users ON post.user_id = users.id GROUP BY users.id;
SELECT users.id, users.email, count(post.id) AS user_post_count FROM post RIGHT JOIN users ON post.user_id = users.id GROUP BY users.id;
Running the Application
Environment Variables
Set your environment variables using the command prompt:

bash
Copy code
echo %MY_DB_URL%
Follow these instructions carefully to set up your FastAPI application with PostgreSQL. Make sure to manage dependencies and configurations correctly to avoid any errors during the setup process.

sql
Copy code

This `README.md` file includes all the setup instructions and SQL commands you provided. You can copy and paste it 