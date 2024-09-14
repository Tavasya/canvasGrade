from dotenv import load_dotenv
import os
import requests
import yagmail

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
apiKey = os.getenv('CANVAS_API_TOKEN')
apiUrl = os.getenv('CANVAS_API_URL')

# Set up headers for authorization
headers = {
    'Authorization': f'Bearer {apiKey}'
}

# Email setup
sender = 'tavasyag@gmail.com'
receiver = 'tavasyag@gmail.com'
appPassword = os.getenv('APP_PASSWORD')

# Initialize yagmail SMTP
yag = yagmail.SMTP(user=sender, password=appPassword)

def get_courses():
    # Fetch the user's enrollments
    response = requests.get(f'{apiUrl}users/self/enrollments', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch courses. Status code: {response.status_code}")
        return []

def get_course_details(course_id):
    # Fetch course details using the course_id
    response = requests.get(f'{apiUrl}courses/{course_id}', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch details for course {course_id}. Status code: {response.status_code}")
        return {}

def send_email_notification(subject, message):
    # Send email notification using yagmail
    try:
        yag.send(to=receiver, subject=subject, contents=message)
        print("Email sent")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_grades():
    courses = get_courses()
    for course in courses:
        course_id = course['course_id']  # Extract the course_id from enrollments
        
        # Fetch additional course details using the course_id
        course_details = get_course_details(course_id)
        course_name = course_details.get('name', 'Unknown Course')  # Get the course name or use a default value

        # Get the student's enrollment information for the specific course
        if 'grades' in course and course['type'] == 'StudentEnrollment':
            current_score = course['grades'].get('current_score')  # Use correct key 'current_score'
            if current_score is not None and float(current_score) < 100:  # Set your own threshold
                subject = f"Grade Alert for {course_name}"
                message = f"Your grade in {course_name} has dropped to {current_score}."
                send_email_notification(subject, message)

# Call the function to check grades and send notifications
check_grades()
