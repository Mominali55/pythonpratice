-- Demontrates joining tables with JOIN
-- Uses sea_lion.db

-- shows all sea lions for which we have data
SELECT * FROM "sea_lions"
JOIN "migrations" ON "migrations"."id" = "sea_lions"."id"; -- inner join

-- shows all sea lions ,wheather or not we have data or not
SELECT * FROM "sea_lions"
LEFT JOIN "migrations" ON "migrations"."id" = "sea_lions"."id"; -- left join

-- shows all data ,wheather or not there are matching sea lions
SELECT * FROM "sea_lions"
RIGHT JOIN "migrations" ON "migrations"."id" = "sea_lions"."id"; -- right join

-- shows all data and all sea lions
SELECT * FROM "sea_lions"
FULL JOIN "migrations" ON "migrations"."id" = "sea_lions"."id"; -- full join

-- JOINs sea lions and migrations without specifying matching column
SELECT * FROM "sea_lions"
NATURAL JOIN "migrations"; -- natural join

-- Uses WHERE after joining a table
SELECT * FROM "sea_lions"
JOIN "migrations" ON "migrations"."id" ="sea_lions"."id"
WHERE "migrations"."distance" > 1500;