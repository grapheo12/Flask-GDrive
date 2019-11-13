from __future__ import print_function
import pickle
import os.path
import threading
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from flask import current_app, _app_ctx_stack, Response, url_for

class GDriveMain:
    def __init__(self, app, creds, token, *args):
        self.app = app
        self.folder_id = ""
        if app is not None:
            app.config.setdefault('GDRIVE_CREDENTIALS_URI', creds)
            app.config.setdefault('GDRIVE_TOKEN_URI', token)
            self.init_app(app, *args)
    
    def init_app(self, app, *args):
        pass
        #To be implemented separately.

    def connect(self):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/spreadsheets'
        ]
        creds = None
        if os.path.exists(current_app.config['GDRIVE_TOKEN_URI']):
            with open(current_app.config['GDRIVE_TOKEN_URI'], 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    current_app.config['GDRIVE_CREDENTIALS_URI'], SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(current_app.config['GDRIVE_TOKEN_URI'], 'wb') as token:
                pickle.dump(creds, token)

        return creds


class GDriveStatic(GDriveMain):
    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'gdrive_service'):
            ctx.gdrive_service = None
    
    def init_app(self, app, *args):
        remote_folder = args[0]
        app.config.setdefault('GDRIVE_STATIC_FOLDER', remote_folder)
        app.teardown_appcontext(self.teardown)
    
    @property
    def gdrive_service(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'gdrive_service'):
                creds = self.connect()
                service = build('drive', 'v3', credentials=creds)     
                result = service.files().list(
                    pageSize=1, fields='nextPageToken, files(id, mimeType)', q="name='{}'".format(current_app.config['GDRIVE_STATIC_FOLDER'])).execute()
                items = result.get('files', [])

                if not items:
                    raise IOError("Folder not found in Google Drive")
                else:
                    self.folder_id = items[0]['id']
                ctx.gdrive_service = service

                print(self.folder_id)
            return ctx.gdrive_service

    def fileHandler(self, fpath):
        name, ext = os.path.splitext(fpath)
        doc_mimetypes = {
            '.html': 'text/html',
            '.txt': 'text/plain',
        }

        other_mimetypes = {
            '.pdf': 'application/pdf',
            '.jpeg': 'image/jpeg',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
            '.svg': 'image/svg'
        }

        results = self.gdrive_service.files().list(
            pageSize=1, fields="nextPageToken, files(id, mimeType)", q=f"name='{fpath}' and '{self.folder_id}' in parents").execute()
        items = results.get('files', [])
        if not items:
            raise IOError('File Not Found')
        else:
            file_id = items[0]['id']
            if ext in doc_mimetypes:
                res = self.gdrive_service.files().export_media(fileId=file_id,
                    mimeType=doc_mimetypes[ext]).execute()
                return res, 200
            else:
                res = self.gdrive_service.files().get_media(fileId=file_id).execute()
                try:
                    return Response(res, mimetype=other_mimetypes[ext])
                except:
                    return res, 200

    def g_url_for(self, fpath):
        return url_for('fileHandler', fpath=fpath)


class GDriveDB(GDriveMain):
    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'gdrive_db'):
            ctx.gdrive_service = None
    
    def init_app(self, app, *args):
        self.remote_sheets = args[0]
        self.RANGE = 'A1:Z'
        if len(args) > 1:
            cache_update = args[1]
        else:
            cache_update = 0

        # app.config.setdefault('GDRIVE_DB_ID', remote_sheet)
        self.cache_update_time = cache_update
        app.teardown_appcontext(self.teardown)
    
    @property
    def gdrive_db(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'gdrive_db'):
                creds = self.connect()
                service = build('sheets', 'v4', credentials=creds)
                sheet = service.spreadsheets()
                
                
                self.global_values = dict()
                for s in self.remote_sheets:
                    result = sheet.values().get(spreadsheetId=self.remote_sheets[s], range=self.RANGE).execute()
                    values = result.get('values', [])

                    if not values:
                        raise IOError("Sheet not found")
                    else:
                        self.global_values[s] = values
                    
                    
                ctx.gdrive_db = self.global_values
                self.sheet = sheet 
                # self.update_thread = threading.Thread(target=lambda: self.update_cache())
                # self.update_thread.start()
            return ctx.gdrive_db

    def update(self, sheet_name):
        result = self.sheet.values().update(
                spreadsheetId=self.remote_sheets[sheet_name], range=self.RANGE,
                body={'values': self.global_values[sheet_name]}, valueInputOption="RAW").execute()



    # def update_cache(self):
    #     time.sleep(self.cache_update_time)
    #     print("Updating cache")
    #     #TODO
