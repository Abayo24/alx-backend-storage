-- creates a stored procedure
-- ComputeAverageWeightedScoreForUsers
-- that computes and store the average
-- weighted score for all students.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
DECLARE done INT DEFAULT 0;
DECLARE user_id INT;

DECLARE cur CURSOR FOR SELECT id FROM users;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

OPEN cur;

read_loop: LOOP
  FETCH cur INTO user_id;
  IF done
    THEN LEAVE read_loop;
  END IF;

SET @total_weighted_score := (SELECT SUM(score * weight) FROM scores WHERE user_id = user_id);
SET @total_weight := (SELECT SUM(weight) FROM scores WHERE user_id = user_id);

IF @total_weight > 0 
  THEN SET @average_weighted_score := @total_weighted_score / @total_weight;
  ELSE SET @average_weighted_score := 0;
END IF;

UPDATE users
SET average_weighted_score = @average_weighted_score
WHERE id = user_id;

END LOOP;

CLOSE cur;

END $$

DELIMITER ;
