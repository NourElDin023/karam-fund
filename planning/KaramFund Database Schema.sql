CREATE TABLE "User" (
  "id" int PRIMARY KEY,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "password" varchar NOT NULL,
  "phone_number" varchar(12) NOT NULL,
  "is_admin" boolean DEFAULT false,
  "profile_picture" varchar,
  "bio" text,
  "is_activated" boolean DEFAULT false,
  "birthdate" date,
  "facebook_profile" varchar,
  "country" varchar,
  "created_at" timestamp NOT NULL DEFAULT 'now()'
);

CREATE TABLE "Project" (
  "id" int PRIMARY KEY,
  "title" varchar NOT NULL,
  "description" text NOT NULL,
  "target_amount" decimal NOT NULL,
  "current_amount" decimal NOT NULL DEFAULT 0,
  "category_id" int NOT NULL,
  "creator_id" int NOT NULL,
  "campaign_start" date NOT NULL,
  "campaign_end" date NOT NULL,
  "is_active" boolean DEFAULT true,
  "avg_rating" decimal DEFAULT 0,
  "is_reported" boolean DEFAULT false,
  "is_deleted" boolean DEFAULT false,
  "is_cancelled" boolean DEFAULT false
);

CREATE TABLE "ProjectMedia" (
  "id" int PRIMARY KEY,
  "project_id" int NOT NULL,
  "media_url" varchar NOT NULL,
  "added_at" timestamp DEFAULT 'now()'
);

CREATE TABLE "ProjectCategory" (
  "id" int PRIMARY KEY,
  "name" varchar NOT NULL
);

CREATE TABLE "Tag" (
  "id" int PRIMARY KEY,
  "name" varchar NOT NULL
);

CREATE TABLE "ProjectTags" (
  "project_id" int NOT NULL,
  "tag_id" int NOT NULL,
  "primary" key(project_id,tag_id)
);

CREATE TABLE "ProjectDonations" (
  "id" int PRIMARY KEY,
  "user_id" int NOT NULL,
  "project_id" int NOT NULL,
  "amount" decimal NOT NULL,
  "created_at" timestamp DEFAULT 'now()'
);

CREATE TABLE "ProjectComments" (
  "id" int PRIMARY KEY,
  "user_id" int NOT NULL,
  "project_id" int NOT NULL,
  "comment" text NOT NULL,
  "parent_comment_id" int,
  "created_at" timestamp DEFAULT 'now()',
  "is_reported" boolean DEFAULT false,
  "is_deleted" boolean DEFAULT false
);

CREATE TABLE "ProjectRate" (
  "id" int PRIMARY KEY,
  "user_id" int NOT NULL,
  "project_id" int NOT NULL,
  "rate" int NOT NULL,
  "created_at" timestamp DEFAULT 'now()'
);

CREATE TABLE "ProjectReport" (
  "id" int PRIMARY KEY,
  "reporter_id" int NOT NULL,
  "project_id" int NOT NULL,
  "reason" text NOT NULL,
  "created_at" timestamp DEFAULT 'now()',
  "status" varchar DEFAULT 'pending'
);

CREATE TABLE "CommentReport" (
  "id" int PRIMARY KEY,
  "reporter_id" int NOT NULL,
  "comment_id" int NOT NULL,
  "reason" text NOT NULL,
  "created_at" timestamp DEFAULT 'now()',
  "status" varchar DEFAULT 'pending'
);

CREATE TABLE "AdminSelectedProjects" (
  "project_id" int PRIMARY KEY NOT NULL
);

ALTER TABLE "Project" ADD FOREIGN KEY ("category_id") REFERENCES "ProjectCategory" ("id");

ALTER TABLE "Project" ADD FOREIGN KEY ("creator_id") REFERENCES "User" ("id");

ALTER TABLE "ProjectMedia" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");

ALTER TABLE "ProjectTags" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");

ALTER TABLE "ProjectTags" ADD FOREIGN KEY ("tag_id") REFERENCES "Tag" ("id");

ALTER TABLE "ProjectDonations" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "ProjectDonations" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");

ALTER TABLE "ProjectComments" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "ProjectComments" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");

ALTER TABLE "ProjectComments" ADD FOREIGN KEY ("parent_comment_id") REFERENCES "ProjectComments" ("id");

ALTER TABLE "ProjectRate" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "ProjectRate" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");

ALTER TABLE "ProjectReport" ADD FOREIGN KEY ("reporter_id") REFERENCES "User" ("id");

ALTER TABLE "ProjectReport" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");

ALTER TABLE "CommentReport" ADD FOREIGN KEY ("reporter_id") REFERENCES "User" ("id");

ALTER TABLE "CommentReport" ADD FOREIGN KEY ("comment_id") REFERENCES "ProjectComments" ("id");

ALTER TABLE "AdminSelectedProjects" ADD FOREIGN KEY ("project_id") REFERENCES "Project" ("id");
