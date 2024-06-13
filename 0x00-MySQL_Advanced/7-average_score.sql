-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id_parameter INT
)
BEGIN
    DECLARE user_avg DECIMAL(10, 2);

    -- Compute average score for the user
    SELECT AVG(score)
    INTO user_avg
    FROM corrections
    WHERE user_id = user_id_parameter;

    -- Update the average_score field in the users table
    UPDATE users
    SET average_score = user_avg
    WHERE id = user_id_parameter;

END //

DELIMITER ;

