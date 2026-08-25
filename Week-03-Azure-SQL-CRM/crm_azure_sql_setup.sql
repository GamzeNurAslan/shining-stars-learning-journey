/* =========================================================
   SHINING STARS - WEEK 03
   Azure SQL & CRM Analytics
   ========================================================= */


/* 1. TABLES */

IF OBJECT_ID('dbo.CustomerSegments', 'U') IS NULL
BEGIN
    CREATE TABLE CustomerSegments (
        SegmentID INT PRIMARY KEY,
        SegmentName NVARCHAR(50) NOT NULL,
        SegmentDescription NVARCHAR(200)
    );
END;


IF OBJECT_ID('dbo.ProductCategories', 'U') IS NULL
BEGIN
    CREATE TABLE ProductCategories (
        CategoryID INT PRIMARY KEY,
        CategoryName NVARCHAR(100) NOT NULL
    );
END;


IF OBJECT_ID('dbo.Products', 'U') IS NULL
BEGIN
    CREATE TABLE Products (
        ProductID INT PRIMARY KEY,
        ProductName NVARCHAR(100) NOT NULL,
        CategoryID INT,
        UnitPrice DECIMAL(12,2),

        CONSTRAINT FK_Products_Categories
            FOREIGN KEY (CategoryID)
            REFERENCES ProductCategories(CategoryID)
    );
END;


IF OBJECT_ID('dbo.Channels', 'U') IS NULL
BEGIN
    CREATE TABLE Channels (
        ChannelID INT PRIMARY KEY,
        ChannelName NVARCHAR(50) NOT NULL
    );
END;


IF OBJECT_ID('dbo.Customers', 'U') IS NULL
BEGIN
    CREATE TABLE Customers (
        CustomerID INT PRIMARY KEY,
        CustomerName NVARCHAR(100),
        Age INT,
        Gender NVARCHAR(20),
        City NVARCHAR(50),
        JoinDate DATE,
        CustomerStatus NVARCHAR(30),
        ChurnStatus BIT DEFAULT 0,
        ChurnDate DATE NULL,
        Segment NVARCHAR(50),
        SegmentID INT NULL,

        CONSTRAINT FK_Customers_Segments
            FOREIGN KEY (SegmentID)
            REFERENCES CustomerSegments(SegmentID)
    );
END;


IF OBJECT_ID('dbo.Leads', 'U') IS NULL
BEGIN
    CREATE TABLE Leads (
        LeadID INT PRIMARY KEY,
        LeadName NVARCHAR(100),
        LeadSource NVARCHAR(50),
        LeadStatus NVARCHAR(50),
        Converted BIT DEFAULT 0,
        ConvertedDate DATE NULL
    );
END;


IF OBJECT_ID('dbo.Sales', 'U') IS NULL
BEGIN
    CREATE TABLE Sales (
        SaleID INT IDENTITY(1,1) PRIMARY KEY,
        OrderID INT,
        CustomerID INT NOT NULL,
        SaleDate DATE,
        ProductID INT NULL,
        ProductCategory NVARCHAR(100),
        ProductName NVARCHAR(100),
        Quantity INT,
        UnitPrice DECIMAL(12,2),
        TotalAmount DECIMAL(12,2),
        DiscountRate DECIMAL(5,2) DEFAULT 0,
        DiscountAmount DECIMAL(12,2) DEFAULT 0,
        NetAmount DECIMAL(12,2),
        SalesChannel NVARCHAR(50),

        CONSTRAINT FK_Sales_Customers
            FOREIGN KEY (CustomerID)
            REFERENCES Customers(CustomerID),

        CONSTRAINT FK_Sales_Products
            FOREIGN KEY (ProductID)
            REFERENCES Products(ProductID)
    );
END;


IF OBJECT_ID('dbo.Interactions', 'U') IS NULL
BEGIN
    CREATE TABLE Interactions (
        InteractionID INT IDENTITY(1,1) PRIMARY KEY,
        CustomerID INT NOT NULL,
        InteractionDate DATE,
        Channel NVARCHAR(30),
        InteractionType NVARCHAR(50),
        Outcome NVARCHAR(50),

        CONSTRAINT FK_Interactions_Customers
            FOREIGN KEY (CustomerID)
            REFERENCES Customers(CustomerID)
    );
END;


IF OBJECT_ID('dbo.SupportTickets', 'U') IS NULL
BEGIN
    CREATE TABLE SupportTickets (
        TicketID INT PRIMARY KEY,
        CustomerID INT NOT NULL,
        OpenDate DATE,
        CloseDate DATE NULL,
        IssueCategory NVARCHAR(100),
        Priority NVARCHAR(30),
        TicketStatus NVARCHAR(30),
        SatisfactionScore DECIMAL(3,2),

        CONSTRAINT FK_SupportTickets_Customers
            FOREIGN KEY (CustomerID)
            REFERENCES Customers(CustomerID)
    );
