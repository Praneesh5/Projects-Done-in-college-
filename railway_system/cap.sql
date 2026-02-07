CREATE DATABASE ticket_system;
USE ticket_system;
CREATE TABLE credentials(
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  password_hash VARCHAR(255),
  is_admin BOOLEAN
);
CREATE TABLE trains(
  train_no INT PRIMARY KEY,
  train_name VARCHAR(100),
  from_loc VARCHAR(50),
  to_loc VARCHAR(50),
  seats INT,
  cost INT,
  start_time TIME,
  end_time TIME
);
CREATE TABLE tickets(
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  train INT,
  passenger_name VARCHAR(100),
  age INT,
  berth_pref VARCHAR(20),
  date DATE,
  booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE payments(
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  amount INT,
  method VARCHAR(50),
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO credentials(username,password_hash,is_admin)
VALUES
('admin', SHA2('admin123',256),1),
('user', SHA2('user123',256),0);
