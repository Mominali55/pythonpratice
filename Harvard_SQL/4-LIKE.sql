-- Find all books with "love" in the title
SELECT "title" FROM "longlist" WHERE "title" LIKE '%love%'; --Here using uppercase 'LOVE' will work as it is not case sensitive

-- Find all books that begin with "The" (includes "There", etc.)
SELECT "title" FROM "longlist" WHERE "title" LIKE 'The%';

-- Find all books that begin with "The" only
SELECT "title" FROM "longlist" WHERE "title" LIKE 'The %';

-- Find a book whose title unsure how to spell
SELECT "title" FROM "longlist" WHERE "title" LIKE 'P_re';