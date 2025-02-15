#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#########################################################
# Name: generate_INNO_setup.py
# Porpose: make videomass.iss file for Inno Setup (Windows only)
# Compatibility: Python3
# Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
# Copyright: (c) 2020-2022 Gianluca Pernigotto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: June.20.2020
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
import os
import sys
import platform

if not platform.system() == 'Windows':
    sys.exit('ERROR: invalid platform. This script work on MS-Windows '
             'only, exit.')

this = os.path.realpath(os.path.abspath(__file__))
here = os.path.dirname(os.path.dirname(os.path.dirname(this)))
sys.path.insert(0, here)
try:
    from videomass.vdms_sys.msg_info import current_release
except ModuleNotFoundError as error:
    sys.exit(error)
# here = os.path.dirname(this)

cr = current_release()  # Gets informations
RLS_NAME = cr[0]  # first letter is Uppercase
PRG_NAME = cr[1]  # first letter is lower
VERSION = cr[2]
RELEASE = cr[3]
COPYRIGHT = cr[4]
WEBSITE = cr[5]
AUTHOR = cr[6]
EMAIL = cr[7]
COMMENT = cr[8]
BUILD_DIR = os.path.join(here, 'dist', RLS_NAME)  # dist/Videomass folder
COPYING = os.path.join(BUILD_DIR, 'DOC', 'LICENSE')
INFO_RTF = os.path.join(BUILD_DIR, 'DOC', 'NOTICE.rtf')
AUTH = os.path.join(BUILD_DIR, 'DOC', 'AUTHORS')
ICONS_PATH = os.path.join(BUILD_DIR, 'art', 'videomass.ico')
PATH_EXE = os.path.join(BUILD_DIR, '%s.exe' % RLS_NAME)

contents = r"""; Script generated by the Inno Setup Script Wizard.
; Edited by Gianluca jeanslack Pernigotto
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "%(RLS_NAME)s"
#define MyAppVersion "%(VERSION)s (64-bit)"
#define MyAppPublisher "%(AUTHOR)s"
#define MyAppURL "%(WEBSITE)s"
#define MyAppExeName "%(RLS_NAME)s.exe"
#define MyAppIcoName "videomass.ico"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{1608E2C6-6B13-4793-A9A6-6283E3BF1305}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=%(COPYING)s
InfoBeforeFile=%(INFO_RTF)s
InfoAfterFile=%(AUTH)s
OutputDir=%(here)s
OutputBaseFilename=%(RLS_NAME)s-v%(VERSION)s-x86_64-Setup
SetupIconFile=%(ICONS_PATH)s
Password=
Compression=lzma
SolidCompression=yes
CreateAppDir=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags:

[Files]
Source: "%(PATH_EXE)s"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(BUILD_DIR)s\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcoName}"; WorkingDir: "{app}"
Name: "{group}\Uninstall %(RLS_NAME)s"; Filename: "{uninstallexe}"
Name: "{group}\Website"; Filename: "%(WEBSITE)s"

Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}";IconFilename: "{app}\{#MyAppIcoName}"; Tasks: desktopicon
; Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}";IconFilename: "{app}\{#MyAppIcoName}";
; Name: "{commonstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}";IconFilename: "{app}\{#MyAppIcoName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
""" % {
       "RLS_NAME": RLS_NAME,
       "AUTHOR": AUTHOR,
       "WEBSITE": WEBSITE,
       "VERSION": VERSION,
       "COPYING": COPYING,
       "INFO_RTF": INFO_RTF,
       "AUTH": AUTH,
       "here": here,
       "ICONS_PATH": ICONS_PATH,
       "PATH_EXE": PATH_EXE,
       "BUILD_DIR": BUILD_DIR,
       }


def createinno():
    """
    Generate a inno file (.iss) in order to make a videomass installer
    for MS-Windows. To use this file is required to install Inno
    Setup, see web page at <https://jrsoftware.org/isinfo.php> .

    """
    innofile = os.path.join(here, '%s_v%s.iss' % (PRG_NAME, VERSION))

    with open(innofile, 'w') as inno:
        inno.write(contents)


if __name__ == '__main__':
    if not os.path.exists(BUILD_DIR) and not os.path.isdir(BUILD_DIR):
        sys.exit('ERROR: You should first create a videomass bundle with '
                 'pyinstaller.')
    elif '%s.exe' % RLS_NAME not in os.listdir(BUILD_DIR):
        sys.exit('ERROR: %s.exe bundle is missing in dist folder.' % RLS_NAME)
    else:
        createinno()
