insert into activity (activity_id, Activity_Type, reservation_id, course_id, department_id) values (1, 'lecture', 1, 1, 1);
insert into activity (activity_id, Activity_Type, reservation_id, course_id, department_id) values (4, 'practical', 4, 4, 4);
---------------------------------------------------------------------------------------------------------------------------------
insert into exam (exam_id, duration, exam_type, course_id, department_id) values (1, 39, 'midterm', 1, 1);
insert into exam (exam_id, duration, exam_type, course_id, department_id) values (4, 69, 'project', 4, 4);
----------------------------------------------------------------------------------------
INSERT INTO student_takes_an_exam (exam_id, student_id, statu) VALUES (1, 1, 'absent');
INSERT INTO student_takes_an_exam (exam_id, student_id, statu) VALUES (4, 4, 'present');
-----------------------------------------------------------------------------------------------------------

INSERT INTO attendance_to_activities (student_id, activity_id, attendance_date, statu) VALUES (1, 1, '12/20/2025', 'absent');
INSERT INTO attendance_to_activities (student_id, activity_id, attendance_date, statu) VALUES (4, 4, '5/15/2025', 'absent');

---------------------------------------------------------------------------------------------------------------------------------

INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (1, 1, 1, '2025-01-10');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (1, 2, 1, '2025-01-12');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (1, 3, 1, '2025-01-15');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (2, 1, 1, '2025-01-10');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (2, 4, 4, '2025-02-01');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (3, 2, 1, '2025-01-20');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (3, 3, 1, '2025-01-22');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (4, 1, 1, '2025-01-11');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (4, 4, 4, '2025-02-05');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (5, 2, 1, '2025-01-18');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (5, 3, 1, '2025-01-25');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (2, 2, 1, '2025-01-14');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (3, 1, 1, '2025-01-11');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (4, 2, 1, '2025-01-19');
INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (5, 1, 1, '2025-01-13');

-----------------------------------------------------------------------------------------

-- Marks for Student 1 (Ali)
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (1, 1, 1, 1, 14.5, '2025-04-10');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (2, 1, 2, 1, 12.0, '2025-04-15');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (3, 1, 3, 1, 10.0, '2025-05-20');

-- Marks for Student 2 (Amar)
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (4, 2, 1, 1, 11.0, '2025-04-10');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (5, 2, 2, 1, 13.5, '2025-04-15');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (6, 2, 4, 4, 16.0, '2025-06-01');

-- Marks for Student 3 (Ameur)
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (7, 3, 1, 1, 09.5, '2025-04-10');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (8, 3, 4, 4, 12.0, '2025-06-01');

-- Marks for Student 4 (Aissa)
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (9, 4, 1, 1, 15.0, '2025-04-10');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (10, 4, 2, 1, 08.0, '2025-04-15');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (11, 4, 4, 4, 14.5, '2025-06-01');

-- Marks for Student 5 (Fatima)
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (12, 5, 2, 1, 18.0, '2025-04-15');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (13, 5, 3, 1, 17.5, '2025-05-20');
INSERT INTO mark (mark_id, student_id, course_id, department_id, mark_value, mark_date) VALUES (14, 5, 4, 4, 19.0, '2025-06-01');