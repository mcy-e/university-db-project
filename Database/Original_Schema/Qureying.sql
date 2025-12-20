

SELECT * FROM Student;

--* 1. List of the last names and first names of the students stored in the database.

SELECT last_name ,first_name FROM Student;

--* 2. List of the last names and first names of the students who live in a chosen city (by you) from the list of cities in the database.

SELECT last_name,first_name FROM Student  WHERE  city LIKE 'Annaba';

--* 3. List of the last names and first names of the students whose last name starts with ’A’.

SELECT last_name,first_name FROM Student  WHERE last_name LIKE 'A%';

--* 4. List of the last names and first names of the teachers whose second-to-last letter of the last name is ’E’.

SELECT last_name,first_name FROM Instructor WHERE last_name LIKE '%e_';

--* 5. List of the last names and first names of the teachers sorted by department name, then by last name and then by first name.

SELECT i.last_name, i.first_name FROM Instructor i JOIN Department d
ON i.Department_ID = d.Department_ID
ORDER BY
    d.name,
    i.last_name,
    i.first_name;

--* 6. How many teachers have the grade ’Supleant’?

SELECT COUNT(rank) AS num_teachers_with_grade_Supleant FROM Instructor WHERE rank LIKE 'Substitute';


--* 7. What are the last names and first names of the students who do not have a Fax number (NULL value)?

SELECT last_name,first_name FROM Student WHERE phone IS NULL;

--* 8. What are the titles of the courses whose description

SELECT * FROM Course WHERE description ILIKE '%Licence%';

--* 9. If we assume that one teaching hour costs 3000 DA, what is the cost in DA of each course (course hours) concern reserved hours– see the Reservation relationship)?

SELECT * From Reservation;

SELECT  c.Course_ID, SUM(hours_number)*3000 AS course_total_cost FROM Reservation r JOIN Course c ON c.Course_ID = r.Course_ID
GROUP BY c.Course_ID
ORDER BY course_total_cost ASC
;


--* 10. From the previous query, indicate the titles of the courses whose cost is between 3000 and 5000 DA.

SELECT 
    c.name,
    SUM(r.hours_number) * 3000 AS course_total_cost
FROM Course c
JOIN Reservation r ON r.Course_ID = c.Course_ID
GROUP BY c.Course_ID, c.name
HAVING SUM(r.hours_number) * 3000 BETWEEN 30000 AND 50000
ORDER BY course_total_cost ASC;

--* 11. What are the average capacity and the maximum capacity of the rooms?

SELECT AVG(capacity),MAX(capacity) FROM Room;

--* 12. What are the rooms whose capacity is less than the average capacity?

SELECT * FROM Room;

SELECT roomno, capacity
FROM Room
WHERE capacity < (
    SELECT AVG(capacity)
    FROM Room
);

--* 13. What are the last names and first names of the teachers belonging to the departments named ’SADS’ or ’CCS’? (Use IN then another solution)


SELECT first_name,last_name,d.name FROM Instructor i JOIN department d ON d.department_id = i.department_id WHERE d.name IN ('SADS','CSS');


SELECT first_name,last_name,d.name FROM Instructor i JOIN department d ON d.department_id = i.department_id WHERE d.name = 'SADS' OR d.name = 'CSS';

--* 14. What are the last names and first names of the teachers belonging neither to the ’SADS’ department nor to the ’CCS’ department?


SELECT first_name,last_name,d.name FROM Instructor i JOIN department d ON d.department_id = i.department_id WHERE d.name NOT IN ('SADS','CSS');


--* 15. Sort the students by city.

SELECT * FROM student 
ORDER BY city ASC;

--* 16. How many courses are associated with each department?

SELECT d.name,COUNT(c.department_id) FROM department d  LEFT JOIN course c ON  d.department_id = c.department_id
GROUP BY d.name;

--* 17. What are the names of the departments where the number of associated courses is greater than or equal to 3?

SELECT * FROM 
    (SELECT d.name,COUNT(c.department_id) AS course_number 
    FROM department d  LEFT JOIN course c ON  d.department_id = c.department_id
    GROUP BY d.name)
WHERE course_number >=3;

--* 18. What are the last names and first names of the teachers for whom there is at least two reservations? (Use EXISTS then another solution using the view created previously).


