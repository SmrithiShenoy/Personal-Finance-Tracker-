DELIMITER $$
-- SECTION 1: DDL - DATA DEFINITION LANGUAGE (CREATE TABLES)

CREATE TABLE USER (
    USERID VARCHAR(20) PRIMARY KEY,
    EmailID VARCHAR(100) UNIQUE NOT NULL,
    Name VARCHAR(100),
    PWD VARCHAR(50) NOT NULL,
    DOB DATE
);

CREATE TABLE PHONE (
    USERID VARCHAR(20),
    Phone VARCHAR(15),
    PRIMARY KEY (USERID, Phone),
    FOREIGN KEY (USERID) REFERENCES USER(USERID)
);

CREATE TABLE ACCOUNTS (
    ACCID VARCHAR(20) PRIMARY KEY,
    USERID VARCHAR(20) NOT NULL,
    AccNa VARCHAR(100) NOT NULL,
    Type VARCHAR(50),
    Curren_Bal DECIMAL(10, 2),
    FOREIGN KEY (USERID) REFERENCES USER(USERID)
);

CREATE TABLE GOALS (
    GID VARCHAR(20) PRIMARY KEY,
    USERID VARCHAR(20) NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Target DECIMAL(10, 2),
    Deadline DATE,
    FOREIGN KEY (USERID) REFERENCES USER(USERID)
);

CREATE TABLE CATEGORY (
    CID VARCHAR(20) PRIMARY KEY,
    C_Name VARCHAR(50) UNIQUE NOT NULL,
    Type VARCHAR(20) CHECK (Type IN ('Expense', 'Income', 'Transfer')),
    Description VARCHAR(255)
);

CREATE TABLE BUDGET (
    BID VARCHAR(20) PRIMARY KEY,
    USERID VARCHAR(20) NOT NULL,
    CID VARCHAR(20) NOT NULL,
    Month INT NOT NULL CHECK (Month BETWEEN 1 AND 12),
    Year INT NOT NULL,
    Limit_Amt DECIMAL(10, 2) NOT NULL,
    UNIQUE (USERID, CID, Month, Year),
    FOREIGN KEY (USERID) REFERENCES USER(USERID),
    FOREIGN KEY (CID) REFERENCES CATEGORY(CID)
);

CREATE TABLE TRANSACTION (
    ACCID VARCHAR(20) NOT NULL,
    TXID VARCHAR(20) NOT NULL,
    CID VARCHAR(20) NOT NULL,
    expense DECIMAL(10, 2) NOT NULL,
    mode VARCHAR(50),
    time DATETIME,
    PRIMARY KEY (ACCID, TXID),
    FOREIGN KEY (ACCID) REFERENCES ACCOUNTS(ACCID),
    FOREIGN KEY (CID) REFERENCES CATEGORY(CID)
);

CREATE TABLE SETS (
    USERID VARCHAR(20) NOT NULL,
    BID VARCHAR(20) NOT NULL,
    PRIMARY KEY (USERID, BID),
    FOREIGN KEY (USERID) REFERENCES USER(USERID),
    FOREIGN KEY (BID) REFERENCES BUDGET(BID)
);




-- SECTION 2: DML - DATA MANIPULATION LANGUAGE (INSERT/CRUD)


