from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleDriveApi():
    def __init__(self):
        self.__gauth = GoogleAuth()           
        self.__drive = GoogleDrive(self.__gauth)

    def api_access(self):
        return self.__drive

    def upload_files(self, list_of_files, folder_id):
        
        for file in list_of_files:
            gfile = self.__drive.CreateFile({'parents': [{'id': folder_id}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(file)
            gfile.Upload() # Upload the file.

    def get_files_at_directory(self, folder_id):
        return self.__drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()

    def download_file(self, folder_id):
        file_list = self.get_files_at_directory(folder_id)
        for file in file_list:
            file_id = file['id']
        file = self.__drive.CreateFile({'id': file_id,'parents': [{'id': folder_id}]}) 
        content = file.GetContentString()

        return file,content

    def update_gdrive_file(self, gfile, content):
        gfile.SetContentString(content)
        gfile.Upload()