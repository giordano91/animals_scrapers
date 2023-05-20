USE charlie_feeder;

-- subito.it table
CREATE TABLE IF NOT EXISTS subito_it (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    place VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    post_id VARCHAR(50),
    link_post VARCHAR(200) NOT NULL,
    link_image VARCHAR(200)
);

-- materialized view (the one read from Charlie web app)
CREATE TABLE IF NOT EXISTS mv_external_ads(
    title VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    place VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    link_post VARCHAR(200) NOT NULL,
    link_image VARCHAR(200)
);

-- store procedure to get data from service tables and populate materialized view
DELIMITER //
CREATE PROCEDURE feed_mv_external_ads ()
BEGIN
    TRUNCATE TABLE mv_external_ads;
    INSERT INTO mv_external_ads
    SELECT s.title,
           s.date,
           s.place,
           s.category,
           s.description,
           s.link_post,
           s.link_image
    FROM subito_it s;
END //
DELIMITER ;
