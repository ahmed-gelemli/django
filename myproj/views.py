from django.shortcuts import render
from django.http import HttpResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def homepage(request):
    
    return render(request , 'login_form.html')

def createaccounthomepage(request):
    f_create = open('templates/create.html')
    return HttpResponse(f_create)

# After this Google API Starts

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("myproj/creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Database").sheet1   #SheetName
usernameCol = sheet.col_values(1)
passwordCol = sheet.col_values(2)
emailCol = sheet.col_values(3)

# Before this Google API Ends

def submitted(request):
    data = request.POST.copy()
    context = {
        "username" : data.get('usernameInput'),
        "password" : data.get('passwordInput')
    }

    username = context['username'] 
    password = context['password']

    # Check Database Google Sheet

    usernameInput = username
    passwordInput = password
    f_accgrant = open('templates/accgrant.html', 'r')
    f_accnotgrant = open('templates/accnotgrant.html', 'r')
    if usernameInput in usernameCol:
        value_index = usernameCol.index(usernameInput)
        try:
            if passwordInput == passwordCol[value_index]:
                return HttpResponse(f_accgrant)
        except:
            return HttpResponse(f_accnotgrant)
    else:
        return HttpResponse(f_accnotgrant)

    # return render(request, 'submitted.html', context)

def createaccount(request):
    data = request.POST.copy()
    context = {
        "newusername" : data.get('NewUsernameInput'),
        "email" : data.get('inputEmail'),
        "newpassword" : data.get('NewPasswordInput'),
        "confirmpassword" : data.get('ConfirmPasswordInput')
    }

    newusername = context['newusername']
    email = context['email']
    newpassword = context['newpassword']
    confirmpassword = context['confirmpassword']

    if (newusername in usernameCol) or (email in emailCol):
        return HttpResponse("This Username or Email alredy in use. Please try another.")
    else:
        if len(newpassword) < 6:
            return HttpResponse("Password must be 6 or more character!")
        else:
            if newpassword == confirmpassword:
                newUserPassRow = [newusername , newpassword , email]
                sheet.append_row(newUserPassRow)
                return HttpResponse('We created your account. Welcome to family!')
            else:
                return HttpResponse("Passwords* aren't same! *(New Password and Confirm Password).")