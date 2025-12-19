-- Starting with the basic codes
-- Selecting all the data from the table
SELECT * FROM "longlist";

-- key:LIMIT (To display some few rows from the table)
SELECT * FROM "longlist" LIMIT 10;

-- key:WHERE (To filter the data)
SELECT "title", "author" FROM "longlist" WHERE "year" = 2023;

-- key:NOT (negation of the value)
SELECT "title", "author" FROM "longlist" WHERE NOT ("year" = 2023);

-- key:NULL (null values There are two types of null values: 1. IS NULL 2. IS NOT NULL)
SELECT "title", "author" FROM "longlist" WHERE "year" IS NULL;

SELECT "title", "author" FROM "longlist" WHERE "year" IS NOT NULL;

-- key:LIKE (To search for a specified pattern in a column)
-- You can use the like keyword features in different ways

-- 1. To search for a specified pattern in a column
SELECT "title", "author" FROM "longlist" WHERE "title" LIKE "The%";

-- 2. by using two "%" 
SELECT "title", "author" FROM "longlist" WHERE "title" LIKE "%The%";

-- 3. by using "_" (To search for a specified pattern in a column)
SELECT "title", "author" FROM "longlist" WHERE "title" LIKE "The_";