INSERT INTO USER (USERID, EmailID, Name, PWD, DOB) VALUES
('U001', 'alice@mail.com', 'Alice Smith', 'hash1', '1990-05-15'),
('U002', 'bob@mail.com', 'Bob Johnson', 'hash2', '1985-11-20'),
('U003', 'charlie@mail.com', 'Charlie Brown', 'hash3', '1998-03-01'),
('U004', 'diana@mail.com', 'Diana Prince', 'hash4', '1993-07-25'),
('U005', 'eve@mail.com', 'Eve Adams', 'hash5', '1982-01-10'),
('U006', 'frank@mail.com', 'Frank Green', 'hash6', '1975-04-12'),
('U007', 'grace@mail.com', 'Grace Hall', 'hash7', '2000-09-03'),
('U008', 'henry@mail.com', 'Henry King', 'hash8', '1991-12-30'),
('U009', 'ivy@mail.com', 'Ivy Lane', 'hash9', '1987-06-18'),
('U010', 'jack@mail.com', 'Jack Miller', 'hash10', '1995-02-28'),
('U011', 'kathy@mail.com', 'Kathy Nolan', 'hash11', '1989-10-05'),
('U012', 'liam@mail.com', 'Liam Ortiz', 'hash12', '1992-08-14'),
('U013', 'mia@mail.com', 'Mia Patel', 'hash13', '1997-04-04'),
('U014', 'noah@mail.com', 'Noah Quinn', 'hash14', '1980-11-11'),
('U015', 'olivia@mail.com', 'Olivia Reed', 'hash15', '1996-01-22'),
('U016', 'peter@mail.com', 'Peter Scott', 'hash16', '1983-05-29'),
('U017', 'quinn@mail.com', 'Quinn Terry', 'hash17', '1994-07-19'),
('U018', 'rachel@mail.com', 'Rachel Uzzo', 'hash18', '1978-03-08'),
('U019', 'sam@mail.com', 'Sam Vance', 'hash19', '1999-10-27'),
('U020', 'tina@mail.com', 'Tina White', 'hash20', '1988-06-06');

INSERT INTO Phone (USERID, Phone) VALUES
('U001', '555-123-4001'), ('U001', '555-123-4002'),
('U002', '555-234-4003'), ('U003', '555-345-4004'),
('U004', '555-456-4005'), ('U004', '555-456-4006'),
('U005', '555-567-4007'), ('U006', '555-678-4008'),
('U007', '555-789-4009'), ('U008', '555-890-4010'),
('U009', '555-012-4011'), ('U010', '555-111-4012'),
('U011', '555-222-4013'), ('U012', '555-333-4014'),
('U013', '555-444-4015'), ('U014', '555-555-4016'),
('U015', '555-666-4017'), ('U016', '555-777-4018'),
('U017', '555-888-4019'), ('U018', '555-999-4020');

INSERT INTO Category (CID, C_Name, Type, description) VALUES
('C001', 'Rent/Mortgage', 'Expense', 'Monthly housing payment'),
('C002', 'Groceries', 'Expense', 'Food and household essentials'),
('C003', 'Salary', 'Income', 'Monthly paycheck'),
('C004', 'Entertainment', 'Expense', 'Movies, concerts, subscriptions'),
('C005', 'Transport', 'Expense', 'Fuel, public transit, car maintenance'),
('C006', 'Eating Out', 'Expense', 'Restaurants and takeout'),
('C007', 'Utilities', 'Expense', 'Electricity, water, internet'),
('C008', 'Healthcare', 'Expense', 'Doctor visits, insurance, meds'),
('C009', 'Investment Gain', 'Income', 'Profit from stocks/funds'),
('C010', 'Clothing', 'Expense', 'New apparel and accessories'),
('C011', 'Savings Transfer', 'Expense', 'Transfer to dedicated savings'),
('C012', 'Education', 'Expense', 'Tuition, books, courses'),
('C013', 'Gifts Given', 'Expense', 'Presents for others'),
('C014', 'Interest Income', 'Income', 'Interest earned on savings'),
('C015', 'Travel', 'Expense', 'Flights, hotels, vacation costs'),
('C016', 'Pet Care', 'Expense', 'Food, vet, toys'),
('C017', 'Home Repairs', 'Expense', 'Maintenance and fixes'),
('C018', 'Freelance Income', 'Income', 'Payment for side gigs'),
('C019', 'Personal Care', 'Expense', 'Haircuts, toiletries, gym'),
('C020', 'Refunds', 'Income', 'Money back from purchases');

