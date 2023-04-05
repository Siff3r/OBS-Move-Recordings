import os
import shutil
import obspython as obs

# Enter folder where you would like recordings moved to
destination_folder = "C:/path/to/destination/folder"

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        move_recordings()

def move_recordings():
    try:
        recording_folder = obs.obs_frontend_get_recording_folder()
        files = os.listdir(recording_folder)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in files:
            if file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".flv"):
                src = os.path.join(recording_folder, file)
                dst = os.path.join(destination_folder, file)
                shutil.move(src, dst)

        obs.script_log(obs.LOG_INFO, "Moved recordings to: " + destination_folder)

    except Exception as e:
        obs.script_log(obs.LOG_ERROR, str(e))

def script_description():
    return "Move Recordings after Stream Stopped"

def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)

def script_unload():
    obs.obs_frontend_remove_event_callback(on_event)

