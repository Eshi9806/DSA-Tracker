# DSA Tracker
#### Video Demo: https://youtu.be/87Z3za1qsjc

#### Description:
DSA Tracker is lightweight Flask web application designed for engineering students to track and organize Data Structures & Algorithms problem-solving across platforms. It is a platform made to track the DSA problems solved, the key points to note after solving a problem, and categorise it according to difficulty and status. We can add theory URLs, question URLs for future reference, and we can edit and delete the problem as well. It is authenticated and needs a user ID and password every time one opens the website.

### File Structure & Overview
In this project, each file plays a specific role in connecting the Flask backend, SQLite database, and Jinja2 frontend templates.

* **`app.py`**: It is the main document which is connecting backend to frontend, connecting HTML pages to SQL databases. Storing info given by user, editing it and storing all user names using HTML forms and saving it in backend in SQLite database. We have used a lot of routes in `app.py` for easier access to all basic facilities:
  1. `/` route: It is used to show basic dashboard using `user_id` and accessing the SQL database stored from that `user_id`.
  2. `/login` route: It is used for logging in the user using user name and password.
  3. `/logout` route: This route is used to log the user out from the website and redirect to the login page.
  4. `/add` route: This route is used to add problems into the DSA tracker using Jinja templates in HTML, storing data in a table and showing it on the website using Bootstrap and HTML.
  5. `/edit` route: This route is used to edit the problems added into the DSA tracker.
  6. `/delete` route: This route is used to delete the problem in DSA tracker.
  7. `/register` route: This route is used to register a new user and after registering it redirects to the login page.

* **`helpers.py`**: It helps us to authenticate users and get a `user_id` to help us run the website smoothly.

* **`schema.sql`**: We made all our tables through this. Users table which stores username and password and problems table which stores the name of problem, difficulty, status, theory link, question link and notes that you get while solving the problem are made in `schema.sql`.

* **`templates/` directory**: It is the basis of our whole website. How we are perceiving things and how a form looks. Everything is done in templates directory. It has various documents:
  1. `layout.html`: It is the basis of the layout for all the HTML pages inside the directory and we are using Jinja to access it and use it for others as well.
  2. `add.html`: We are redirected to `add.html` when we click on add a problem. We have written the code for showing a form to submit the problems.
  3. `edit.html`: We are redirected to `edit.html` when we click on edit in the dashboard. This helps us to edit the problem we stored.
  4. `register.html`: We are redirected to this page when we click on register on the top right corner. It helps us to register as a new user.
  5. `login.html`: We are redirected to this page when we click on login and this is the default page when we open the site. It helps us to login by entering our username and password.

### Key Design Choices

* **Database Choice (SQLite):** I chose SQLite because it allows relational data handling for connecting users to their specific problems. Using a foreign key (`user_id`) in the problems table ensures data isolation, so users only see and manage their own logged problems without interfering with other accounts.
* **Security & Route Protection:** Security was a major priority. Passwords are never stored in plain text; instead, they are hashed before being saved to the database. Additionally, using a custom `@login_required` decorator on protected routes prevents unauthorized access by ensuring users cannot view, edit, or delete entries without an active session.
* **User Interface & Experience (Bootstrap & Badges):** For the frontend, I used Bootstrap to create a clean, responsive layout. I incorporated color-coded badges for difficulty levels (Easy, Medium, Hard) and completion statuses (Not Started, In Progress, Completed). This makes the dashboard visually intuitive, allowing users to assess their progress at a glance.

### Key Features
- **User Authentication:** Secure registration and session management.
- **Topic Categorization:** Track status by topics (Arrays, Graphs, DP).
- **Interactive Dashboard:** Visual progress tracking using SQLite queries.

### Local Setup Instructions
1. Clone repository: `git clone <your-repository-url>`
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Run app: `python app.py`