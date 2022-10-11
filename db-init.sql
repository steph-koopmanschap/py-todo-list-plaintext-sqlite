PRAGMA foreign_keys = ON;

CREATE TABLE lsts (
    id integer PRIMARY KEY,
    lst_name text NOT NULL UNIQUE
);

CREATE TABLE tasks (
    id integer PRIMARY KEY,
    task_name text NOT NULL,
    task_isDone text NOT NULL,
    lst_id integer,
    FOREIGN KEY (lst_id) REFERENCES lsts (id) 
);

CREATE TABLE subtasks (
    id integer PRIMARY KEY,
    subtask_name text NOT NULL,
    subtask_isDone text NOT NULL,
    task_id integer,
    FOREIGN KEY (task_id) REFERENCES tasks (id)
);

INSERT INTO lsts (id, lst_name)
VALUES(12345678, "TODOs");

INSERT INTO lsts (id, lst_name)
VALUES(12345679, "DAILIES");

INSERT INTO lsts (id, lst_name)
VALUES(12345670, "HABITS");

INSERT INTO tasks (id, task_name, task_isDone, lst_id)
VALUES(87654321, "My task", "NO", 12345678);

INSERT INTO subtasks (id, subtask_name, subtask_isDone, task_id)
VALUES(12365478, "A subtask", "NO", 87654321);

INSERT INTO tasks (id, task_name, task_isDone, lst_id)
VALUES(33333333, "A difficult task", "NO", 12345678);

INSERT INTO tasks (id, task_name, task_isDone, lst_id)
VALUES(11111111, "My Habit", "NO", 12345670);

INSERT INTO tasks (id, task_name, task_isDone, lst_id)
VALUES(22222222, "Another task", "NO", 12345679);

SELECT 
    name
FROM 
    sqlite_schema
WHERE 
    type ='table' AND 
    name NOT LIKE 'sqlite_%';

