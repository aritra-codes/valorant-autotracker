<div align="center">
  <img src="readme_files/logo.png" alt="Valorant AutoTracker logo" width="200">

  # Valorant AutoTracker

  <img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/aritra-codes/valorant-autotracker">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/t/aritra-codes/valorant-autotracker">

  `Valorant AutoTracker` uploads all your Valorant matches to YouTube and puts them on a spreadsheet in the click of a button! 🔘👆

  ![GIF of the app running](readme_files/running.gif)

  If this helps you, please ⭐ the repository & [follow me](https://github.com/aritra-codes) :D
</div>

---

# ⬇️ Installation

Currently, only [Windows](https://www.microsoft.com/en-gb/windows) is supported (as Valorant does not support other OSes).

**Video Tutorial (old version, so some steps are invalid):**
<br/>
<a href="https://youtu.be/i68pHqGllIs"><img src="readme_files/video_thumbnail.png" alt="Valorant AutoTracker logo" width="500"></a>

Main Installation:
- Click on the latest [release](https://github.com/aritra-codes/valorant-aut/releases) (on the right of the page, under the 'About' section).
  <br>
  <img src="readme_files/latest_release.png" alt="Latest release" width="400">
- Download 'Valorant_AutoTracker.msi'.
- Run the file (if there is a Windows Defender prompt, click 'More info' and 'Run anyway').
- Finish the installation wizard.
- Fill in the settings (check out the setup instructions below).
- You're ready to go!

---

# 🔄 Updating

Just follow the installation instructions above but you don't have fill in the settings again.

---

# ⚙️ Setup (only the complicated parts)
- API key:
  - Join the HenrikDev discord server (https://discord.gg/henrikdev-systems-704231681309278228).
  - Follow the instructions and verify yourself.
  - Go to the 'get-a-key' channel.
  - Click 'Generate' at the bottom of the message.
    <br>
    <img src="readme_files/generate_key.png" alt="Generate key button" width="400">
  - Select 'VALORANT'.
  - Select 'VALORANT (Basic Key)'.
  - In the Generate API Key form:
    - For Product Name, type 'Valorant AutoTracker'
    - For Product Description, type 'Uploads Valorant matches to YouTube and puts them on a spreadsheet.'
    - Click Submit.
  - Copy the key into the 'API Key' setting.
    <br>
    <img src="readme_files/key_generated.png" alt="Key generated message" width="400">
    <br>
    ![API Key setting](readme_files/api_key_setting.png)
  - Click 'Save API Key'.
- Auto-upload to YouTube:
  - Download [Firefox](https://www.mozilla.org/en-US/firefox/new).
  - Turn on the 'Auto-Upload Videos' setting.
    <br/>
    ![Auto-upload Videos setting](readme_files/auto_upload_videos.png)
  - Go to the URL 'about:profiles' and create a [new firefox profile](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles).
  - Copy the root directory path of that profile into the 'Firefox Profile Path' setting.
    <br/>
    ![Root directory of profile](readme_files/root_directory.png)
    <br/>
    ![Firefox Profile Path setting](readme_files/firefox_profile_path.png)
  - Click 'Save All' at the top of the settings window.
  - Go back to Firefox and click 'Launch profile in new browser'.
  - Go to [YouTube Studio](https://studio.youtube.com) and log in.
  - Choose the YouTube channel to which you like to upload your matches (**if there is a 'Don't ask again' option, select it**).
- Insert to Google Sheets:
  - Go to [Google Cloud](https://console.cloud.google.com) and log in.
  - Create a [new project](https://console.cloud.google.com/projectcreate) and name it anything (e.g. Valorant AutoTracker).
  - Go to [APIs and services](https://console.cloud.google.com/apis), then to [Enabled APIs and services](https://console.cloud.google.com/apis/dashboard) and click the 'ENABLE APIS AND SERVICES' button.
    <br/>
    !['ENABLE APIS AND SERVICES' button](readme_files/enable_apis.png)
  - Enable the [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) and [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com).
  - Go back to [APIs and services](https://console.cloud.google.com/apis), then to [Credentials](https://console.cloud.google.com/apis/credentials), click the 'CREATE CREDENTIALS' button and choose the 'Service account' option.
    <br/>
    ![Create 'Service account' option](readme_files/create_service_account.png)
  - Enter any Service account name (e.g. Valorant Spreadsheet Updater) and click the 'DONE' button.
  - Copy the service account's email, go to your Google Sheets spreadsheet and share it with this email as Editor.
    <br/>
    ![Service account email](readme_files/service_account_email.png)
    <br/>
    ![Sharing Google Sheets spreadsheet](readme_files/share_google_sheets.png)
  - Go back to the service account and click the 'Edit service account' button.
    <br/>
    !['Edit service account' button](readme_files/edit_service_account.png)
  - Go the 'KEYS' section, click 'ADD KEY', choose 'Create new key', choose JSON as the key type and click the 'CREATE' button. A .json file will be downloaded, save this to a location you prefer.
  - Turn on the 'Google Sheets' setting, type in your spreadsheet's name in the 'Spreadsheet Name' setting and choose the location of the .json file you downloaded in the 'Google Service Acc. Key' setting.
    <br/>
    !['Google Sheets' setting and more](readme_files/google_sheets_setting.png)
  - Click 'Save All' at the top of the settings window.

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

# ‼️ Disclaimer

This project is not associated with Riot Games. This application does not modify Valorant in any way, it only makes a request to the [unofficial-valorant-api](https://github.com/Henrik-3/unofficial-valorant-api) to get user and match data.

If you have any problems with this project, please send me an email at aritra8.codes@gmail.com.
