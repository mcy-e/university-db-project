--Create triggers for:
--● Mark table (INSERT, UPDATE, DELETE)
--● Attendance table (INSERT, UPDATE, DELETE)

-- Created  the mark_Audit_Log table in new tables.sql


---function to insert into the log when the mark get modificated

create or replace function audit_mark_changes_statement()
returns trigger
as $$
    DECLARE time TIMESTAMP;
    DECLARE msg_description TEXT;
    BEGIN
        time:=CURRENT_TIMESTAMP;
        msg_description:='A statement-level DML operation '||TG_OP||' occurred on marks table.';
        insert into mark_Audit_Log(OperationType,OperationTime,Description)
        values(TG_OP::varchar,time::TIMESTAMP(0),msg_description);
        return null;
    END
$$
LANGUAGE plpgsql;

--the trigger for mark table

create trigger trg_audit_mark_statement
      after insert or update or DELETE on mark
      FOR each statement
      EXECUTE function audit_mark_changes_statement() ;

--for the attandence table

create or replace function audit_attandence_changes_statement()
returns trigger 
as $$
    DECLARE msg_description text;
    DECLARE time TIMESTAMP ;
BEGIN
    msg_description:='A statement-level DML operation '||TG_OP||' occurred on '||TG_TABLE_NAME||' table. ';
    time:=CURRENT_TIMESTAMP;
    insert into attendance_Audit_Log(OperationType,OperationTime,Description)
    values(TG_OP::varchar,time::TIMESTAMP(0),msg_description);
    return null;
end
$$
LANGUAGE plpgsql;

create trigger trg_audit_attendance_to_activities_statement
after insert or update or DELETE on attendance_to_activities
for each statement
EXECUTE function audit_attandence_changes_statement();
 