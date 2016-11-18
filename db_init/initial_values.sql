use eng_api;

source db_schema.sql

INSERT INTO author (id, full_name, birth_date, death_date, gender) 
            VALUES (1, "Henryk Sienkiewicz", "1846-05-05", NULL, "M")
                 , (2, "Jan Brzechwa", NULL, NULL, "M")
                 , (3, "Astrid Lindgren", "1907-11-14", "2002-01-28", "F");

INSERT INTO book (id, title, isbn, book_read, authorid) 
          VALUES (1, "Ogniem i Mieczem", "83-86858-83-4", 1, 1)
               , (2, "Pan Wolodyjowski", "83-86858-68-0", 0, 1)
               , (3, "Akademia Pana Kleksa", "978-8-3751-7445-8", 1, 2)
               , (4, "Sto Bajek", NULL, 1, 2)
               , (5, "Podroze Pana Kleksa", NULL, 0, 2)
               , (6, "Dzieci z Bullerbyn", NULL, 1, 3);