INSERT INTO Accounts (ACCID, USERID, AccNa, Type, Curren_Bal) VALUES
('A001', 'U001', 'Checking - Primary', 'Checking', 5500.25),
('A002', 'U001', 'Savings - Emergency', 'Savings', 12000.00),
('A003', 'U002', 'Joint Checking', 'Checking', 8100.50),
('A004', 'U003', 'Student Account', 'Checking', 950.75),
('A005', 'U004', 'Main Savings', 'Savings', 30000.00),
('A006', 'U005', 'Business Checking', 'Checking', 15200.00),
('A007', 'U006', 'Retirement Fund', 'Investment', 75000.00),
('A008', 'U007', 'Travel Savings', 'Savings', 1500.00),
('A009', 'U008', 'Debit Card Account', 'Checking', 3200.40),
('A010', 'U009', 'High Yield Savings', 'Savings', 25000.00),
('A011', 'U010', 'Cash Envelope', 'Cash', 500.00),
('A012', 'U011', 'Home Mortgage', 'Loan', -150000.00),
('A013', 'U012', 'Primary Checking', 'Checking', 4100.80),
('A014', 'U013', 'Side Hustle Cash', 'Checking', 1200.00),
('A015', 'U014', 'Kids College Fund', 'Investment', 5000.00),
('A016', 'U015', 'Main Checking', 'Checking', 7200.10),
('A017', 'U016', 'Rainy Day Fund', 'Savings', 800.00),
('A018', 'U017', 'Personal Checking', 'Checking', 2150.30),
('A019', 'U018', 'Brokerage Account', 'Investment', 45000.00),
('A020', 'U019', 'Small Checking', 'Checking', 650.99);

INSERT INTO Goals (GID, USERID, title, Target, deadline) VALUES
('G001', 'U001', 'Down Payment', 50000.00, '2026-12-31'),
('G002', 'U002', 'New Car Fund', 15000.00, '2025-10-01'),
('G003', 'U003', 'Pay Off Student Loan', 8000.00, '2024-12-31'),
('G004', 'U004', 'European Trip', 4500.00, '2025-07-01'),
('G005', 'U005', 'Retirement Boost', 100000.00, '2035-01-01'),
('G006', 'U006', 'New Laptop', 1500.00, '2024-11-30'),
('G007', 'U007', 'Emergency Buffer', 2000.00, '2024-10-31'),
('G008', 'U008', 'Home Renovation', 25000.00, '2026-06-01'),
('G009', 'U009', 'Invest 20k', 20000.00, '2025-03-01'),
('G010', 'U010', 'Wedding Fund', 30000.00, '2027-08-01'),
('G011', 'U011', 'Clear Credit Card Debt', 5000.00, '2024-12-31'),
('G012', 'U012', 'Sabbatical Fund', 7000.00, '2025-11-01'),
('G013', 'U013', 'Business Equipment', 3000.00, '2024-10-31'),
('G014', 'U014', 'New TV', 1200.00, '2024-12-01'),
('G015', 'U015', 'Charity Donation', 500.00, '2025-01-01'),
('G016', 'U016', 'Buy a Bike', 800.00, '2025-05-01'),
('G017', 'U017', 'Save for Tax', 2500.00, '2025-04-15'),
('G018', 'U018', 'Kids Summer Camp', 1000.00, '2025-06-01'),
('G019', 'U019', 'New Phone', 1000.00, '2024-11-30'),
('G020', 'U020', 'Kitchen Gadgets', 500.00, '2024-10-31');