CREATE VIEW instructor_reservation AS 
    SELECT i.first_name, i.last_name, COUNT(r.instructor_id) AS reservations
    FROM instructor i
    JOIN reservation r ON r.instructor_id = i.instructor_id
    GROUP BY i.first_name, i.last_name
;


SELECT * FROM instructor_reservation WHERE reservations >= 2;

SELECT i.first_name, i.last_name
FROM instructor i
WHERE EXISTS (

    SELECT 1 FROM reservation r WHERE r.instructor_id=i.instructor_id
    OFFSET 1
)
;


--* 19. Which teachers have the most reservations (Use the View defined in question 18 and the keyword ALL)?

SELECT * FROM instructor_reservation WHERE reservations >= ALL (
    SELECT reservations FROM instructor_reservation
);

--* 20. What are the last names and first names of the teachers who do not have any reservations?

SELECT first_name,last_name FROM instructor 

WHERE (first_name,last_name) NOT IN (
    SELECT first_name,last_name FROM instructor_reservation
);

--* 21. Which rooms were reserved on all dates (stored in the database)?

SELECT r.roomno,COUNT(re.reserv_date) AS dates_num
 FROM room r  LEFT JOIN reservation re ON r.roomno=re.roomno
 GROUP BY r.roomno
 HAVING COUNT(re.reserv_date) > 0
 ;

SELECT * FROM reservation
ORDER BY reserv_date ASC;

--* 22. On which dates are all rooms reserved?

SELECT reserv_date FROM reservation WHERE reserv_date IN 
(SELECT reserv_date FROM reservation WHERE roomno ='022'AND roomno ='020' AND roomno ='301');


--* 23. Provide 5 examples including update clause.

UPDATE Student SET fax = '0145678970' WHERE student_id = 5;

UPDATE Room SET capacity = capacity + 5 WHERE roomno = '301';

UPDATE Instructor SET department_id = 3 WHERE instructor_id = 5;

UPDATE Reservation SET end_time = '17:30:00' WHERE end_time >= '17:00:00';

UPDATE course SET department_id = 3 WHERE course_id = 3;


--* 24. Provide 5 distinct examples of aggregation including aggregation with grouping.

SELECT COUNT(*) AS total_reservations FROM Reservation;

SELECT MAX(Capacity) AS max_capacity FROM Room;

SELECT Department_ID, COUNT(Instructor_ID) AS num_instructors FROM Instructor GROUP BY Department_ID;

SELECT Course_ID, COUNT(Reservation_ID) AS total_reservations_per_course FROM Reservation GROUP BY Course_ID;

SELECT Department_ID, COUNT(Course_ID) AS total_courses_per_department FROM Course GROUP BY Department_ID;

--* 25. Provide 5 distinct examples of set operations.

SELECT RoomNo FROM Room WHERE Building = 'A'
UNION
SELECT RoomNo FROM Room WHERE Building = 'B';

SELECT RoomNo FROM Room WHERE Building = 'A'
UNION ALL
SELECT RoomNo FROM Room WHERE Building = 'B';

SELECT RoomNo FROM Room WHERE Building = 'A'
INTERSECT
SELECT RoomNo FROM Room WHERE Capacity > 30;

SELECT RoomNo FROM Room WHERE Building = 'A'
EXCEPT
SELECT RoomNo FROM Room WHERE Capacity < 20;

SELECT Course_ID FROM Course WHERE Department_ID = 1
EXCEPT
SELECT Course_ID FROM Course WHERE Department_ID = 2

--* 26. Provide 5 examples of querying inside from clause.

SELECT RoomNo, num_reservations
FROM 
(SELECT RoomNo, COUNT(*) AS 
num_reservations FROM Reservation GROUP BY RoomNo) AS room_counts;

SELECT Instructor_ID, total_reservations
FROM (SELECT Instructor_ID, COUNT(*) AS total_reservations FROM Reservation GROUP BY Instructor_ID) AS inst_res;

SELECT Building, total_reservations
FROM (SELECT Building, COUNT(*) AS total_reservations FROM Reservation GROUP BY Building) AS building_res;

SELECT Department_ID, total_courses
FROM (SELECT Department_ID, COUNT(Course_ID) AS total_courses FROM Course GROUP BY Department_ID) AS dept_courses;

SELECT Department_ID, total_instructors
FROM (SELECT Department_ID, COUNT(Instructor_ID) AS total_instructors FROM Instructor GROUP BY Department_ID) AS dept_instructors;



