from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import io
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload


async def transver_withdraw(filename):
    try:
        try:
            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
            else:
                # Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")
            drive = GoogleDrive(gauth)
        except Exception as err:
            print(err)
            print("Ошибка входа")
        folder = "12XGaHoGMiFUqDa3k3rxYasv7G4f-ljEg"
        gfile = drive.CreateFile({"parents": [{"id": folder}], "title": filename})
        try:
            gfile.SetContentFile(filename)
        except Exception as err:
             print(err)
             print("\nОшибка сборки")
        
        gfile.Upload()
        file2 = drive.CreateFile({'id': gfile['id']})
        photo_id = file2['id']

        return photo_id
    except Exception as e:
        print('ERROR:', str(e))
        return {"success": False}
    

async def transver_from_withdraw_disc(photo_name, photo_id):
    try:

        try:
            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
            else:
                # Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")
            drive = GoogleDrive(gauth)
        except Exception as err:
            print(err)
            print("Ошибка входа")

        file = drive.CreateFile({'id': photo_id})
        file_url = file['alternateLink']

        file.GetContentFile(photo_name)

    except:
        print("Ошибка загрузки файла с диска")


async def transver_screen_to_disk(filename):
    try:
        try:
            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
            else:
                # Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")
            drive = GoogleDrive(gauth)
        except Exception as err:
            print(err)
            print("Ошибка входа")
        folder = "1mGtnRPULlONlQ1iDpNVoW7KFKCEJi5Dc"
        gfile = drive.CreateFile({"parents": [{"id": folder}], "title": filename})
        try:
            gfile.SetContentFile(filename)
        except Exception as err:
             print(err)
             print("\nОшибка сборки")
        
        gfile.Upload()
        file2 = drive.CreateFile({'id': gfile['id']})
        photo_id = file2['id']

        return photo_id
    except Exception as e:
        print('ERROR:', str(e))
        return {"success": False}






