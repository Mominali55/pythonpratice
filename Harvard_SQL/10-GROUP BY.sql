-- Demonstration of GROUP BY clause in SQL

-- Finds average rating for each book
SELECT "book_id",ROUND(avg("rating"),2) AS "average rating" FROM "ratings"
GROUP BY "book_id";

-- Jions titles
SELECT "title",ROUND(avg("rating"),2) AS "average rating" FROM "ratings"
JOIN "books" ON "books"."id" = "ratings"."book_id"
GROUP BY "book_id";

-- Chooses books with a rating of 4.0 or higher 
SELECT "title",ROUND(AVG("rating"),2) AS "average rating " FROM "ratings"
JOIN "books" ON "books"."id" = "ratings"."book_id"
GROUP BY "book_id"
HAVING "average rating" > 4.0;