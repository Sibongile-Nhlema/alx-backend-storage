-- script that creates a function SafeDiv that divides (and returns)
-- the first by the second number or returns 0
-- if the second number is equal to 0.

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 4)
BEGIN
    DECLARE result DECIMAL(10, 4);

    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = CAST(a AS FLOAT) / CAST(b AS FLOAT);
    END IF;

    RETURN result;
END //

DELIMITER ;