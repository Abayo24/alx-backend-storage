-- creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
DECLARE total_weighted_score DECIMAL(10,2) DEFAULT 0;
DECLARE total_weight DECIMAL(10,2) DEFAULT 0;
DECLARE average_weighted_score DECIMAL(10,2) DEFAULT 0;

SELECT SUM(score * weight), SUM(weight)
INTO total_weighted_score, total_weight
FROM scores
WHERE user_id = user_id;

IF total_weight > 0
  THEN SET average_weighted_score = total_weighted_score / total_weight;
  ELSE SET average_weighted_score = 0;
END IF;

UPDATE users
SET average_weighted_score = average_weighted_score
WHERE id = user_id;

END $$

DELIMITER ;
