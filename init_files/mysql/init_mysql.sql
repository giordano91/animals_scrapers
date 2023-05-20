USE charlie_feeder;

CREATE TABLE IF NOT EXISTS subito_it (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    place VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    post_id VARCHAR(50),
    link_post VARCHAR(200) NOT NULL,
    link_image VARCHAR(200)
);
