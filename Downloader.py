from General import General
import os
import shutil

class Downloader (General):
    def __init__ (self):
        self.config = self.load_json(os.path.join("./", "configs", "main.json"))
        self.downloads = self.load_json(os.path.join("./", "configs", "downloads.json"))
        self.setInterval(self.updateDeletedDownloads, 20)

    def updateDeletedDownloads (self):
        for download in self.downloads["deleted_downloads"]:
            try:
                self.httpPost({
                    "operation": "delete-download",
                    "id": download
                })
            catch Exception as e:
                print(e)

    def getDownloads (self):
        downloads = os.listdir(os.path.join("./", "downloads"))
        return downloads
    
    def loadDownload (self, downloadConfigFile):
        return self.load_json(os.path.join("./", "downloads", downloadConfigFile))

    def newDownload (self, url, savePath, saveName = "", overwrite = False, chunkSize = False):
        if not chunkSize:
            chunkSize = self.config["chunkSize"]

        if not overwrite:
            for [downloadUrl, downloadSavePath] in self.downloads["downloads"]:
                if url != downloadUrl and downloadSavePath != savePath:
                    continue

                return self.sendFalse({
                    "data": "A similar download already exists"
                })

        try:
            downloadData = self.httpPost(
                os.path.join(self.config["server"], "Mkshift-Downloader", "new-download.php"),
                {
                    "operation": "new-download",
                    "url": url,
                    "chunkSize": 512,
                    "downloaded": 0,
                    "fileSize": 0,
                    "id": None,
                    "savePath": savePath,
                    "completed": False
                }
            )

            self.save_json(os.path.join("./", "downloads", downloadData["id"]), downloadData)

            with open(os.path.join(self.config["temp_dir"], downloadData["id"]), "w") as downloadFile:
                downloadFile.write("")

            return self.sendTrue({
                "data": "Configured new download"
            })
        except Exception as e:
            return self.sendFalse({
                "data": e
            })

    def continueDownload (self, download):
        try:
            downloadData = self.httpPost(
                os.path.join(self.config["server"], "Mkshift-Downloader", "continue-download.php"),
                {
                    "id": download["id"]
                }
            )

            self.save_json(os.path.join("./", "downloads", download["id"]), downloadData)

            with open(os.path.join(self.config["temp_dir"], downloadData["id"]), "a") as downloadFile:
                downloadFile.write(downloadData["currentChunk"])

            return self.sendTrue({
                "data": "Got a chunk!"
            })
        except Exception as e:
            return sendFalse({
                "data": e
            })

    def deleteDownload (self, download, deleteFile = False):
        if os.path.isfile(os.path.join("./", "downloads", download["id"])):
            try:
                self.httpPost(
                    os.path.join(self.config["url"], "Mkshift-Downloader", "delete-download.php"),
                {
                    "operation": "delete-download",
                    "id": download["id"]
                })
            except Exception as e:
                self.downloads["deleted_downloads"].append(download["id"])
            
            if deleteFile:
                if download["completed"]: # If the download completed
                    os.unlink(download["savePath"]) # Delete the downloaded file
                else:
                    os.unlink(os.path.join(self.config["temp_dir"], download["id"])) # Delete the temp file
            else:
                shutil.move(
                    os.path.join(self.config["temp_dir"], download["id"]),
                    download["savePath"]
                )

            os.unlink(os.path.join("./", "downloads", download["id"])

            return self.sendTrue({
                "data": "The download has been deleted successfully"
            })
        else:
            return self.sendFalse({
                "data": "The download does not exist!"
            })

    def saveDownloadData (self):
        self.save_json("./configs/downloads.json", self.downloads)

if __name__ == "__main__":
    downloader = Downloader()