# Farmsupp-BE

Farmsupp is a platform built for the agricultural sector that uses AI models to provides expert advice to farmers on crop management, market insights, and real-time problem-solving as well as provide agricultural knowledge updates, weather forecasts, and pest alerts. Farmsupp provides farmers with a platform to post agricultural related articles as well as manage produce listings.

## Requirements

- [Python](https://www.python.org/) is a high-level, general-purpose programming language. It is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library
- [Postgres](https://www.postgresql.org/) is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
- [Fastapi](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. Its key features are high performance, speed to develop features, reduction in bugs, ease of use, robustness.
- [Openai](https://openai.com/) is an AI research and deployment company dedicated to ensuring that general-purpose artificial intelligence benefits all of humanity.

## Database Design

## Postgres Script

```
CREATE TABLE "public.user" (
	"id" uuid NOT NULL,
	"mobile_number" TEXT NOT NULL UNIQUE,
	"password" TEXT NOT NULL,
	"is_mobile_verified" BOOLEAN NOT NULL DEFAULT 'false',
	"country_code" TEXT NOT NULL DEFAULT '+234',
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "user_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.profile" (
	"id" uuid NOT NULL,
	"first_name" TEXT,
	"last_name" TEXT,
	"email" TEXT NOT NULL UNIQUE,
	"role" TEXT,
	"mobile_number" TEXT NOT NULL,
	"user_id" uuid NOT NULL,
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "profile_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.product" (
	"id" uuid NOT NULL,
	"profile_id" uuid NOT NULL,
	"name" TEXT NOT NULL,
	"description" TEXT,
	"price" int NOT NULL,
	"quantity" int NOT NULL,
	"unit" TEXT NOT NULL,
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "product_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.otp" (
	"id" uuid NOT NULL,
	"user_id" uuid NOT NULL,
	"token" TEXT NOT NULL,
	"created_at" DATE NOT NULL,
	CONSTRAINT "otp_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.image" (
	"id" uuid NOT NULL,
	"file_name" TEXT NOT NULL,
	"url" TEXT NOT NULL,
	"product_id" uuid NOT NULL,
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "image_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.article" (
	"id" uuid NOT NULL,
	"author_id" uuid NOT NULL,
	"body" TEXT NOT NULL,
	"title" TEXT NOT NULL,
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "article_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.conversation" (
	"id" uuid NOT NULL,
	"is_deleted" BOOLEAN NOT NULL DEFAULT 'false',
	"profile_id" uuid NOT NULL,
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "conversation_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.message" (
	"id" uuid NOT NULL,
	"user_message" TEXT NOT NULL,
	"conversation_id" uuid NOT NULL,
	"chatbot_response" TEXT,
	"created_at" DATE NOT NULL,
	"updated_at" DATE NOT NULL,
	CONSTRAINT "message_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

ALTER TABLE "profile" ADD CONSTRAINT "profile_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("id");

ALTER TABLE "product" ADD CONSTRAINT "product_fk0" FOREIGN KEY ("profile_id") REFERENCES "profile"("id");

ALTER TABLE "otp" ADD CONSTRAINT "otp_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("id");

ALTER TABLE "image" ADD CONSTRAINT "image_fk0" FOREIGN KEY ("product_id") REFERENCES "product"("id");

ALTER TABLE "article" ADD CONSTRAINT "article_fk0" FOREIGN KEY ("author_id") REFERENCES "profile"("id");

ALTER TABLE "conversation" ADD CONSTRAINT "conversation_fk0" FOREIGN KEY ("profile_id") REFERENCES "profile"("id");

ALTER TABLE "message" ADD CONSTRAINT "message_fk0" FOREIGN KEY ("conversation_id") REFERENCES "conversation"("id");
```

## Todo

- Ground Openai LLM on agricultural info.

## How to setup locally

- Clone repository using `git clone `
- Create a virtual environment in the project root folder and create a virtual environment using `python -m venv venv`
- Setup virtual environment by typing `source venv\Scripts\activate`
- Install requirements using `pip install -r requirements.txt`
- Run development server by typing `bash run_dev_server.sh`

## Useful commands

- `alembic revision --autogenerate` to automatically generate migrations
- `alembic upgrade head` to run migrations

## Author

[Alahira Jeffrey](https://github.com/alahirajeffrey)
