CREATE TABLE "Users" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "username" varchar UNIQUE,
  "email" varchar UNIQUE,
  "password" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "Projects" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "owner_id" int,
  "title" varchar,
  "description" text,
  "goal_amount" decimal,
  "start_date" date,
  "end_date" date,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "Donations" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "user_id" int,
  "project_id" int,
  "amount" decimal,
  "created_at" timestamp
);

CREATE TABLE "Categories" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "name" varchar,
  "description" text
);

CREATE TABLE "ProjectCategories" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "project_id" int,
  "category_id" int
);

CREATE TABLE "Comments" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "user_id" int,
  "project_id" int,
  "text" text,
  "created_at" timestamp
);

CREATE TABLE "Ratings" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "user_id" int,
  "project_id" int,
  "rating" int,
  "created_at" timestamp
);

CREATE TABLE "Reports" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "user_id" int,
  "project_id" int,
  "reason" text,
  "created_at" timestamp
);

CREATE TABLE "Media" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "project_id" int,
  "image_url" varchar,
  "created_at" timestamp
);

ALTER TABLE "Projects" ADD FOREIGN KEY ("owner_id") REFERENCES "Users" ("id");

ALTER TABLE "Donations" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Donations" ADD FOREIGN KEY ("project_id") REFERENCES "Projects" ("id");

ALTER TABLE "Comments" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Comments" ADD FOREIGN KEY ("project_id") REFERENCES "Projects" ("id");

ALTER TABLE "Ratings" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Ratings" ADD FOREIGN KEY ("project_id") REFERENCES "Projects" ("id");

ALTER TABLE "Reports" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Reports" ADD FOREIGN KEY ("project_id") REFERENCES "Projects" ("id");

ALTER TABLE "Media" ADD FOREIGN KEY ("project_id") REFERENCES "Projects" ("id");

ALTER TABLE "ProjectCategories" ADD FOREIGN KEY ("project_id") REFERENCES "Projects" ("id");

ALTER TABLE "ProjectCategories" ADD FOREIGN KEY ("category_id") REFERENCES "Categories" ("id");
