-- script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
	    IN p_user_id INT
)
BEGIN
	    DECLARE total_score FLOAT DEFAULT 0;
	    DECLARE total_weight FLOAT DEFAULT 0;
	    DECLARE weighted_avg FLOAT DEFAULT 0;

	    -- Calculate total_score and total_weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = p_user_id;

    -- Calculate weighted average
    IF total_weight > 0 THEN
	        SET weighted_avg = total_score / total_weight;
		    ELSE
			        SET weighted_avg = 0;
				    END IF;

				    -- Update average_score in users table
    UPDATE users
    SET average_score = weighted_avg
    WHERE id = p_user_id;

END //

DELIMITER ;

