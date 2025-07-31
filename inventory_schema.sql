CREATE DATABASE EKR_BookStore
  
USE EKR_BookStore;

CREATE TABLE InventoryManagement (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    BookName VARCHAR(255) NOT NULL,
    MarketPrice DECIMAL(10, 2) NOT NULL,
    Units INT NOT NULL
);




-- JEE/NEET Oriented E-Books
INSERT INTO InventoryManagement (BookName, MarketPrice, Units) VALUES
('DC Pandey-Physics', 2016, 50),
('HC Verma-Physics', 1410, 50),
('N. Avasthi-Physical Chemistry', 658, 50),
('MS Chauhan-Organic Chemistry', 692, 50),
('Bio 11 for NEET, AIIMS', 426, 50),
('Maths for JEE Mains and Advanced', 2920, 50),
('I.E. Irodov-Physics', 182, 50),
('JD Lee-Inorganic Chemistry', 790, 50);

-- Engineering E-Books
INSERT INTO InventoryManagement (BookName, MarketPrice, Units) VALUES
('Basic electrical engineering - Oxford', 575, 50),
('Basic electric and electronic engineering- RK Rajput', 996, 50),
('Dictionary of electrical engineering -Oxford', 1963, 50),
('Advanced computer architecture - Smruti R. Sarangi', 935, 50),
('Electronic Devices and Circuit Design', 10515, 50),
('Foundations of mechanical engineering', 7488, 50),
('Mechanical engineering designs - Lichard G. Budinas', 836, 50),
('Engineering Mechanics - Oxford', 545, 50);

-- Trading E-Books
INSERT INTO InventoryManagement (BookName, MarketPrice, Units) VALUES
('Encyclopedia of Charts Patterns', 3553, 50),
('How to Make Money in Stocks', 729, 50),
('The Intelligent Investor', 454, 50),
('Trend Following - Michael W. Covel', 2763, 50),
('Technical Analysis in the Financial Market', 2978, 50),
('NSE NISM Course', 3500, 50);

-- Additional E-Books
INSERT INTO InventoryManagement (BookName, MarketPrice, Units) VALUES
('Objective Electrical Technology - S. Chand pub.', 559, 50),
('Principles of Electrical engineering V. Bush', 2765, 50),
('Core python programming - Dr. R. Nageshwara Rao', 705, 50),
('Machine learning using Python', 605, 50),
('Core Java programming - Dr. R. Nageshwara Rao', 590, 50),
('Data structure and algorithms in Java - Wiley pub.', 2099, 50),
('Notes in Mechanical engineering - Henry Adams', 2142, 50),
('Basic mechanical engineering - RK Rajput', 495, 50);





CREATE TABLE CustomerData (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    BookOrdered VARCHAR(255) NOT NULL,
    BookPrice DECIMAL(10, 2) NOT NULL,
    PaymentStatus ENUM('Paid', 'Pending', 'Failed') NOT NULL
);
