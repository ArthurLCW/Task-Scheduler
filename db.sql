DROP DATABASE IF EXISTS task_scheduler;
CREATE DATABASE task_scheduler charset=utf8;
USE task_scheduler;

CREATE TABLE date_task (
TASK_DATE char(10) not null,
TASK char(100) not null,
TRACKED_TIME char(11) not null,
FINISHED BOOL not null);


-- SELECT * FROM date_task;
-- INSERT INTO date_task (TASK_DATE, TASK, TRACKED_TIME, FINISHED) VALUES ('2021-01-04', 'TEST0', 'NA', false);
-- INSERT INTO date_task (TASK_DATE, TASK, TRACKED_TIME, FINISHED) VALUES ('2021-01-07', 'TEST1', 'NA', false);
-- INSERT INTO date_task (TASK_DATE, TASK, TRACKED_TIME, FINISHED) VALUES ('2021-01-08', 'TEST2', 'NA', false);
-- SELECT * FROM date_task;

-- select FINISHED from date_task where TASK_DATE='2022-02-02' AND TASK='666'