 
CREATE TABLE "Customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "contact_no" integer NOT NULL, "address" varchar(300) NOT NULL);

CREATE TABLE "Employees" ("user_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "name" varchar(100) NOT NULL, "role" varchar(50) NOT NULL, "contact_no" integer NOT NULL);

CREATE TABLE "Room_types" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type" varchar(50) NOT NULL, "area" integer NOT NULL);

CREATE TABLE "Rooms" ("room_number" integer NOT NULL PRIMARY KEY, "price" integer NOT NULL, "room_type_id" bigint NOT NULL UNIQUE REFERENCES "Room_types" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Reservations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "check_in_date" date NOT NULL, "check_out_date" date NOT NULL, "reserved_by_id" integer NOT NULL REFERENCES "Employees" ("user_ptr_id") DEFERRABLE INITIALLY DEFERRED, "reserved_for_id" bigint NOT NULL REFERENCES "Customer" ("id") DEFERRABLE INITIALLY DEFERRED, "room_id" integer NOT NULL REFERENCES "Rooms" ("room_number") DEFERRABLE INITIALLY DEFERRED);

Create model Room_images
--
CREATE TABLE "app_room_images" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "Images" varchar(100) NOT NULL, "room_id" integer NOT NULL REFERENCES "Rooms" ("room_number") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "app_room_images_room_id_d8dd2ae0" ON "app_room_images" ("room_id");
COMMIT;