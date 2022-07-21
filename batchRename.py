import os

for chapter in os.listdir("rawkumaDownloads/"):
    chapterBasePath = "rawkumaDownloads/" + chapter + "/"
    for pagePath in os.listdir(chapterBasePath):
        chapterNum = pagePath.split(".")[0]
        os.rename(chapterBasePath + pagePath, chapterBasePath + chapterNum + ".jpg")
print("Done")