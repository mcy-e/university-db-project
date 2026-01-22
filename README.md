# University Database Management System

A comprehensive desktop application for managing university operations including student records, course enrollment, instructor assignments, grading, and attendance tracking. Built with PyQt6 and powered by cloud-hosted PostgreSQL (Neon).

## Purpose

This system streamlines administrative and academic operations for educational institutions by providing:

- Centralized management of students, instructors, courses, departments, and facilities
- Automated enrollment and scheduling processes
- Performance tracking through marks and attendance management
- Academic results processing with automated grade calculations
- Comprehensive audit trails for data integrity
- Multi-language support (English, French, Arabic)

## Tech Stack

- **Frontend**: PyQt6 6.6.1 (Python Qt bindings for desktop GUI)
- **Backend**: Python 3.11
- **Database**: PostgreSQL (hosted on Neon cloud platform)
- **Database Adapter**: psycopg2-binary 2.9.9 with connection pooling
- **Configuration**: python-dotenv 1.0.0 for environment management

## Features

### Core Functionality

- **Complete CRUD Operations**: Manage all database entities through intuitive interfaces
  - Students, Instructors, Courses, Departments, Rooms
  - Enrollments, Marks, Exams, Activities, Attendance, Reservations
- **Instructor Assignment**: Assign teaching staff to courses with department validation
- **Reservation Management**: Schedule classrooms with automated conflict detection
- **Marks Entry**: Bulk entry and editing of student examination grades
- **Attendance Tracking**: Record student presence for lectures and activities
- **Results Processing**: Automatic calculation of passing criteria including:
  - Disqualifying marks (60% of course average)
  - Minimum semester average (10/20)
  - Maximum absences (5 per module)
- **SQL Query Interface**: Execute predefined queries for common reports:
  - Student lists by group/section
  - Instructor and student timetables
  - Average marks by course and group
  - Failed students and resit eligibility
  - Attendance statistics
- **Audit System**: Automated logging of all data modifications (INSERT, UPDATE, DELETE)

### User Interface Features

- **Multi-Language Support**: Full internationalization (i18n) with seamless language switching
  - English (default)
  - French (Français)
  - Arabic (العربية) with right-to-left (RTL) text support
  - All UI elements, menus, and labels dynamically translate
  - User language preference saved and restored on restart

- **Multiple Theme Options**: Professional QSS stylesheet system
  - Default Theme: Clean, modern interface
  - Dark Mode: Eye-friendly dark theme for extended use
  - Cyberpunk Neon: Vibrant, futuristic color scheme
  - Themes apply instantly without restart
  - Custom stylesheets for consistent visual design

