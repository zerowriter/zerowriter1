import sys
import json
import yagmail

# this script handles loading gmail credentials, saving credentials, 
# emailing contents, and etc
# 

class GmailCredentials:
    @staticmethod
    def load_gmail_username():
        # Load JSON data from the file
        with open('zwconfig.json', 'r') as file:
            data = json.load(file)
        username = data.get('username')
        return username

    @staticmethod
    def load_gmail_password():
        # Load JSON data from the file
        with open('zwconfig.json', 'r') as file:
            data = json.load(file)
        password = data.get('password')
        return password

    @staticmethod
    def write_gmail_credentials(username, password):
        # Load JSON data from the file
        with open('zwconfig.json', 'r') as file:
            data = json.load(file)
        # Update the data with the new username and password
        data['username'] = username
        data['password'] = password
        # Open the JSON file in write mode to write the updated data
        with open('zwconfig.json', 'w') as file:
            json.dump(data, file)

    @staticmethod
    def write_gmail_username(username):
        # Load JSON data from the file
        with open('zwconfig.json', 'r') as file:
            data = json.load(file)
        data['username'] = (username + '@gmail.com')
        # Open the JSON file in write mode to write the updated data
        with open('zwconfig.json', 'w') as file:
            json.dump(data, file)

    @staticmethod
    def write_gmail_password(password):
        # Load JSON data from the file
        with open('zwconfig.json', 'r') as file:
            data = json.load(file)
        data['password'] = password
        # Open the JSON file in write mode to write the updated data
        with open('zwconfig.json', 'w') as file:
            json.dump(data, file)

    @staticmethod
    def send_gmail(username, password, contents):
        try:
            yag = yagmail.SMTP(username, password)
            yag.send(username, 'ZeroWriter Mail', contents)
        except Exception as e:
            print (e)
            return

    @staticmethod
    def check_connection(username, password):
        try:
            yag = yagmail.SMTP(username, password)
            yag.login()
            return("Connected")
        except Exception as e:
            #print (e)
            return("Disconnected")

if __name__ == '__main__':
    print("testing")
    username = GmailCredentials.load_gmail_username()
    password = GmailCredentials.load_gmail_password()

    contents = ['test']
    print(GmailCredentials.check_connection(username, password))