END;


IF OBJECT_ID('dbo.Campaigns', 'U') IS NULL
BEGIN
    CREATE TABLE Campaigns (
        CampaignID INT PRIMARY KEY,
        CampaignName NVARCHAR(100),
        CampaignType NVARCHAR(50),
        Budget DECIMAL(12,2),
        StartDate DATE,
        EndDate DATE
    );
END;


IF OBJECT_ID('dbo.CampaignResponses', 'U') IS NULL
BEGIN
    CREATE TABLE CampaignResponses (
        ResponseID INT IDENTITY(1,1) PRIMARY KEY,
        CampaignID INT NOT NULL,
        CustomerID INT NOT NULL,
        ResponseDate DATE,
        ResponseType NVARCHAR(50),
        Converted BIT DEFAULT 0,
        RevenueAttributed DECIMAL(12,2) DEFAULT 0,

        CONSTRAINT FK_CampaignResponses_Campaigns
            FOREIGN KEY (CampaignID)
            REFERENCES Campaigns(CampaignID),

        CONSTRAINT FK_CampaignResponses_Customers
            FOREIGN KEY (CustomerID)
            REFERENCES Customers(CustomerID)
    );
END;


/* 2. SAMPLE LOOKUP DATA */

IF NOT EXISTS (SELECT 1 FROM CustomerSegments)
BEGIN
    INSERT INTO CustomerSegments
        (SegmentID, SegmentName, SegmentDescription)
    VALUES
        (1, 'Individual', 'Individual retail customers'),
        (2, 'SME', 'Small and medium-sized enterprises'),
        (3, 'Corporate', 'Corporate customers');
END;


IF NOT EXISTS (SELECT 1 FROM ProductCategories)
BEGIN
    INSERT INTO ProductCategories
        (CategoryID, CategoryName)
    VALUES
        (1, 'Laptop'),
        (2, 'Smartphone'),
        (3, 'Smartwatch'),
        (4, 'Headphones'),
        (5, 'Accessories');
END;


IF NOT EXISTS (SELECT 1 FROM Products)
BEGIN
    INSERT INTO Products
        (ProductID, ProductName, CategoryID, UnitPrice)
    VALUES
        (1, 'Pro Laptop', 1, 35000),
        (2, 'Smartphone X', 2, 22000),
        (3, 'Smartwatch Pro', 3, 8500),
        (4, 'Wireless Headphones', 4, 4500),
        (5, 'Tech Accessories Pack', 5, 2000);
END;


IF NOT EXISTS (SELECT 1 FROM Channels)
BEGIN
    INSERT INTO Channels
        (ChannelID, ChannelName)
    VALUES
        (1, 'Online'),
        (2, 'Store'),
        (3, 'Mobile App'),
        (4, 'Call Center'),
        (5, 'Email'),
        (6, 'Social Media');
END;


/* 3. DATA CONTROL */

SELECT 'Customers' AS TableName, COUNT(*) AS RecordCount
FROM Customers

UNION ALL

SELECT 'Leads', COUNT(*)
FROM Leads

UNION ALL

SELECT 'Sales', COUNT(*)
FROM Sales

UNION ALL

SELECT 'Interactions', COUNT(*)
FROM Interactions

UNION ALL

SELECT 'SupportTickets', COUNT(*)
FROM SupportTickets

UNION ALL

SELECT 'Campaigns', COUNT(*)
FROM Campaigns

UNION ALL

SELECT 'CampaignResponses', COUNT(*)
FROM CampaignResponses;


/* 4. CUSTOMER SUMMARY */

SELECT
    COUNT(*) AS TotalCustomers,

    SUM(
        CASE
            WHEN CustomerStatus = 'Active'
            THEN 1
            ELSE 0
        END
    ) AS ActiveCustomers,

    SUM(
        CASE
            WHEN ChurnStatus = 1
            THEN 1
            ELSE 0
        END
    ) AS ChurnedCustomers

FROM Customers;


/* 5. CHURN RATE */

