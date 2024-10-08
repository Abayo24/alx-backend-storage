-- swl script that creates a table users with attributes id, email
-- name country - enumeration

CREATE TABLE IF NOT EXISTS users(
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  country ENUM('US', 'CO', 'TN')DEFAULT 'US' NOT NULL
)
