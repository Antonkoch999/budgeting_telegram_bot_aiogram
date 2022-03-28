create table user(
    telegram_id INTEGER primary key,
    name VARCHAR(255)
);

create table category(
    id integer primary key,
    name varchar(255),
    is_expense boolean
);

create table budgeting(
    id integer primary key,
    amount real,
    create_at datetime default CURRENT_TIMESTAMP,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(telegram_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE
);
