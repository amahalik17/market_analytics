-- SQL queries for table creation

CREATE TABLE fav_etfs (
    ticker VARCHAR(10),
    date DATE,
    open DECIMAL,
    high DECIMAL,
    low DECIMAL,
    close DECIMAL,
    volume BIGINT,
    PRIMARY KEY (ticker, date)  -- Ensure ticker + date is unique
);

CREATE TABLE fav_stocks (
    ticker VARCHAR(10),
    date DATE,
    open DECIMAL,
    high DECIMAL,
    low DECIMAL,
    close DECIMAL,
    volume BIGINT,
    PRIMARY KEY (ticker, date)  -- Ensure ticker + date is unique
);

CREATE TABLE snp500 (
    ticker VARCHAR(10),
    date DATE,
    open DECIMAL,
    high DECIMAL,
    low DECIMAL,
    close DECIMAL,
    volume BIGINT,
    PRIMARY KEY (ticker, date)  -- Ensure ticker + date is unique
);

