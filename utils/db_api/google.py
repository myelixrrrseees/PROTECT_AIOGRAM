from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_drive():
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
    return drive


async def transver_withdraw(filename):
    try:
        drive = get_drive()
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
        drive = get_drive()

        file = drive.CreateFile({'id': photo_id})
        file_url = file['alternateLink']

        file.GetContentFile(photo_name)

    except:
        print("Ошибка загрузки файла с диска")


async def transver_screen_to_disk(filename):
    try:
        drive = get_drive()
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






