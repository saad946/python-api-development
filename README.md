# FastAPI and PostgreSQL Setup Guide

This guide provides step-by-step instructions to set up a FastAPI application with a PostgreSQL database. Follow these instructions to create a virtual environment, install necessary dependencies, configure PostgreSQL, and run the FastAPI server.

## Setup Instructions

py -3 -m venv venv
change the python via View and python select Interprter
venv\Scripts\activate.bat
pip install fastapi
python.exe -m pip install --upgrade pip
pip freeze => packages installed
pip install uvicorn
pip install bcrypt==4.2.0
pip install passlib==1.7.4
pip install email-validator
pip install python-jose[cryptography]
uvicorn main:app
uvicorn app.main:app --reload automatically restart the server after new change.
Install the Postman
Go to Body section and select the json to post some data.
fastapi work from start to end, so be careful if you put some variable restriction in above code.
422 Unprocessable Entity: when wrong data, or data types send to the server.
User - dbms -db , dbms basicaaly connect with db engine and provide the response
Data Types:
Numeric: int, decimal, precision
text: varchar,textbool: boolean
sequence: array

add limitations:
add primary key to get all entities, like user id.
make entry of column uniqe with UNIQUE
make it sure that entries is not null via NOT NULL


connect via cmd:
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres

Reset the postgresql password:
Open pg_hba.conf in a text editor with administrator privileges (e.g., Notepad) at C:\Program Files\PostgreSQL\15\data\pg_hba.conf

local    all             all             127.0.0.1/32            trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust

Restart the postgres via,
Win + R
search services.msc and restrt the process named PostgreSQL-15

connect to the server again via 
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres
ALTER USER postgres PASSWORD 'newpassword';

Re-edit pg_hba.conf
Open pg_hba.conf again and change trust back to md5 (or whatever method was used before):
local    all             all             127.0.0.1/32           scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256


connect to db with new password
go to db, schema, table and create a table named products
name = character varrying, not null
price = integer, not null
bigint and small int = tell the bit of the value


-- Table: public.products

-- DROP TABLE IF EXISTS public.products;

CREATE TABLE IF NOT EXISTS public.products
(
    "Name" character varying COLLATE pg_catalog."default" NOT NULL,
    "Price" integer NOT NULL,
    id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),
    CONSTRAINT products_pkey PRIMARY KEY (id)
)

for timestamp colum , put now() under its defaults values;
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.products
    OWNER to postgres;


craete column by going to rright click to table, then view all rows
then further give column properties via column properties then CONSTRAINTsave them via database optiion on table outputs.

go to quert editor via right click db then query tool

SELECT * from products;
SELECT "Name" from products;
SELECT "Name",id from products;
SELECT id AS products_id,"Name" from products limit 5;
SELECT id AS products_id,"Name" from products where id = 1 ;
SELECT * from products WHERE inventory = 5;
SELECT * from products WHERE "Name" = 'TV';
SELECT * from products WHERE inventory < 10;
SELECT * from products WHERE inventory != 0;
SELECT * from products WHERE inventory > 0 AND "Price" >100 ;
SELECT * from products WHERE inventory > 0 OR "Price" >100 ;     
SELECT * from products WHERE "Price" > 100 AND "Price" <1000;
SELECT * from products WHERE id = 7 OR id =9 OR id=10 ;
SELECT * from products WHERE id IN (7,8,9);
SELECT * from products WHERE "Name" LIKE 'TV%';
SELECT * from products WHERE "Name" NOT LIKE '%e';
SELECT * from products ORDER BY "Price" ASC;
SELECT * from products ORDER BY inventory DESC, "Price" ASC ;
SELECT * from products ORDER BY timestamp ;
SELECT * from products WHERE "Price" > 20 ORDER BY timestamp ;
SELECT id AS products_id,"Name" from products LIMIT 5 offset 2;
INSERT INTO products ("Name","Price",is_sale,inventory) VALUES('mouse',4,true,58) returning id;
INSERT INTO products ("Name","Price",is_sale,inventory) VALUES('keyboard',5,true,680),('table',4,true,50) returning id,"Name";
DELETE FROM products WHERE id =10;
DELETE FROM products WHERE id =11 RETURNING *;
DELETE FROM products WHERE inventory =0;
UPDATE products SET "Name" = 'House',"Price" = 1000000 WHERE id = 7;
UPDATE products SET is_sale = 'false'WHERE id = 12 RETURNING *;
UPDATE products SET is_sale = 'true' WHERE inventory < 10 RETURNING *;

connect db with python
pip3 install psycopg2

this libraray gives column name RealDictCursor

ORM=sqlalchemy
code => orm => db
pip3 install sqlalchemy

https://fastapi.tiangolo.com/tutorial/sql-databases/#install-sqlalchemy
if using 2 @

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Tubelight1%40@localhost/postgres"

with sqlalchemy we cant modify column attribute or properties so need to use alembic Notepad

In command prompt
echo %MY_DB_URL%


SQL Joins
SELECT * FROM post LEFT JOIN users ON post.user_id =users.id;

SELECT title, content,email FROM post LEFT JOIN users ON post.user_id =users.id;
SELECT post.id,content,email FROM post LEFT JOIN users ON post.user_id =users.id;
SELECT post.*,content,email FROM post LEFT JOIN users ON post.user_id =users.id;
SELECT users.id, count(*) FROM post RIGHT JOIN users ON post.user_id =users.id group by users.id;

SELECT users.id,count(post.id) FROM post RIGHT JOIN users ON post.user_id =users.id group by users.id;
SELECT users.id,users.email,count(post.id) as user_post_count FROM post RIGHT JOIN users ON post.user_id =users.id group by users.id;




