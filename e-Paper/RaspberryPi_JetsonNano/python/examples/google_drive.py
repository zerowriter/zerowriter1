from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def get_drive_service(credentials_path, scopes):
    # Load the service account credentials from the JSON key file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scopes
    )

    # Create a Google Drive API client
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

def upload_file(file_path, parent_folder_id=None):
    # Initialize the Google Drive API client
    drive_service = get_drive_service('path/to/your/credentials.json', ['https://www.googleapis.com/auth/drive'])

    # Prepare metadata for the file
    file_metadata = {'name': file_path}
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    # Upload the file
    media = MediaFileUpload(file_path)
    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()

    return uploaded_file.get('id')