- **Real-Time Search**: Instant filtering across all data tables as you type
- **Input Validation**: Pre-submission validation with helpful error messages
- **Responsive Design**: Adapts to different screen sizes and resolutions
- **Keyboard Navigation**: Full keyboard shortcuts for power users

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon account recommended)
- Git (for cloning the repository)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/university-db-project-new.git
   cd university-db-project-new
   ```

2. **Install Python dependencies**:
   ```bash
   cd Application
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   
   Create a `.env` file in the `Application` directory with your database connection string:
   
   ```env
   DATABASE_URL=postgresql://username:password@hostname:5432/database?sslmode=require
   ```
   
   See [Neon Database Configuration](#neon-database-configuration) below for details.

4. **Initialize the database schema**:

   Execute the SQL files in order using psql or your Neon SQL Editor:
   
   ```bash
   # Base schema (8 tables)
   psql -h your-neon-host.neon.tech -U username -d database < Database/Original_Schema/CREATE_TABLES.sql
   psql -h your-neon-host.neon.tech -U username -d database < Database/Original_Schema/INSERT_TABLES.sql
   
   # Extended schema (6 additional tables)
   psql -h your-neon-host.neon.tech -U username -d database < Database/Extende_Schema/new_tables.sql
   psql -h your-neon-host.neon.tech -U username -d database < Database/Extende_Schema/functions.sql
   psql -h your-neon-host.neon.tech -U username -d database < Database/Extende_Schema/audit_triggers.sql
   psql -h your-neon-host.neon.tech -U username -d database < Database/Extende_Schema/INSERT_NEW_DATA.sql
   ```

5. **Run the application**:
   ```bash
   python Application/main.py
   ```

## Neon Database Configuration

### Creating a Neon Project

1. Sign up for a free account at [neon.tech](https://neon.tech)
2. Create a new project
3. Note your connection string from the project dashboard

### Connection String Format

Neon provides a connection string in this format:

```
postgresql://username:password@ep-project-12345.us-east-2.aws.neon.tech:5432/neondb?sslmode=require
```

### Environment Configuration

Create an `.env` file in the `Application` directory:

```env
# Option 1: Use DATABASE_URL
DATABASE_URL=postgresql://username:password@ep-project-12345.us-east-2.aws.neon.tech:5432/neondb?sslmode=require

# Option 2: Use NEON_URI (alternative)
NEON_URI=postgresql://username:password@ep-project-12345.us-east-2.aws.neon.tech:5432/neondb?sslmode=require
```

The application automatically:
- Parses the connection string
- Extracts database, user, password, host, port, and SSL settings
- Initializes a connection pool with 1-10 connections
- Ensures secure SSL connections to Neon

### Connection Pool Benefits

The application uses client-side connection pooling via psycopg2:

- Reduced connection overhead
- Better performance through connection reuse
- Automatic connection health monitoring
- Controlled concurrent access limits

## Project Structure

```
university-db-project-new/
├── Application/              # Desktop application code
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   ├── GUI/                 # User interface modules
│   ├── UTILS/               # Utility functions
│   └── Translations/        # Language files
├── Database/                 # Database layer
│   ├── connection.py        # Connection pool manager
│   ├── database.py          # Data access functions (92+ functions)
│   ├── Original_Schema/     # Base SQL schema (8 tables)
│   └── Extende_Schema/      # Extended features (6 tables, 15+ functions)
├── Documentation/            # Project documentation
│   ├── Project_Documentation.md      # System architecture
│   ├── Technical_Documentation.md     # Implementation details
│   ├── Lab_Reports.md                # Technical lab work
│   └── *.png                         # ERD diagrams
└── README.md                # This file
```

## Screenshots

### Main Application

![Main Dashboard](Documentation/Images/main.png)
*Main application dashboard with navigation menu*

![About Section](Documentation/Images/main_about.png)
*Application about section showing project information*

### CRUD Operations

![Student CRUD](Documentation/Images/student_crud.png)
*Student management interface with search and edit capabilities*

### Academic Management

![Instructor Assignment](Documentation/Images/instructor_course_assingment.png)
*Assign instructors to courses with department validation*

![Reservation Management](Documentation/Images/reservation.png)
*Classroom reservation system with conflict detection*

### Performance Tracking

![Grade Entry](Documentation/Images/grade_entry.png)
*Bulk entry of student examination marks*

![Attendance Tracking](Documentation/Images/attendance.png)
*Student attendance recording for activities*

![Grade Processing](Documentation/Images/grade.png)
*Results processing and grade calculations*

### Advanced Features

![Query Execution](Documentation/Images/query_execution.png)
*SQL query interface with predefined and custom queries*

![Settings](Documentation/Images/settings.png)
*Application settings with theme and language options*

*The application features a modern, professional interface with support for multiple themes and languages.*

## Database Schema

The system implements a comprehensive relational schema:

### Original Schema (8 Tables)
- **Department**: Academic departments
- **Student**: Student personal information
- **Course**: Course catalog with department association
- **Instructor**: Teaching staff with rank
- **Room**: Classroom and facilities
- **Reservation**: Room bookings and schedules
- **Enrollment**: Student-course many-to-many relationship
- **Mark**: Student grades with constraints

### Extended Schema (6 Additional Tables)
- **Activity**: Lecture, tutorial, and practical sessions
- **Exam**: Examination definitions
- **Attendance_to_Activities**: Student attendance records
- **Student Attributes**: Group and Section assignments
- **Audit Logs**: Automatic tracking of data modifications

### SQL Functions (15+)
- Student filtering by group/section
- Timetable generation for instructors and students
- Grade calculations and averages
- Disqualifying mark computation
- Semester pass/fail determination
- Attendance statistics

### Database Triggers
- Audit logging for marks (INSERT, UPDATE, DELETE)
- Audit logging for attendance modifications
- Timestamp tracking for all operations

For detailed schema information, see [Technical Documentation](Documentation/Technical_Documentation.md).

## Documentation

Comprehensive documentation is available in the `Documentation/` folder:

- **[Project Documentation](Documentation/Project_Documentation.md)**: System architecture, Neon integration, application lifecycle
- **[Technical Documentation](Documentation/Technical_Documentation.md)**: File-level implementation details, data flow, assignment mapping
- **[Lab Reports](Documentation/Lab_Reports.md)**: Technical lab work and query examples

## Development

### Building Executable

To create a standalone executable using PyInstaller:

```bash
cd Application
pyinstaller UniversityManagement.spec
```

The executable will be created in the `Executable` directory.

### Logging

Application logs are stored in the `logs/` directory. Log files use rotating file handlers to prevent unbounded growth.

## Academic Context

This project was developed as part of the "Introduction to Databases" course (A.year 2025/2026). It fulfills the course term project requirements including:

- Complete ERD design and normalization
- PostgreSQL schema implementation
- Python application with graphical interface
- CRUD operations on all entities
- Academic management features
- Performance tracking and results processing
- SQL functions and triggers
- Comprehensive audit system

For assignment requirements mapping, see the [Technical Documentation](Documentation/Technical_Documentation.md#assignment-requirements-mapping).

## License

This project is created for academic purposes as part of a university course project.

## Contributing

This is an academic project. try to test the beta version found on Executable folder For questions or suggestions, please open an issue on GitHub.

---

**Author**: Reffas chouaib  
**Course**: Introduction to Databases (A.year 2025/2026)  
**Institution**: National Higher School of Cybersecurity