INSERT INTO Budget (BID, USERID, CID, Month, Year, Limit_Amt) VALUES
('B001', 'U001', 'C001', 10, 2024, 1500.00), -- Alice, Rent, Oct 2024
('B002', 'U001', 'C002', 10, 2024, 400.00),  -- Alice, Groceries, Oct 2024
('B003', 'U002', 'C006', 10, 2024, 250.00),  -- Bob, Eating Out, Oct 2024
('B004', 'U003', 'C005', 10, 2024, 150.00),  -- Charlie, Transport, Oct 2024
('B005', 'U004', 'C004', 10, 2024, 100.00),  -- Diana, Entertainment, Oct 2024
('B006', 'U005', 'C007', 10, 2024, 300.00),  -- Eve, Utilities, Oct 2024
('B007', 'U006', 'C010', 10, 2024, 50.00),   -- Frank, Clothing, Oct 2024
('B008', 'U007', 'C002', 10, 2024, 350.00),  -- Grace, Groceries, Oct 2024
('B009', 'U008', 'C008', 10, 2024, 150.00),  -- Henry, Healthcare, Oct 2024
('B010', 'U009', 'C015', 10, 2024, 200.00),  -- Ivy, Travel, Oct 2024
('B011', 'U001', 'C002', 11, 2024, 450.00),  -- Alice, Groceries, Nov 2024
('B012', 'U010', 'C006', 10, 2024, 180.00),  -- Jack, Eating Out, Oct 2024
('B013', 'U011', 'C001', 10, 2024, 1200.00), -- Kathy, Rent, Oct 2024
('B014', 'U012', 'C019', 10, 2024, 80.00),   -- Liam, Personal Care, Oct 2024
('B015', 'U013', 'C005', 10, 2024, 100.00),  -- Mia, Transport, Oct 2024
('B016', 'U014', 'C016', 10, 2024, 60.00),   -- Noah, Pet Care, Oct 2024
('B017', 'U015', 'C004', 10, 2024, 120.00),  -- Olivia, Entertainment, Oct 2024
('B018', 'U016', 'C012', 10, 2024, 50.00),   -- Peter, Education, Oct 2024
('B019', 'U017', 'C006', 10, 2024, 150.00),  -- Quinn, Eating Out, Oct 2024
('B020', 'U018', 'C007', 10, 2024, 250.00);  -- Rachel, Utilities, Oct 2024

INSERT INTO Transaction (TXID, ACCID, CID, expense, mode, time) VALUES
('T001', 'A001', 'C001', 1500.00, 'Transfer', '2024-10-01 09:00:00'),
('T002', 'A001', 'C002', 55.20, 'Card', '2024-10-02 11:30:00'),
('T003', 'A003', 'C006', 35.75, 'Card', '2024-10-02 19:45:00'),
('T004', 'A004', 'C005', 12.50, 'Cash', '2024-10-03 08:00:00'),
('T005', 'A005', 'C014', -15.00, 'Transfer', '2024-10-03 14:00:00'), -- Income is negative expense
('T006', 'A006', 'C018', -1500.00, 'Transfer', '2024-10-04 10:00:00'),
('T007', 'A007', 'C009', -120.00, 'Transfer', '2024-10-04 11:00:00'),
('T008', 'A008', 'C015', 75.00, 'Card', '2024-10-04 16:30:00'),
('T009', 'A009', 'C004', 19.99, 'Card', '2024-10-05 20:00:00'),
('T010', 'A010', 'C011', 500.00, 'Transfer', '2024-10-06 09:30:00'),
('T011', 'A011', 'C002', 40.00, 'Cash', '2024-10-06 13:00:00'),
('T012', 'A012', 'C001', 1200.00, 'Transfer', '2024-10-07 09:00:00'),
('T013', 'A013', 'C005', 85.00, 'Card', '2024-10-07 10:30:00'),
('T014', 'A014', 'C010', 45.99, 'Card', '2024-10-07 15:00:00'),
('T015', 'A015', 'C012', 300.00, 'Transfer', '2024-10-08 08:00:00'),
('T016', 'A016', 'C007', 88.50, 'Card', '2024-10-08 11:45:00'),
('T017', 'A017', 'C013', 25.00, 'Card', '2024-10-09 13:30:00'),
('T018', 'A018', 'C016', 15.75, 'Card', '2024-10-09 17:00:00'),
('T019', 'A019', 'C003', -3500.00, 'Transfer', '2024-10-10 09:00:00'),
('T020', 'A020', 'C002', 30.15, 'Card', '2024-10-10 12:15:00');

