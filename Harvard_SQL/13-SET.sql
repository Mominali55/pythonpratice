-- Demonstartes set operations 
-- Uses lomglist.db
-- Also have to connect csv files

-- UNION
-- select all translater, labeling as translators 
SELECT 'author' AS "profession","name" FROM "authors";

-- Select all translater,labeling as translators
SELECT 'translator' AS "profession", "name" FROM "translators";

-- Combines authors and translators into one result set
SELECT 'author' AS "profession", "name" FROM "authors";
UNION
SELECT 'translator' AS "profession", "name" FROM "translators";

-- INTERSECT (assuming name are unique)
-- Finding name from authors and translater
SELECT "name" FROM "authors"
INTERSECT
SELECT "name" FROM "tanslators";

-- Find boks translated by sophie hughes
SELECT "book_id" FROM "tanslated" WHERE "translator_id" = (
    SELECT "id" FROM "translators" WHERE name = 'Margaret Jull Costa'
);

-- Finds intersection of books
SELECT "book_id" FROM "translated" WHERE "translator_id" = (
    SELECT "id" FROM "translators" WHERE name = 'Sophie Hughes'
)
INTERSECT
SELECT "book_id" FROM "translated" WHERE "translator_id" = (
    SELECT "id" FROM "translators" WHERE name = 'Margaret Jull Costa'
);

-- Finds intersection of books 
SELECT "title" FROM "books" WHERE "id" = (
    SELECT "book_id" FROM "translated" WHERE "translator_id" = (
        SELECT "id" FROM "tanslators" WHERE name = 'Sophie hughes'
    )
    INTERSECT
    SELECT "book_id" FROM "translated" WHERE "translator_id" = (
        select "id" FROM "translators" WHERE name = 'Margaret Jull Costa'
    )
);

-- EXCEPT (Assume names are unique)
-- Finds translators who are not authors
SELECT "name" FROM "translators"
EXCEPT
SELECT "name" FROM "authors";