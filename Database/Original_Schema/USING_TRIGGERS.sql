
--? Create  Student_Audit_Log table

CREATE TABLE Student_Audit_Log (
LogID SERIAL PRIMARY KEY,
OperationType VARCHAR(50) NOT NULL,
OperationTime TIMESTAMP NOT NULL,
Description TEXT
);

--? Create the function that insert the log to the created table on a trigger

CREATE OR REPLACE FUNCTION audit_student_changes_statement() RETURNS TRIGGER AS $$

    DECLARE msg_description TEXT;
    DECLARE time TIMESTAMP;
    BEGIN 

        msg_description := 'A statement-level DML operation ' || TG_OP || 'occurred on Students table.';
        time :=CURRENT_TIMESTAMP;
        INSERT INTO  student_audit_log (operationtype,operationtime,description) VALUES (TG_OP::VARCHAR,time::TIMESTAMP(0),msg_description);


        RETURN NULL;

    END;
$$ LANGUAGE plpgsql;

--? Create the trigger as requested

CREATE TRIGGER  trg_audit_students_statement

    AFTER INSERT OR UPDATE OR DELETE ON Student

    FOR EACH STATEMENT

    EXECUTE FUNCTION audit_student_changes_statement();




--? Test the trigger

UPDATE student SET city = 'Annaba' WHERE student_id=1;
INSERT INTO student VALUES (6,'Chouaib','Reffas','2007-02-23','14, did','Annaba','23000','0657633996',NULL,'ref@gmail.com');
DELETE FROM student WHERE student_id=2;

--* Select all rows from 'student_audit_log' for reviewing the result

SELECT * FROM student_audit_log;