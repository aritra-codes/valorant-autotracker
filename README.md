<h1 align="center">
  <br>
  <img src="readme_images/logo.png" alt="Valorant AutoTracker logo" width="200">
  <br>
  Valorant AutoTracker
  <br>
</h1>

`Valorant AutoTracker` uploads all your Valorant matches to YouTube and puts them on a spreadsheet in the click of a button! 🔘👆

---

# This project is not affiliated with Riot Games. Go to the bottom for more information.

# ⬇️ Installation & Setup

Currently, only [Windows](https://www.microsoft.com/en-gb/windows) is supported (as Valorant does not support other OSes).

## GUI Installation

**Video Tutorial:**
<br/>
<img src="readme_images/video_thumbnail.png" alt="Valorant AutoTracker logo" width="500">

## Setup (only the complicated parts)

- Auto-upload to YouTube:
  - Download [Firefox](https://www.mozilla.org/en-US/firefox/new).
  - Turn on the 'Auto-Upload Videos' setting.
    <br/>
    <img src="readme_images/auto_upload_videos.png" alt="Auto-upload Videos setting">
  - Add a [new firefox profile](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles) and copy the root directory path into the 'Firefox Profile Path' setting.
    <br/>
    ![Root directory of profile](readme_images/root_directory.png)
    <br/>
    ![Firefox Profile Path setting](readme_images/firefox_profile_path.png)
  - Save your settings.
    <br/>
    ![Save settings](readme_images/save_settings.png)
  - Go to [YouTube Studio](https://studio.youtube.com) and log in.
  - Choose the YouTube channel to which you like to upload your matches (**if there is a 'Don't ask again' option, select it**).
- Insert to Google Sheets:
  - Go to [Google Cloud](https://console.cloud.google.com) and log in.
  - Create a [new project](https://console.cloud.google.com/projectcreate) and name it anything (e.g. Valorant AutoTracker)
  - Go to [APIs and services](https://console.cloud.google.com/apis), then to [Enabled APIs and services](https://console.cloud.google.com/apis/dashboard) and click the 'ENABLE APIS AND SERVICES' button.
    <br/>
    <img src="readme_images/enable_apis.png" alt="'ENABLE APIS AND SERVICES' button">
  - Enable the [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) and [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com).
  - Go back to [APIs and services](https://console.cloud.google.com/apis), then to [Credentials](https://console.cloud.google.com/apis/credentials), click the 'CREATE CREDENTIALS' button and choose the 'Service account' option.
    <br/>
    <img src="readme_images/create_service_account.png" alt="Create 'Service account' option">
  - Enter any Service account name (e.g. Valorant Spreadsheet Updater) and click the 'DONE' button.
  - Copy the service account's email, go to your Google Sheets spreadsheet and share it with this email as Editor.
    <br/>
    <img src="readme_images/service_account_email.png" alt="Service account email">
    <br/>
    <img src="readme_images/share_google_sheets.png" alt="Sharing Google Sheets spreadsheet">
  - Go back to the service account and click the 'Edit service account' button.
    <br/>
    <img src="readme_images/edit_service_account.png" alt="'Edit service account' button">
  - Go the 'KEYS' section, click 'ADD KEY', choose 'Create new key', choose JSON as the key type and click the 'CREATE' button. A .json file will be downloaded, save this to a memorable location (e.g. the Valorant AutoTracker folder).
  - Turn on the 'Google Sheets' setting, type in your spreadsheet's name in the 'Spreadsheet Name' setting and choose the location of the .json file you downloaded in the 'Google Service Acc. Key' setting.
    <br/>
    <img src="readme_images/google_sheets_setting.png" alt="'Google Sheets' setting and more">

---

# 💪 Team

<img src="https://github.com/aritra-codes.png" alt="Profile picture of aritra-codes" height="200"/> | <img src="https://github.com/lmdrums.png" alt="Profile picture of lmdrums" height="200"/>
---|---
[Aritra (aritra-codes)](https://github.com/aritra-codes) | [Lewis M (lmdrums)](https://github.com/lmdrums)
Backend | Frontend

---

# ❤️ Credits

- Big thanks to [Henrik-3](https://github.com/Henrik-3) and his [unofficial-valorant-api](https://github.com/Henrik-3/unofficial-valorant-api) for making this project possible.
- Massive thanks to [Tom Schimansky](https://github.com/TomSchimansky) with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for making the UI possible.

---

# Message for Riot Games

This application does not modify Valorant in any way. 
It only makes a request to the [unofficial-valorant-api](https://github.com/Henrik-3/unofficial-valorant-api) to get user and match data.
If you have any problems with this project, please send me an email at aritra8.codes@gmail.com.
