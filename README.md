# ClimbersLog
#### Video Demo:  <https://youtu.be/7ebMZwiKYW8>
#### Description:
ClimbersLog is a comprehensive logbook designed to empower climbers to track, analyze, and enhance their climbing performance. This web application provides climbers with a user-friendly interface to record, visualize, and gain insights into their climbing sessions.

### Project Overview
- **Inspiration:** Climbing enthusiasts often desire a reliable tool to meticulously document their climbing sessions, monitor their progress, and uncover patterns in their performance. ClimbersLog was conceived to cater to this need by offering a user-friendly logbook.

- **Development Process:** The development of ClimbersLog commenced with the conceptualization of the website's design and feature set. HTML templates, combined with Flask routes, were employed to construct the website's structural foundation. A robust SQLite3 database was established, featuring tables for users, gyms, and climbing sessions. User authentication was diligently integrated, ensuring that only authenticated users can access the Sessions and History tabs.

### Features
- **User Registration and Login:** ClimbersLog simplifies user registration and secure login. User data is meticulously stored in a database, guaranteeing data security and privacy.

- **Sessions Tracking:** Climbers can seamlessly log their climbing sessions, capturing vital details such as the date, gym location, and performance metrics for each session. The website's intuitive interface streamlines data entry, making it hassle-free.

- **Key Performance Indicator (KPI):** ClimbersLog introduces a unique Key Performance Indicator (KPI) formula to calculate and summarize climbing session performance. The KPI is a dynamic metric that considers the level of difficulty, gym-specific levels, and the number of tops achieved during a session. This advanced formula provides a holistic assessment of a climber's performance.

- **Session Deletion:** Managing your climbing history is straightforward, as users can effortlessly delete unwanted sessions directly from the web interface.

- **Session History Visualization:** The History tab empowers climbers with data-driven insights. It presents an interactive plot of the KPI values for past sessions, enabling climbers to visualize their progress over time and identify areas for improvement.

### KPI Formula
ClimbersLog employs the following KPI formula to provide an overall summary of climbing performance:
```
kpi += ((level / gym_levels) ** 5) * tops
```
This formula ingeniously takes into account the session's level of difficulty, the gym's specific levels, and the number of tops achieved. The resulting KPI value encapsulates a climber's proficiency, allowing for an accurate assessment of their performance.

### Extended Features (Coming Soon)
- **Leaderboards:** Climbers can compare their performance with others through a leaderboard that showcases top climbers' KPI scores.

- **Goal Setting:** Set climbing goals and track progress towards achieving them.

- **Social Integration:** Share climbing accomplishments on social media platforms and connect with other climbers.

- **Detailed Analytics:** Gain deeper insights into climbing performance through advanced analytics and visualization tools.

### Get Started
To get started with ClimbersLog, follow these simple steps:
1. Clone this repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Create a virtual environment for your project to isolate dependencies.
4. Set up a SQLite3 database and apply migrations using Flask-Migrate.
5. Configure the Flask application to your preferred settings, including a secret key and database URI.
6. Run the application with `flask run`.

### Feedback and Contributions
ClimbersLog is an open-source project, and we welcome contributions from the climbing community. If you have suggestions, find bugs, or want to contribute new features, please open an issue or submit a pull request.

We are committed to continually improving ClimbersLog and making it the go-to logbook for climbers worldwide.

### License
ClimbersLog is not yet released but will in the future.

### Contact Us
For inquiries, suggestions, or support, feel free to contact us at [lars.tuerke@gmx.de](mailto:lars.tuerke@gmx.de).

Feel free to reach out if you have any questions, suggestions, or feedback. Happy climbing! 🧗‍♂️🧗‍♀️




