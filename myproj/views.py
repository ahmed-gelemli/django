from django.shortcuts import render
from django.http import HttpResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def homepage(request):
    
    return render(request , 'login_form.html')

# After this Google API Start

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("myproj/creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Database").sheet1   #SheetName
usernameCol = sheet.col_values(1)
passwordCol = sheet.col_values(2)


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

    if usernameInput in usernameCol:
        value_index = usernameCol.index(usernameInput)
        try:
            if passwordInput == passwordCol[value_index]:
                return HttpResponse("Access Granted!")
        except:
            return HttpResponse("Check your Password!")
    else:
        return HttpResponse("Check your Username!")

    # return render(request, 'submitted.html', context)