-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers() BEGIN DECLARE done INT DEFAULT FALSE; DECLARE user_id INT; DECLARE total_score FLOAT; DECLARE total_weight FLOAT; DECLARE weighted_avg FLOAT; -- Cursor to iterate through each user
 DECLARE cur_users
CURSOR
FOR
SELECT id
FROM users; DECLARE CONTINUE
HANDLER FOR NOT FOUND
SET done = TRUE; -- Open cursor
 OPEN cur_users; -- Loop through each user
 users_loop: LOOP FETCH cur_users INTO user_id; IF done THEN LEAVE users_loop; END IF; -- Initialize variables

SET total_score = 0;
SET total_weight = 0;
SET weighted_avg = 0; -- Calculate total_score and total_weight for the user

SELECT SUM(c.score * p.weight),
       SUM(p.weight) INTO total_score,
                          total_weight
FROM corrections c
JOIN projects p ON c.project_id = p.id
WHERE c.user_id = user_id; -- Calculate weighted average
 IF total_weight > 0 THEN
  SET weighted_avg = total_score / total_weight; ELSE
  SET weighted_avg = 0; END IF; -- Update average_score in users table

  UPDATE users
  SET average_score = weighted_avg WHERE id = user_id; END LOOP; -- Close cursor
 CLOSE cur_users; END //
DELIMITER ;
