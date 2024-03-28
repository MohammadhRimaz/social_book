Social Book
Social Book is a Django-based social media platform where users can share images and interact with each other through comments and likes.

Features
User Authentication: Users can sign up, log in, and log out securely. Passwords are hashed for security.
Upload Posts: Users can upload images along with captions to share with others.
Interactions: Users can like posts and leave comments on them.
User Profiles: Each user has a profile page where their posts are displayed. Users can also edit their profiles and change their profile pictures.
Following System: Users can follow each other to see posts from users they follow on their feed.

Installation
1. Clone the repository:
   git clone https://github.com/your-username/social-book.git
2. Install dependencies:
   pip install -r requirements.txt
3. Apply database migrations:
   python manage.py migrate
4. Run the development server:
   python manage.py runserver
5. Access the application at http://localhost:8000/ in your web browser.

Technologies Used
Python
Django
HTML/CSS
JavaScript
SQLite (for development)
Contributing
Contributions are welcome! If you find any bugs or have feature requests, please open an issue on the GitHub repository. If you would like to contribute code, feel free to open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