SELECT
    CAST(
        100.0 *
        SUM(CASE WHEN ChurnStatus = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(6,2)
    ) AS ChurnRatePct

FROM Customers;


/* 6. CONVERSION RATE */

SELECT
    COUNT(*) AS TotalLeads,

    SUM(
        CASE
            WHEN Converted = 1
            THEN 1
            ELSE 0
        END
    ) AS ConvertedLeads,

    CAST(
        100.0 *
        SUM(CASE WHEN Converted = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(6,2)
    ) AS ConversionRatePct

FROM Leads;


/* 7. SALES SUMMARY & AOV */

SELECT
    COUNT(DISTINCT OrderID) AS TotalOrders,

    COUNT(DISTINCT CustomerID) AS PurchasingCustomers,

    CAST(
        SUM(NetAmount)
        AS DECIMAL(18,2)
    ) AS NetRevenue,

    CAST(
        SUM(NetAmount)
        / NULLIF(COUNT(DISTINCT OrderID), 0)
        AS DECIMAL(12,2)
    ) AS AOV

FROM Sales;


/* 8. REPEAT PURCHASE RATE */

WITH CustomerOrders AS (
    SELECT
        CustomerID,
        COUNT(DISTINCT OrderID) AS OrderCount
    FROM Sales
    GROUP BY CustomerID
)

SELECT
    COUNT(*) AS PurchasingCustomers,

    SUM(
        CASE
            WHEN OrderCount > 1
            THEN 1
            ELSE 0
        END
    ) AS RepeatCustomers,

    CAST(
        100.0 *
        SUM(CASE WHEN OrderCount > 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(6,2)
    ) AS RepeatPurchaseRatePct

FROM CustomerOrders;


/* 9. PURCHASE FREQUENCY */

SELECT
    CAST(
        COUNT(DISTINCT OrderID) * 1.0
        / NULLIF(COUNT(DISTINCT CustomerID), 0)
        AS DECIMAL(12,2)
    ) AS PurchaseFrequency

FROM Sales;


/* 10. CUSTOMER LIFETIME VALUE */

SELECT
    CAST(
        SUM(NetAmount)
        / NULLIF(COUNT(DISTINCT CustomerID), 0)
        AS DECIMAL(18,2)
    ) AS HistoricalCLV

FROM Sales;


/* 11. EFFECTIVE DISCOUNT RATE */

SELECT
    CAST(
        100.0 * SUM(DiscountAmount)
        / NULLIF(SUM(TotalAmount), 0)
        AS DECIMAL(6,2)
    ) AS EffectiveDiscountRatePct

FROM Sales;


/* 12. INTERACTION SUMMARY */

SELECT
    COUNT(*) AS TotalInteractions,
    COUNT(DISTINCT CustomerID) AS CustomersReached,
    COUNT(DISTINCT Channel) AS ChannelCount

FROM Interactions;


/* 13. SUPPORT SUMMARY */

SELECT
    COUNT(*) AS TotalTickets,

    SUM(
        CASE
            WHEN TicketStatus = 'Closed'
            THEN 1
            ELSE 0
        END
    ) AS ClosedTickets,

    SUM(
        CASE
            WHEN TicketStatus <> 'Closed'
            THEN 1
            ELSE 0
        END
    ) AS OpenTickets,

    CAST(
        AVG(SatisfactionScore)
        AS DECIMAL(5,2)
    ) AS AvgSatisfactionScore

FROM SupportTickets;


/* 14. REVENUE BY PRODUCT CATEGORY */

SELECT
    ProductCategory,
    CAST(SUM(NetAmount) AS DECIMAL(18,2)) AS NetRevenue
FROM Sales
GROUP BY ProductCategory
ORDER BY NetRevenue DESC;


/* 15. REVENUE BY SALES CHANNEL */

SELECT
    SalesChannel,
    CAST(SUM(NetAmount) AS DECIMAL(18,2)) AS NetRevenue
FROM Sales
GROUP BY SalesChannel
ORDER BY NetRevenue DESC;


/* 16. MONTHLY NET REVENUE */

SELECT
    YEAR(SaleDate) AS SaleYear,
    MONTH(SaleDate) AS SaleMonth,
    CAST(SUM(NetAmount) AS DECIMAL(18,2)) AS NetRevenue

FROM Sales

GROUP BY
    YEAR(SaleDate),
    MONTH(SaleDate)

ORDER BY
    SaleYear,
    SaleMonth;


/* 17. CAMPAIGN ROAS */

SELECT
    c.CampaignName,
    c.Budget,

    CAST(
        SUM(cr.RevenueAttributed)
        AS DECIMAL(18,2)
    ) AS AttributedRevenue,

    CAST(
        SUM(cr.RevenueAttributed)
        / NULLIF(c.Budget, 0)
        AS DECIMAL(12,2)
    ) AS ROAS

FROM Campaigns c

LEFT JOIN CampaignResponses cr
    ON c.CampaignID = cr.CampaignID

GROUP BY
    c.CampaignID,
    c.CampaignName,
    c.Budget

ORDER BY
    ROAS DESC;
