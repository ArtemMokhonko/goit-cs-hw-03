SELECT * FROM tasks WHERE user_id = 3;
SELECT * FROM tasks WHERE status_id = 1;
UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 5;
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);
INSERT INTO tasks (title, description, status_id, user_id) VALUES ('Kill Bill', 'Use sword to kill Bill', 2, 2);
SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
DELETE FROM tasks WHERE id=6;
SELECT * from users WHERE email LIKE '%@%.net';
UPDATE users SET fullname = 'Uma Thurman' WHERE id = 1;
SELECT status.name, COUNT(tasks.id) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name;
SELECT tasks.*, fullname Name, email FROM tasks JOIN users on tasks.user_id = users.id WHERE users.email LIKE '%@%.net';
SELECT * FROM tasks WHERE description IS NULL  
SELECT users.fullname, tasks.title FROM tasks INNER JOIN users ON tasks.user_id = users.id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress';
SELECT u.fullname, COUNT(t.id) total_tasks FROM tasks t LEFT JOIN users as u ON t.user_id = u.id GROUP BY u.fullname; 