CREATE TABLE `Flight`(
    `flight_num` VARCHAR(20) PRIMARY KEY,
    `price` INT,
    `seat_num` INT,
    `avail_num` INt,
    `from_city` VARCHAR(20),
    `arrive_city` VARCHAR(20)
);

CREATE TABLE `hotel`(
    `location` VARCHAR(20) PRIMARY KEY,
    `price` INT,
    `rooms_num` INT,
    `avail_num` INt
);

CREATE TABLE `bus`(
    `location` VARCHAR(20) PRIMARY KEY,
    `price` INT,
    `bus_num` INT,
    `avail_num` INt
);

CREATE TABLE `customers`(
    `name` VARCHAR(20) PRIMARY KEY,
    `id` INT
);

CREATE TABLE `reservation`(
    `resvkey` VARCHAR(20) PRIMARY KEY,
    `cust_name` VARCHAR(20),
    `resv_type` TINYINT,
    FOREIGN KEY(cust_name)
        REFERENCES customers(`name`) ON DELETE CASCADE,
    CONSTRAINT resv_type_check check(resv_type IN (1,2,3))
);