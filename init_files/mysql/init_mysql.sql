USE charlie_feeder;

-- breed table
CREATE TABLE IF NOT EXISTS breed (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

-- species table
CREATE TABLE IF NOT EXISTS species (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

-- ads table
CREATE TABLE IF NOT EXISTS ads (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    post_date DATETIME,
    birthdate DATETIME,
    place VARCHAR(100),
    description TEXT,
    price VARCHAR(50),
    post_id VARCHAR(50) NOT NULL UNIQUE,
    link_post VARCHAR(200),
    link_image JSON,
    source VARCHAR(50) NOT NULL,
    breed_id INT,
    species_id INT,
    CONSTRAINT fk_ads_breed FOREIGN KEY (breed_id) REFERENCES breed(id),
    CONSTRAINT fk_ads_species FOREIGN KEY (species_id) REFERENCES species(id)
);
