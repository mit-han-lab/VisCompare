# VisCompare

**VisCompare** is a WebUI application powered by [Streamlit](https://streamlit.io/) for side-by-side comparison of visual media from different folders.

<p align="center">
  <img src="assets/demo.gif" width="100%"/>
</p>

## Installation

Ensure you are using Python 3 to run this application. Then, install the required dependencies with the following command:
```shell
pip install streamlit streamlit-extras streamlit-sortables streamlit-file-browser
```

## Usage

### Local Deployment
To run the application locally, use the following command:
```shell
streamlit run main.py
```
You can execute this command in any working directory by adjusting the path to `main.py` as needed. Once the application is running, open a web browser and navigate to the provided URL and port. By default, the application should be accessible at http://localhost:8501.

### Remote Deployment
To deploy the application remotely, first follow the steps outlined in the local deployment section to start the application on your remote server. After that, establish an SSH tunnel to map the remote server's port to your local machine. Use the following command:
```shell
ssh -N -L $LOCAL_PORT:localhost:$REMOTE_PORT -o ServerAliveCountMax=3 -o ServerAliveInterval=15 -o ExitOnForwardFailure=yes -p $LOGIN_PORT $USERNAME@$SERVER_ADDRESS
```
Replace the placeholders (`$LOCAL_PORT`, `$REMOTE_PORT`, `$LOGIN_PORT`, `$USERNAME`, and `$SERVER_ADDRESS`) with the appropriate values for your setup. In most cases, if you are using a VS Code server, the setup for port forwarding will be handled automatically. Once the SSH tunnel is established, you can open your browser, navigate to the specified local port, and use the application.

## Features

### Folders and Display Names

To compare images or videos, enter the folder paths into the input fields. You can use either relative paths (from your current directory) or absolute paths. After clicking **Compare**, you’ll be navigated to the comparison page, where files with the same names (without suffix) across all specified folders will be displayed in a row. Only files common to all folders will be shown.

Each folder path can be assigned a display name corresponding to the **Display Name** field, which serves as the column header. If left blank, a default name like "Folder $i$" (where $i$ represents the row index) will be used. You can reorder the folders by clicking the **Reorder** button and dragging the folder items into your desired order.

To randomize the display order of media files, use the **Random Seed** option. If its value is set to -1, the media files are displayed in alphabetical order.

### Captions

To add captions, place your caption prompt files in the `captions` folder in YAML format. The YAML file should follow this structure:
```yaml
filename1: prompt1
filename2: prompt2
filename3: prompt3
```
Here, `filename` refers to the media file name without the file extension. For an example, refer to [example.yaml](captions/example.yaml). Once added, your caption file will appear as an option under **Path to the Caption File**.

### Save and Load
You can save the application's current state by clicking the **Save** button and entering a save path. The state is saved as a YAML file in the `configs` folder. To load a saved state, click the **Load** button and select the desired file path.
