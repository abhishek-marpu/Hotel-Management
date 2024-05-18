--  Create Table customer
CREATE TABLE "Customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "contact_no" integer NOT NULL, "address" varchar(300) NOT NULL);

--  Create Table Employees
CREATE TABLE "Employees" ("id" integer NOT NULL PRIMARY KEY , "name" varchar(100) NOT NULL, "role" varchar(50) NOT NULL, "contact_no" integer NOT NULL);

--  Create Table Room_type

CREATE TABLE "Room_types" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type" varchar(50) NOT NULL, "area" integer NOT NULL, "price" integer NOT NULL);

--  Create Table Tax_rate

CREATE TABLE "Tax_rate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tax_name" varchar(50) NOT NULL, "tax_percent" integer NOT NULL);

--  Create Table Rooms

CREATE TABLE "Rooms" ("room_number" integer NOT NULL PRIMARY KEY, "price" integer NOT NULL, "room_type" bigint NOT NULL REFERENCES "Room_types" ("id") DEFERRABLE INITIALLY DEFERRED);

--  Create model Room_availability

CREATE TABLE "room_availability" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_available" bool NOT NULL, "date" date NOT NULL, "id" integer NOT NULL REFERENCES "Rooms" ("room_number") DEFERRABLE INITIALLY DEFERRED);

-- Create model room_reviews
CREATE TABLE "room_reviews" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review" text NOT NULL, "customer" bigint NOT NULL REFERENCES "Customer" ("id") DEFERRABLE INITIALLY DEFERRED, "id" integer NOT NULL REFERENCES "Rooms" ("room_number") DEFERRABLE INITIALLY DEFERRED);

--  Create Table Room_pricing

CREATE TABLE "room_pricing" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" integer NOT NULL, "room_type" bigint NOT NULL UNIQUE REFERENCES "Room_types" ("id") DEFERRABLE INITIALLY DEFERRED);

--  Create Table Room_images

CREATE TABLE "Room_images" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "room" integer NOT NULL REFERENCES "Rooms" ("room_number") DEFERRABLE INITIALLY DEFERRED);

--  Create Table Room_features

CREATE TABLE "Room_features" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "standard" varchar(50) NOT NULL, "feature" varchar(200) NOT NULL, "updated_on" datetime NOT NULL, "room_type" bigint NOT NULL UNIQUE REFERENCES "Room_types" ("id") DEFERRABLE INITIALLY DEFERRED);

--  Create Table Reservations

CREATE TABLE "Reservations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "check_in_date" date NOT NULL, "payment_status" bool NOT NULL, "check_out_date" date NOT NULL, "reserved_by" integer NULL REFERENCES "Employees" ("id") DEFERRABLE INITIALLY DEFERRED, "reserved_for" bigint NOT NULL REFERENCES "Customer" ("id") DEFERRABLE INITIALLY DEFERRED, "room" integer NOT NULL REFERENCES "Rooms" ("room_number") DEFERRABLE INITIALLY DEFERRED);

--  Create Table Payments

CREATE TABLE "payments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "amount" integer NOT NULL, "payment_mode" varchar(50) NOT NULL, "payment_status" varchar(50) NOT NULL, "date" datetime NOT NULL, "reservation" bigint NOT NULL UNIQUE REFERENCES "Reservations" ("id") DEFERRABLE INITIALLY DEFERRED);


--  Create model Reports

CREATE TABLE "reports" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "bug" text NOT NULL, "reported_on" datetime NOT NULL, "reported_by" integer NOT NULL REFERENCES "Employees" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Create model customer_rating
CREATE TABLE "customer_rating" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" integer NOT NULL, "customer" bigint NOT NULL REFERENCES "Customer" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Create model customer_personal_data
CREATE TABLE "customer_personal_data" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "identifcation_number" integer NOT NULL, "verified" bool NOT NULL, "customer" bigint NOT NULL REFERENCES "Customer" ("id") DEFERRABLE INITIALLY DEFERRED);