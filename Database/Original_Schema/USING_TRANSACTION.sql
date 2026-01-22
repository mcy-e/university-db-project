--* 1. Propose and write two simple transactions without save points.

BEGIN;

INSERT INTO Instructor VALUES
(7, 3, 'Chouaib', 'Reffas', 'MCA', NULL, NULL, 'CR@yahoo.en');

INSERT INTO Instructor VALUES
(8, 3, 'Sadek', 'Fehis', 'MCA', '4185', '4091', 'FE@yahoo.en');

COMMIT;



--* 2. Propose and write two transactions with save points.

SELECT * FROM instructor;

BEGIN;

UPDATE instructor SET department_id=2 WHERE instructor_id=7;

SAVEPOINT step1;

UPDATE instructor SET department_id=2 WHERE instructor_id=8;

ROLLBACK TO step1;

COMMIT;
