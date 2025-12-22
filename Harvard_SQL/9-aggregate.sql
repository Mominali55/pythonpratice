-- Finding the averag rating of all longlisted books and rounding the result
SELECT ROUND(AVG("rating"), 2) FROM "longlist";

-- Renaming the column to "Average Rating" by using AS keyword
SELECT ROUND(AVG("rating"), 2) AS "Average Rating" FROM "longlist";

-- Finding maximum and minimum ratings
SELECT MAX("rating") FROM "longlist";
SELECT MIN("rating") FROM "longlist";

-- Finding total number of votes
SELECT SUM("votes") FROM "longlist";

-- Finding total number of books
SELECT COUNT(*) FROM "longlist";

-- Finding total number of translators
SELECT COUNT("translator") FROM "longlist";

-- Incorrectly counting publishers (counts all entries including duplicates)
SELECT COUNT("publisher") FROM "longlist";

-- Correctly counting unique publishers using DISTINCT
SELECT COUNT(DISTINCT "publisher") FROM "longlist"; -- Correct way to count unique publishers
