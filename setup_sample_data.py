#!/usr/bin/env python3
"""
Sample Data Setup Script
This script will create sample users and data for the Group Study Finder application.
Run this after setting up the database schema.

Usage: python setup_sample_data.py
"""

import sys
import os
sys.path.append('backend')

from backend.app import create_app, db
from backend.app.models import User, Course, UserCourses, GroupStudy, GroupMembers, Notification
from datetime import datetime

def create_sample_data():
    app = create_app()

    with app.app_context():
        print("Setting up sample data...")

        # Clear existing data (optional - uncomment if needed)
        # db.drop_all()
        # db.create_all()

        # Create sample users
        users_data = [
            {'name': 'Dr. John Smith', 'email': 'john.smith@bracu.ac.bd', 'password': 'password123', 'role': 'teacher'},
            {'name': 'Alice Johnson', 'email': 'alice.j@g.bracu.ac.bd', 'password': 'password123', 'role': 'student'},
            {'name': 'Bob Wilson', 'email': 'bob.w@g.bracu.ac.bd', 'password': 'password123', 'role': 'student'},
            {'name': 'Carol Davis', 'email': 'carol.d@g.bracu.ac.bd', 'password': 'password123', 'role': 'student'},
            {'name': 'David Brown', 'email': 'david.b@g.bracu.ac.bd', 'password': 'password123', 'role': 'student'}
        ]

        created_users = []
        for user_data in users_data:
            # Check if user already exists
            if not User.query.filter_by(email=user_data['email']).first():
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    role=user_data['role']
                )
                user.set_password(user_data['password'])
                user.save()
                created_users.append(user)
                print(f"✅ Created user: {user.name} ({user.email})")

        # Create sample courses
        if not Course.query.first():
            teacher = User.query.filter_by(role='teacher').first()
            courses_data = [
                {'course_code': 'CSE470', 'course_name': 'Software Engineering', 'instructor_id': teacher.user_id},
                {'course_code': 'CSE370', 'course_name': 'Database Systems', 'instructor_id': teacher.user_id},
                {'course_code': 'CSE220', 'course_name': 'Data Structures', 'instructor_id': teacher.user_id},
                {'course_code': 'MAT120', 'course_name': 'Calculus I', 'instructor_id': teacher.user_id},
                {'course_code': 'PHY111', 'course_name': 'Physics I', 'instructor_id': teacher.user_id}
            ]

            for course_data in courses_data:
                course = Course(**course_data)
                course.save()
                print(f"✅ Created course: {course.course_code} - {course.course_name}")

        # Create user-course relationships
        students = User.query.filter_by(role='student').all()
        courses = Course.query.all()

        if students and courses:
            # Alice - doing CSE470, done CSE220
            alice = next((u for u in students if 'alice' in u.email.lower()), None)
            if alice:
                cse470 = next((c for c in courses if c.course_code == 'CSE470'), None)
                cse220 = next((c for c in courses if c.course_code == 'CSE220'), None)

                if cse470 and not UserCourses.query.filter_by(user_id=alice.user_id, course_id=cse470.course_id).first():
                    uc1 = UserCourses(user_id=alice.user_id, course_id=cse470.course_id, status='doing')
                    uc1.save()

                if cse220 and not UserCourses.query.filter_by(user_id=alice.user_id, course_id=cse220.course_id).first():
                    uc2 = UserCourses(user_id=alice.user_id, course_id=cse220.course_id, status='done')
                    uc2.save()

            print("✅ Created user-course relationships")

        # Create sample study group
        if not GroupStudy.query.first():
            alice = User.query.filter_by(email='alice.j@g.bracu.ac.bd').first()
            cse470 = Course.query.filter_by(course_code='CSE470').first()

            if alice and cse470:
                group = GroupStudy(
                    course_id=cse470.course_id,
                    group_name='CSE470 Final Prep',
                    description='Preparing for the final examination together',
                    created_by=alice.user_id,
                    session_start=datetime(2024, 12, 15, 14, 0),
                    session_end=datetime(2024, 12, 15, 16, 0)
                )
                group.save()

                # Add Alice as leader
                membership = GroupMembers(
                    group_id=group.group_id,
                    user_id=alice.user_id,
                    role='leader'
                )
                membership.save()

                print("✅ Created sample study group")

        # Create sample notifications
        if not Notification.query.first():
            alice = User.query.filter_by(email='alice.j@g.bracu.ac.bd').first()
            if alice:
                notification = Notification(
                    user_id=alice.user_id,
                    message='Welcome to Group Study Finder!'
                )
                notification.save()
                print("✅ Created sample notifications")

        print("\n🎉 Sample data setup completed!")
        print("\nTest Accounts:")
        print("Teacher: john.smith@bracu.ac.bd / password123")
        print("Student: alice.j@g.bracu.ac.bd / password123")
        print("Student: bob.w@g.bracu.ac.bd / password123")
        print("Student: carol.d@g.bracu.ac.bd / password123")
        print("Student: david.b@g.bracu.ac.bd / password123")

if __name__ == "__main__":
    create_sample_data()
