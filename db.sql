-- DROP DATABASE task_scheduler;
CREATE DATABASE task_scheduler charset=utf8;
USE task_scheduler;

CREATE TABLE date_task (
TASK_DATE char(10) not null,
TASK char(100) not null,
TRACKED_TIME char(11) not null,
FINISHED BOOL not null);