INSERT INTO Sets (USERID, BID) VALUES
('U001', 'B001'), ('U001', 'B002'),
('U001', 'B011'), ('U002', 'B003'),
('U003', 'B004'), ('U004', 'B005'),
('U005', 'B006'), ('U006', 'B007'),
('U007', 'B008'), ('U008', 'B009'),
('U009', 'B010'), ('U010', 'B012'),
('U011', 'B013'), ('U012', 'B014'),
('U013', 'B015'), ('U014', 'B016'),
('U015', 'B017'), ('U016', 'B018'),
('U017', 'B019'), ('U018', 'B020');

-- Example CRUD Queries:

SELECT Name, EmailID FROM USER WHERE USERID = 'U001';

UPDATE Budget
SET Limit_Amt = 300.00
WHERE BID = 'B003';

DELETE FROM Goals
WHERE GID = 'G002';


-- SECTION 3: TRIGGERS, FUNCTIONS, AND PROCEDURES


-- A. TRIGGER: trg_update_account_balance_simple 
CREATE TRIGGER trg_update_account_balance_simple
AFTER INSERT ON TRANSACTION
FOR EACH ROW
BEGIN
    UPDATE Accounts
    SET Curren_Bal = Curren_Bal - NEW.expense
    WHERE ACCID = NEW.ACCID;
END $$

-- B. FUNCTION: GetAccountBalance 
CREATE FUNCTION GetAccountBalance (
    acc_id_in VARCHAR(10)
)
RETURNS DECIMAL(10, 2)
READS SQL DATA
BEGIN
    DECLARE balance DECIMAL(10, 2);

    SELECT Curren_Bal
    INTO balance
    FROM Accounts
    WHERE ACCID = acc_id_in;

    RETURN COALESCE(balance, 0.00);
END $$

-- C. PROCEDURE: LogNewExpense 
CREATE PROCEDURE LogNewExpense (
    IN acc_id_in VARCHAR(10),
    IN cid_in VARCHAR(10),
    IN expense_amt DECIMAL(10, 2),
    IN txid_in VARCHAR(20)
)
BEGIN
    INSERT INTO TRANSACTION (TXID, ACCID, CID, expense, mode, time)
    VALUES (
        txid_in,
        acc_id_in,
        cid_in,
        expense_amt,
        'Manual Entry',
        NOW()
    );
END $$


-- SECTION 4: COMPLEX QUERIES (NESTED, JOIN, AGGREGATE)


-- A. NESTED QUERY: Find users who set a budget limit greater than the overall average limit.
SELECT
    U.Name
FROM
    USER AS U
JOIN
    Budget AS B ON U.USERID = B.USERID
WHERE
    B.Limit_Amt > (
        SELECT AVG(Limit_Amt)
        FROM Budget
    )
GROUP BY
    U.Name;

-- B. JOIN QUERY: List all Groceries transactions with the Account Name and User Name.
SELECT
    U.Name AS User_Name,
    A.AccNa AS Account_Name,
    T.expense AS Expense_Amount,
    T.time AS Transaction_Date
FROM
    TRANSACTION AS T
JOIN
    Accounts AS A ON T.ACCID = A.ACCID
JOIN
    USER AS U ON A.USERID = U.USERID
JOIN
    Category AS C ON T.CID = C.CID
WHERE
    C.C_Name = 'Groceries'
ORDER BY
    T.time DESC;

-- C. AGGREGATE QUERY: Calculate the Total Spending (SUM) grouped by Category for Oct.
SELECT
    C.C_Name AS Category_Name,
    SUM(T.expense) AS Total_Spent_Oct
FROM
    TRANSACTION AS T
JOIN
    Category AS C ON T.CID = C.CID
WHERE
    T.expense > 0
    AND MONTH(T.time) = 10
    AND YEAR(T.time) = 2024
GROUP BY
    C.C_Name
ORDER BY
    Total_Spent_Oct_2024 DESC;

DELIMITER ;