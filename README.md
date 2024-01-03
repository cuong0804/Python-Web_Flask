# Python-
### Use database with postgreSQl 
CREATE TABLE Books (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    year_published INT,
    genre VARCHAR(100),
    quantity_available INT
);
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(50)
);
CREATE TABLE Loans (
    loan_id INT PRIMARY KEY,
    user_id INT,
    book_id INT,
    date_borrowed DATE,
    return_date DATE,
    date_returned DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);
INSERT INTO Books (book_id, title, author, year_published, genre, quantity_available) VALUES
(1, 'Book Title 1', 'Author A', 2000, 'Genre X', 5),
(2, 'Book Title 2', 'Author B', 2010, 'Genre Y', 3),
(3, 'Book Title 3', 'Author C', 1995, 'Genre Z', 8);
INSERT INTO Users (user_id, username, password, email, role) VALUES
(1, 'User1', 'hashed_password_1', 'user1@example.com', 'Regular'),
(2, 'User2', 'hashed_password_2', 'user2@example.com', 'Admin'),
(3, 'User3', 'hashed_password_3', 'user3@example.com', 'Regular');
INSERT INTO Loans (loan_id, user_id, book_id, date_borrowed, return_date, date_returned) VALUES
(1, 1, 1, '2023-01-01', '2023-01-15', NULL),
(2, 2, 2, '2023-02-01', '2023-02-15', '2023-02-14'),
(3, 3, 3, '2023-03-01', '2023-03-15', NULL);
### farmework Flask 
