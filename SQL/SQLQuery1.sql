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
