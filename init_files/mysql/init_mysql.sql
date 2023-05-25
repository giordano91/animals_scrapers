USE charlie_feeder;

-- ads table
CREATE TABLE IF NOT EXISTS ads (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    date DATETIME,
    place VARCHAR(100),
    category VARCHAR(50),
    description TEXT,
    price VARCHAR(50),
    post_id VARCHAR(50) NOT NULL UNIQUE,
    link_post VARCHAR(200),
    link_image TEXT,
    source VARCHAR(50) NOT NULL
);
