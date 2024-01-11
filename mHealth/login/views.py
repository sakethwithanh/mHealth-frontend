
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
import csv
from django.http import HttpResponse
import io
import requests
def generate_hl7(request):
    # URL of the file in the GitHub repository
    file_url = 'https://raw.githubusercontent.com/sakethwithanh/mHealth-frontend/main/AHLSAM018434.csv'

    try:
        # Download the file and save it as a string
        csv_file_content = requests.get(file_url).text

        # Read data from CSV content directly
        csv_reader = csv.DictReader(csv_file_content.splitlines())
        dataset = list(csv_reader)

        # Create an HL7 message template (MSH segment)
        hl7_message = (
            "MSH|^~\\&|YourApp|YourFacility|HL7Server|HL7Server|20230908170000||ORU^R01|123456|P|2.5|||\n"
        )

        # Iterate through the dataset and create an HL7 message for each record
        for record in dataset:
            # Create a new HL7 message for each record
            hl7_message += f"PID|1||{record['Time']}||{record['Sleep']}|||\n"

            # OBX segment for GSR
            obx_gsr = (
                f"OBX|1|NM|GSR^Galvanic Skin Response^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['GSR']}\n"
            )
            hl7_message += obx_gsr

            # OBX segment for CBT
            obx_cbt = (
                f"OBX|2|NM|CBT^Core Body Temperature^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['CBT(degC)']}\n"
            )
            hl7_message += obx_cbt

            # OBX segment for PPG
            obx_ppg = (
                f"OBX|3|NM|PPG^Photoplethysmogram^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['PPG']}\n"
            )
            hl7_message += obx_ppg

            # OBX segment for ECG
            obx_ecg = (
                f"OBX|4|NM|ECG^Electrocardiogram^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['ECG']}\n"
            )
            hl7_message += obx_ecg

        # Set the proper content type for plain text
        response = HttpResponse(hl7_message, content_type='text/plain')
        
        # Set the Content-Disposition header to inline
        response['Content-Disposition'] = 'inline; filename="hl7_messages.hl7"'
        
        return response

    except requests.exceptions.RequestException as e:
        # Handle the exception (print/log the error, return an appropriate response, etc.)
        print(f"Error fetching data from GitHub: {e}")
        return HttpResponse("Internal Server Error", status=500)

def download_hl7(request):
    # URL of the file in the GitHub repository
    file_url = 'https://raw.githubusercontent.com/sakethwithanh/mHealth-frontend/main/AHLSAM018434.csv'

    try:
        # Download the file and save it as a string
        csv_file_content = requests.get(file_url).text

        # Read data from CSV content directly
        csv_reader = csv.DictReader(csv_file_content.splitlines())
        dataset = list(csv_reader)

        # Create an HL7 message template (MSH segment)
        hl7_message = (
            "MSH|^~\\&|YourApp|YourFacility|HL7Server|HL7Server|20230908170000||ORU^R01|123456|P|2.5|||\n"
        )

        # Iterate through the dataset and create an HL7 message for each record
        for record in dataset:
            # Create a new HL7 message for each record
            hl7_message += f"PID|1||{record['Time']}||{record['Sleep']}|||\n"

            # OBX segment for GSR
            obx_gsr = (
                f"OBX|1|NM|GSR^Galvanic Skin Response^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['GSR']}\n"
            )
            hl7_message += obx_gsr

            # OBX segment for CBT
            obx_cbt = (
                f"OBX|2|NM|CBT^Core Body Temperature^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['CBT(degC)']}\n"
            )
            hl7_message += obx_cbt

            # OBX segment for PPG
            obx_ppg = (
                f"OBX|3|NM|PPG^Photoplethysmogram^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['PPG']}\n"
            )
            hl7_message += obx_ppg

            # OBX segment for ECG
            obx_ecg = (
                f"OBX|4|NM|ECG^Electrocardiogram^HL7|||{record['Time']}|||||AmplitudeData^{record['Time']}^Units|{record['ECG']}\n"
            )
            hl7_message += obx_ecg

        # Set the proper content type for plain text
        response = HttpResponse(hl7_message, content_type='text/plain')
        
        # Set the Content-Disposition header to trigger download
        response['Content-Disposition'] = 'attachment; filename="hl7_messages.hl7"'
        
        return response

    except requests.exceptions.RequestException as e:
        # Handle the exception (print/log the error, return an appropriate response, etc.)
        print(f"Error fetching data from GitHub: {e}")
        return HttpResponse("Internal Server Error", status=500)


def HomePage(request):
    return render(request,'home.html')
def SignupPage(request):
    error_message = None  # Initialize error_message to None

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if the username is already in use
        if User.objects.filter(username=uname).exists():
            error_message = 'This username is already taken. Please choose a different one.'
        else:
            # Use EmailValidator to validate the email
            email_validator = EmailValidator()
            try:
                email_validator(email)
            except ValidationError:
                error_message = 'Invalid email address'
            
            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                error_message = 'This email is already registered.'

            # Check if passwords match and are at least 8 characters long
            if pass1 != pass2:
                error_message = 'Passwords do not match.'
            elif len(pass1) < 8:
                error_message = 'Password must be at least 8 characters long.'

            if error_message is None:  # No error, create the user
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                return redirect('login')

    return render(request, 'signup.html', {'error_message': error_message})



def LoginPage(request):
    error_message = ''  # Initialize error_message to an empty string

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Username or password is incorrect'

    return render(request, 'login.html', {'error_message': error_message})

def LogoutPage(request):
    logout(request)
    return redirect('login')



def SheetPage(request):
    return render(request, 'sheets.html')

# views.py

def download_csv_data(request):
    # Replace this with your logic to fetch data from the Google Sheet
    # For example, you can use gspread library or any other method to get the data
    sheet_data = [
        ["Header1", "Header2", "Header3"],
        ["Data1", "Data2", "Data3"],
        # Add more rows as needed
    ]

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="google_sheet_data.csv"'

    # Create a CSV writer and write the data to the response
    csv_writer = csv.writer(response)
    for row in sheet_data:
        csv_writer.writerow(row)

    return response
