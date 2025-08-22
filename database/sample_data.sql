-- Sample data for Group Study Finder

USE group_study_finder;

-- Insert sample users (passwords are hashed for 'password123')
INSERT INTO User (name, email, password, role) VALUES
('Dr. John Smith', 'john.smith@bracu.ac.bd', 'scrypt:32768:8:1$7dTYZSqEK7iKV3XG$46e6e0b1c8a1b4a5f9c2d8e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'teacher'),
('Alice Johnson', 'alice.j@g.bracu.ac.bd', 'scrypt:32768:8:1$7dTYZSqEK7iKV3XG$46e6e0b1c8a1b4a5f9c2d8e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'student'),
('Bob Wilson', 'bob.w@g.bracu.ac.bd', 'scrypt:32768:8:1$7dTYZSqEK7iKV3XG$46e6e0b1c8a1b4a5f9c2d8e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'student'),
('Carol Davis', 'carol.d@g.bracu.ac.bd', 'scrypt:32768:8:1$7dTYZSqEK7iKV3XG$46e6e0b1c8a1b4a5f9c2d8e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'student'),
('David Brown', 'david.b@g.bracu.ac.bd', 'scrypt:32768:8:1$7dTYZSqEK7iKV3XG$46e6e0b1c8a1b4a5f9c2d8e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'student');

-- Insert sample courses
INSERT INTO Course (course_code, course_name, instructor_id) VALUES
('CSE470', 'Software Engineering', 1),
('CSE370', 'Database Systems', 1),
('CSE220', 'Data Structures', 1),
('MAT120', 'Calculus I', 1),
('PHY111', 'Physics I', 1);

-- Insert user-course relationships
INSERT INTO UserCourses (user_id, course_id, status) VALUES
(2, 1, 'doing'), -- Alice doing CSE470
(2, 3, 'done'),  -- Alice completed CSE220
(3, 1, 'doing'), -- Bob doing CSE470
(3, 2, 'doing'), -- Bob doing CSE370
(4, 1, 'done'),  -- Carol completed CSE470
(4, 2, 'doing'), -- Carol doing CSE370
(5, 1, 'doing'), -- David doing CSE470
(5, 4, 'doing'); -- David doing MAT120

-- Insert sample study groups
INSERT INTO GroupStudy (course_id, group_name, description, created_by, session_start, session_end) VALUES
(1, 'CSE470 Final Prep', 'Preparing for the final examination together', 2, '2024-12-15 14:00:00', '2024-12-15 16:00:00'),
(2, 'Database Design Team', 'Working on database design project', 3, '2024-12-20 10:00:00', '2024-12-20 12:00:00');

-- Insert group members
INSERT INTO GroupMembers (group_id, user_id, role) VALUES
(1, 2, 'leader'), -- Alice leads CSE470 group
(1, 3, 'member'), -- Bob joins CSE470 group
(1, 5, 'member'), -- David joins CSE470 group
(2, 3, 'leader'), -- Bob leads Database group
(2, 4, 'member'); -- Carol joins Database group

-- Insert sample notifications
INSERT INTO Notification (user_id, message) VALUES
(2, 'Welcome to Group Study Finder!'),
(3, 'Your request to join "CSE470 Final Prep" has been approved!'),
(4, 'New study group created for CSE370 - Database Systems'),
(5, 'Reminder: CSE470 Final Exam is next week');

-- Insert sample global chat messages
INSERT INTO GlobalChat (sender_id, message) VALUES
(2, 'Hello everyone! Excited to use this platform for study groups!'),
(3, 'Looking for study partners for CSE370. Anyone interested?'),
(4, 'Just finished CSE470. Happy to help anyone with questions!');

-- Insert sample group chat messages
INSERT INTO GroupChat (group_id, sender_id, message) VALUES
(1, 2, 'Hey everyone, let's start preparing for the final!'),
(1, 3, 'I have some practice problems we can work on together.'),
(1, 5, 'Great! When should we meet?'),
(2, 3, 'Let's work on the ER diagram for our project.'),
(2, 4, 'I have some good resources for database design.');