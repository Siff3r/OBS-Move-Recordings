import obspython as obs
from shutil import move
import os

# Global variables for prefixes and folders
prefix_a = ''
folder_a = ''
prefix_b = ''
folder_b = ''

def script_description():
    return 'This plugin moves the recorded file to specified folders based on file name prefixes.'

def script_load(settings):
    """Hook stop recording signal on plugin load."""
    signal_handler = obs.obs_output_get_signal_handler(obs.obs_frontend_get_recording_output())
    obs.signal_handler_connect(signal_handler, 'stop', signal_handler_function)

def script_update(settings):
    """Update global variables when settings change."""
    global prefix_a, folder_a, prefix_b, folder_b
    prefix_a = obs.obs_data_get_string(settings, 'prefix_a')
    folder_a = obs.obs_data_get_string(settings, 'folder_a')
    prefix_b = obs.obs_data_get_string(settings, 'prefix_b')
    folder_b = obs.obs_data_get_string(settings, 'folder_b')

def script_properties():
    """Create properties for user input."""
    props = obs.obs_properties_create()
    
    obs.obs_properties_add_text(props, 'prefix_a', 'Prefix A', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_path(props, 'folder_a', 'Folder A', obs.OBS_PATH_DIRECTORY, '', '')
    
    obs.obs_properties_add_text(props, 'prefix_b', 'Prefix B', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_path(props, 'folder_b', 'Folder B', obs.OBS_PATH_DIRECTORY, '', '')
    
    return props

def signal_handler_function(calldata):
    """Handle the recording stop signal and move the file accordingly."""
    global prefix_a, folder_a, prefix_b, folder_b
    try:
        last_recording = obs.obs_frontend_get_last_recording()
        file_name = os.path.basename(last_recording)
        
        if file_name.lower().startswith(prefix_a):
            move(last_recording, os.path.join(folder_a, file_name))
        elif file_name.lower().startswith(prefix_b):
            move(last_recording, os.path.join(folder_b, file_name))
        else:
            pass  # Do not move the file
    except Exception as e:
        obs.script_log(obs.LOG_WARNING, 'Error moving file: ' + str(e))
