--* 1. Write, and show a use case within an SQL querry, an SQL function that returns all rooms with a capacity greater than a given value.

CREATE FUNCTION BigCapacityRooms (capa INTEGER ) returns  

    TABLE ( roomno VARCHAR,capacity INT) AS $$

    SELECT roomno , capacity FROM room WHERE capacity > $1

$$ LANGUAGE SQL;

SELECT * FROM BigCapacityRooms(15);

--* 2. Write, and show a use case within an SQL querry, an SQL function that returns the ID of a department given its name.

CREATE FUNCTION Find_ID(Name VARCHAR) RETURNS 

    INT AS $$ 

    SELECT department_id FROM department WHERE name ILIKE $1;

$$ LANGUAGE SQL;

SELECT Find_ID('CCS');


--* 3. Write, and show a use case within an SQL querry, an SQL function that checks if a room reservation is possible while providing the list of existing reservations (IDs) in conflict with the given reservation’s input parameters

DROP FUNCTION CheckReservation

CREATE FUNCTION CheckReservation(Building VARCHAR, RoomNo VARCHAR, reservation_date DATE, start_t TIME, end_t TIME ) 
    RETURNS BOOLEAN AS $$
    SELECT NOT EXISTS 
    (SELECT 1 FROM
        (SELECT reservation_id
        FROM reservation
        WHERE building = $1
        AND roomno   = $2
        AND reserv_date = $3
        AND NOT (
                end_time   <= $4
            OR start_time >= $5
        )) AS reservation_table
    
     );

$$ LANGUAGE SQL;

--* Other query that returns the table instead of just checking

CREATE FUNCTION ReservationConflicts(Building VARCHAR,RoomNo VARCHAR,reservation_date DATE,start_t TIME,end_t TIME)
    RETURNS TABLE (reservation_id INTEGER)
    AS $$
        SELECT reservation_id
        FROM reservation
        WHERE building = $1
        AND roomno = $2
        AND reserv_date = $3
        AND NOT (
                end_time   <= $4
            OR start_time >= $5
        );
    $$ LANGUAGE SQL;



SELECT * FROM reservation

SELECT ReservationConflicts('A','301','2006-09-24','13:45:00','17:00:00')