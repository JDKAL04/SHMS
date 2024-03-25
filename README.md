# Hostel Management System (HMS) Web Application

The Hostel Management System (HMS) is a Django-based web application designed to manage hostel operations efficiently. This application provides features for managing hostels, floors, rooms, beds, user registrations, and occupancy analytics.

## Features

- **Dashboard**: Provides an overview of hostel statistics including total floors, rooms, beds, and active hostels.
- **Hostel Management**: Allows adding, editing, and managing hostels with details such as name, address, organization, and branch.
- **Floor and Room Management**: Admins can add floors and rooms to hostels, indicating the number of rooms per floor.
- **Bed Allocation**: Users can allocate beds to students, ensuring efficient occupancy management.
- **User Registration**: Allows registration of users/students into the hostel with details like hostel, floor, room, and bed.
- **Analytics**: Provides analytics on hostel occupancy, bed utilization, and user distribution by organization and branch.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/hostel-project.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

4. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the application at `http://localhost:8000/`.**

## Usage

- Register as a superuser or login if already registered.
- Use the dashboard to monitor hostel statistics and occupancy analytics.
- Manage hostels, floors, rooms, and beds through the admin interface.
- Allocate beds to students through user registration functionality.
- Access hostel analytics for insights into bed utilization and user distribution.

## Contributing

Contributions are welcome! Please follow the [Contribution Guidelines](CONTRIBUTING.md) before making any contributions.

## License

This project is licensed under the [MIT License](LICENSE).
