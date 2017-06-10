#!/usr/bin/env python
import os
import shutil
import zipfile
import xml.etree.cElementTree as ElementTree

dir = os.path.dirname(__file__)

def getFilename(xmlPath):
    file = ElementTree.parse(xmlPath).getroot()
    version = file.get('version')
    addon_id = file.get('id')
    return addon_id + "-" + version


def zipDir(path, filename):
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

def populateRepo(xmlPath):
    zipfilename = getFilename(xmlPath) + ".zip"
    file = ElementTree.parse(xmlPath).getroot()
    addon_id = file.get('id')
    version = file.get('version')
    destPath = dir + os.sep + "zips" + os.sep + addon_id + os.sep
    ensure_dir(destPath)
    if not move(zipfilename, destPath):
        os.remove(zipfilename)
    copy(dir + os.sep + addon_id + os.sep + "changelog.txt", destPath + "changelog-" + version + ".txt")
    copy(dir + os.sep + addon_id + os.sep + "icon.png", destPath + "icon.png")
    copy(dir + os.sep + addon_id + os.sep + "fanart.png", destPath + "fanart.png")
    copy(dir + os.sep + addon_id + os.sep + "icon.jpg", destPath + "icon.jpg")
    copy(dir + os.sep + addon_id + os.sep + "fanart.jpg", destPath + "fanart.jpg")

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def copy(orig, dest):
    try:
        shutil.copyfile(orig, dest)
    except:
        print "Error copying, skipping..."
        return False

def move(orig, dest):
    try:
        shutil.move(orig, dest)
    except:
        print "Error moving, skipping..."
        return False

def createAddonZip(addonPath, xmlPath):
    filename = getFilename(xmlPath)
    zipDir(addonPath, filename + '.zip')


def testRoutine():
    createAddonZip("service.subtitles.tusubtitulo/", "service.subtitles.tusubtitulo/addon.xml")
    populateRepo("service.subtitles.tusubtitulo/addon.xml")
