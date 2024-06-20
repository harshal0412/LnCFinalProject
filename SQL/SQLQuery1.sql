USE LnC;

CREATE TABLE Users (
    Emp_id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('admin', 'chef', 'employee')) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Menu (
    ID INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    availability BIT NOT NULL
);
 
 CREATE TABLE Feedback (
    ID INT PRIMARY KEY IDENTITY(1,1),
    menu_id int,
    Emp_id int,
    comment VARCHAR(255),
	rating float,
	date date
);

CREATE TABLE Notification (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Emp_id INT,
    message VARCHAR(255),
    is_read bit,
    sentdate DATE
);

CREATE TABLE ChefRecommandation (
    ID INT PRIMARY KEY IDENTITY(1,1),
    menu_id INT,
    type VARCHAR(15) CHECK (type IN ('Breakfast', 'Lunch', 'Dinner')) NOT NULL,
    sentdate DATE
);

CREATE TABLE EmpChoice (
    ID INT PRIMARY KEY IDENTITY(1,1),
    ChefRecommandation_id INT,
	Choice bit,
	Emp_id int,
	menu_id int
);



INSERT INTO Menu (name, price, availability)
VALUES 
-- Breakfast items
('Masala Dosa', 4.50, 1),
('Idli', 3.00, 1),
('Aloo Paratha', 5.00, 1),
('Poha', 3.50, 1),
('Upma', 3.00, 1),
-- Lunch items
('Chicken Biryani', 10.00, 1),
('Paneer Butter Masala', 8.00, 1),
('Dal Makhani', 6.50, 1),
('Roti', 1.00, 1),
('Vegetable Pulao', 7.00, 1),
-- Dinner items
('Butter Chicken', 12.00, 1),
('Fish Curry', 11.00, 1),
('Chole Bhature', 9.00, 1),
('Mutton Rogan Josh', 13.00, 1),
('Palak Paneer', 8.50, 1),
-- Snacks and Others
('Samosa', 1.50, 1),
('Pakora', 2.50, 1),
('Pani Puri', 3.00, 1),
('Gulab Jamun', 4.00, 1),
('Jalebi', 3.50, 1);

INSERT INTO Users (name, role, password)
VALUES 
('Rakshit jain', 'chef', 'chef'),
('Anita Sharma', 'employee', 'emp789'),
('Vikram Patel', 'employee', 'emp456'),
('Priya Iyer', 'employee', 'emp123');

delete from Users where Emp_id=5 

INSERT INTO Feedback (menu_id, Emp_id, comment, rating, date)
VALUES 
(1, 1, 'Delicious and crispy', 4.5, '2024-06-01'),
(2, 2, 'Very soft and tasty', 4.0, '2024-06-02'),
(3, 3, 'Too spicy for my taste', 2.5, '2024-06-03'),
(4, 6, 'Light and refreshing', 4.2, '2024-06-04'),
(5, 7, 'Not very flavorful', 2.8, '2024-06-05'),
(6, 8, 'Flavorful and aromatic', 4.7, '2024-06-06'),
(7, 9, 'Too oily', 3.0, '2024-06-07'),
(8, 1, 'Smooth and flavorful', 4.3, '2024-06-08'),
(9, 2, 'Overcooked and dry', 2.9, '2024-06-09'),
(10, 3, 'Well-balanced flavors', 4.1, '2024-06-10'),
(11, 6, 'Juicy and tender', 4.9, '2024-06-11'),
(12, 7, 'Spicy and tangy', 4.4, '2024-06-12'),
(13, 8, 'Too salty', 3.2, '2024-06-13'),
(14, 9, 'Rich and hearty', 4.8, '2024-06-14'),
(15, 1, 'Creamy and delicious', 4.5, '2024-06-15'),
(16, 2, 'Crispy and spicy', 3.7, '2024-06-16'),
(17, 3, 'Too bland', 2.6, '2024-06-17'),
(18, 6, 'Refreshing and spicy', 4.3, '2024-06-18'),
(19, 7, 'Sweet and soft', 4.6, '2024-06-19'),
(20, 8, 'Too sweet for my liking', 3.5, '2024-06-20');

-- Create the ChefRecommandation table
CREATE TABLE ChefRecommandedmenu (
    ID INT PRIMARY KEY IDENTITY(1,1),
    menu_id INT,
    type VARCHAR(15) CHECK (type IN ('Breakfast', 'Lunch', 'Dinner')) NOT NULL,
    sentdate DATE
);

-- Insert test data into the ChefRecommandation table
INSERT INTO ChefRecommandedmenu (menu_id, type, sentdate)
VALUES 
(1, 'Breakfast', '2024-06-01'),
(2, 'Breakfast', '2024-06-02'),
(3, 'Lunch', '2024-06-03'),
(4, 'Lunch', '2024-06-04'),
(5, 'Dinner', '2024-06-05'),
(6, 'Dinner', '2024-06-06');

-- Create the EmpChoice table
CREATE TABLE EmpChoice (
    ID INT PRIMARY KEY IDENTITY(1,1),
    ChefRecommandation_id INT,
    Choice BIT,
    Emp_id INT,
    menu_id INT
);

-- Insert test data into the EmpChoice table
INSERT INTO EmpChoice (ChefRecommandation_id, Choice, Emp_id, menu_id)
VALUES 
(1, 1, 1, 1), -- Harshal chooses Masala Dosa for breakfast
(2, 1, 2, 2), -- Ron chooses Idlis for breakfast
(3, 1, 3, 3), -- Test chooses Butter Chicken for lunch
(4, 1, 6, 4), -- Anita Sharma chooses Paneer Butter Masala for lunch
(5, 1, 7, 5), -- Vikram Patel chooses Biryani for dinner
(6, 1, 8, 6); -- Priya Iyer chooses Dal Makhani for dinner
