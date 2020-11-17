# [GymTracker](https://gymtrackerduke.herokuapp.com/) 🤸🏋️🚴💙

## Introduction
Tired of waiting for the treadmill to free up? Want to ensure you get the workout your body deserves?

(_Drumroll..._)

Presenting [GymTracker](https://gymtrackerduke.herokuapp.com/) . A combined portal for Duke students to reserve gym equipment, view and enroll in fitness classes, and manage their workout schedule! GymTracker allows you to view equipment and resources available by their location, reserve equipment in times that work for you, find and enroll in exciting classes - and manage all of your bookings, just with a click!

## How We Built This
1. Database: MySQL
2. App framework: Flask (/Jinja templating)
3. Authentication: Firebase
4. Deployement: Heroku

## Screenshots
*GymTracker Homepage*
![homepage](screenshots\homepage.png)

*Brodie Equipment*
![brodie equipment](screenshots\brodie_equipment.png)

## What's next?
- Admin Management
- Calories and workout tracking


## Learn More
![learnmore](screenshots\Boxing.gif)




## Running it Locally

1. Clone the repo
  ```
  $ git clone git@github.com:himanshukj17122000/316-Gym-Tracker.git
  $ cd 316-Gym-Tracker
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

