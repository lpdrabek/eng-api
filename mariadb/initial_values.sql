use eng_api;

CREATE TABLE author (
     id INTEGER(20) NOT NULL AUTO_INCREMENT,
     full_name VARCHAR(190) NOT NULL UNIQUE,
     birth_date DATE DEFAULT "0000-00-00",
     death_date DATE DEFAULT "0000-00-00",
     gender VARCHAR(1) DEFAULT NULL,
     CONSTRAINT pk_author PRIMARY KEY (id)
     );

CREATE TABLE book (
     id INTEGER(20) NOT NULL AUTO_INCREMENT,
     title VARCHAR(190) NOT NULL UNIQUE,
     isbn VARCHAR(17) DEFAULT NULL UNIQUE,
     book_read INTEGER(1) NOT NULL DEFAULT 0,
     authorid INTEGER(20) NOT NULL,
     CONSTRAINT pk_book_id PRIMARY KEY (id),
     CONSTRAINT fk_book_author FOREIGN KEY (authorid) 
     REFERENCES author (id) ON DELETE CASCADE
     );

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

