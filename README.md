# teacherpal-backend
TacherPal is a solution to track attentivity of students in online classes. It helps the teacher to take attendances and quizzes via chrome extension and track students' responses via web portal. This repository contains code for the API endpoints required for the extensions. It also contains code for both teacher and student side dashboards.

**Tech Stack-** Django, Django Rest Framework, SQLite3

## Project Setup Guide:
- Clone the repository
- After going into the required directory make a vitual environment and activate it (optional but preferrable)
- Run `pip install -r requirements.txt`  to install all the requirements/dependencies. 
(**Note**- Your system must have python installed (version >= 3.7.6))
- You will have to run a migration to make the specific tables in the database so run the following command terminal:      
 `python manage.py migrate`        
- **Creating superuser**- This will give you the access to the admin page of the website. To make a superuser run `python manage.py createsuperuser` in the terminal and specify the details.
- Now you are good to go! Finally run `python manage.py runserver` or `python manage.py runserver <hostip>`to run the django application.

### Links to other parts of the project
- [https://github.com/ApoorvaRajBhadani/teacherpal-host](https://github.com/ApoorvaRajBhadani/teacherpal-host) - Extension for Teachers
- [https://github.com/ApoorvaRajBhadani/teacherpal-attendee](https://github.com/ApoorvaRajBhadani/teacherpal-attendee) - Extension for Students
- [https://github.com/ApoorvaRajBhadani/teacherpal-pushserver](https://github.com/ApoorvaRajBhadani/teacherpal-pushserver) - Push notification server
- [https://github.com/ParthKhanna07/teacher-pal](https://github.com/ParthKhanna07/teacher-pal) - Frontend webapp



**Note-** For complete demo of the project refer to [link](https://www.youtube.com/watch?v=ptUJ4uGR3Og)
