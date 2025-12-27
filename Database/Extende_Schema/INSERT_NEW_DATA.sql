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