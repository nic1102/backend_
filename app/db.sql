CREATE TABLE "quotes" (
	"id" serial NOT NULL UNIQUE,
	"song_id" int NOT NULL,
	"text" varchar(255) NOT NULL UNIQUE,
	"is_validated" boolean NOT NULL DEFAULT false,
	"likes" int NOT NULL DEFAULT 0,
	"dislikes" int NOT NULL DEFAULT 0,
	PRIMARY KEY("id")
);


CREATE TABLE "songs" (
	"id" serial NOT NULL UNIQUE,
	"group_id" int NOT NULL,
	"name" varchar(255) NOT NULL UNIQUE,
	"is_validated" boolean NOT NULL DEFAULT false,
	PRIMARY KEY("id")
);


CREATE TABLE "groups" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL UNIQUE,
	"is_validated" boolean NOT NULL DEFAULT false,
	PRIMARY KEY("id")
);


ALTER TABLE "quotes"
ADD FOREIGN KEY("id") REFERENCES "songs"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "songs"
ADD FOREIGN KEY("group_id") REFERENCES "groups"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;