-- SQL queries for price history table
DROP TABLE IF EXISTS price_history;

CREATE TABLE price_history (
    ticker VARCHAR(10),
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    PRIMARY KEY (ticker, date)  -- Ensure ticker + date is unique
);
