Recipe Management Application - README

Overview

This Recipe Management Application is a web-based system that enables users to securely manage their recipes. Built using Python's Flask framework, it offers features like user registration, authentication, recipe creation, viewing, updating, and deletion. The application is containerized using Docker and utilizes GitHub Actions for CI/CD to deploy on AWS EC2 instances.

![image](https://github.com/user-attachments/assets/d0a432db-f0b3-40da-a011-a6041a320ef4)


---

Features
1. User Authentication:
   - Secure user registration and login.
   - Passwords are hashed using Flask-Bcrypt for security.
   - Flask-Login manages user sessions.

2. Recipe Management:
   - CRUD (Create, Read, Update, Delete) functionality for recipes.
   - Users can add recipes with details like title, ingredients, and instructions.
   - View, update, or delete existing recipes.

3. Caching:
   - Frequently accessed pages are cached using Flask-Caching to improve performance.

4. Deployment:
   - The application is containerized with Docker and hosted on AWS EC2 instances.
   - CI/CD pipelines are implemented with GitHub Actions to automate testing, building, and deployment.

---

 System Requirements
- Python 3.8 or higher
- Flask 2.0.1
- Docker
- SQLite database
- AWS EC2 instance (for deployment)

---

Installation

1. Clone the Repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install Dependencies:
   Install Python dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Set Up the Database:
   Run the database initialization script to create the `users` and `recipes` tables:
   ```bash
   python -c "from database import init_db; init_db()"
   ```

4. Run the Application Locally:
   Start the Flask application:
   ```bash
   python app.py
   ```
   The application will run at `http://localhost:8080`.

---

Docker Setup

1. Build Docker Image:
   ```bash
   docker build -t recipe-app .
   ```

2. Run the Docker Container:
   ```bash
   docker run -d -p 8080:8080 --name recipe-container recipe-app
   ```

3. Access the Application:
   The application will be available at `http://localhost:8080`.

4. Push to Docker Hub (Optional):
   Tag and push the Docker image:
   ```bash
   docker tag recipe-app <your-dockerhub-username>/recipe-app
   docker push <your-dockerhub-username>/recipe-app
   ```

---

Deployment on AWS EC2

1. Provision an EC2 Instance:
   - Set up an EC2 instance with Docker pre-installed.

2. Pull the Docker Image:
   On the EC2 instance, pull the latest image from Docker Hub:
   ```bash
   docker pull <your-dockerhub-username>/recipe-app
   ```

3. Run the Docker Container:
   Start the container:
   ```bash
   docker run -d -p 8080:8080 recipe-app
   ```

4. Access the Application:
   Visit `http://<EC2-public-IP>:8080`.

---

CI/CD with GitHub Actions

1. Pipeline Steps:
   - Code is pushed to the repository.
   - GitHub Actions triggers workflows to:
     - Lint and test the code.
     - Build the Docker image.
     - Push the Docker image to Docker Hub.
     - Deploy the image to AWS EC2 via SSH.

2. Docker Configuration:
   Update `Dockerrun.aws.json` with the correct Docker image details.

3. Setup Environment Variables:
   Configure necessary environment variables like `FLASK_APP` and `FLASK_ENV` in the `Dockerrun.aws.json` file.

---

Folder Structure

```
├── app.py              # Main Flask application
├── database.py         # Database connection and initialization
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration (optional)
├── recipes.db          # SQLite database file
└── templates/          # HTML templates for the frontend
```

---

Known Issues

- Caching Invalidation: Cached pages may take up to 300 seconds to refresh. This timeout can be adjusted in the `app.py` configuration.
- Scalability: The application currently uses SQLite, which is suitable for low to moderate traffic. For higher scalability, consider migrating to a database like PostgreSQL.

---

Future Enhancements

- Add search and filtering options for recipes.
- Implement role-based access control for users.
- Integrate email notifications for recipe updates.
- Migrate to PostgreSQL for enhanced scalability.

---

Contributors
- Apoorv S  
- Contributions are welcome! Feel free to submit pull requests or raise issues.

For more information or queries, please contact: [apoorv2501@gmail.com]
