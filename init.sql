CREATE TABLE IF NOT EXISTS People
(
    Gender         VARCHAR check ( Gender in ('male', 'female')),
    Name           VARCHAR     NOT NULL,
    "First name"   VARCHAR     NOT NULL,
    "Last name"    VARCHAR     NOT NULL,
    City           VARCHAR     NOT NULL,
    Email          VARCHAR     NOT NULL,
    "Md5 login"    VARCHAR(32) NOT NULL,
    "Phone number" VARCHAR     NOT NULL,
    "Date loaded"  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);