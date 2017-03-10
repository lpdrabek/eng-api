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

