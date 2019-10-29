import glob
import os
import shutil
import librosa
import soundfile as sf


# Print types and count for each of the file formats in the server     
def get_file_formats(server_root_path):
    print("Getting all file formats...")
    all_file_formats = {}
    for root, dirs, files in os.walk(server_root_path):
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if (file_extension in all_file_formats):
                all_file_formats[file_extension] += 1
            else:
                all_file_formats[file_extension] = 1
            
    print('File formats: \n', all_file_formats)
    return all_file_formats

# Make local copy of folder structure   
def make_directory_copy(server_root_path, local_root_path):
    print("Making local copy of folder structure...")
    for root, dirs, files in os.walk(server_root_path):
        for directory in dirs:
            l_root = root.replace(server_root_path+'/', '') # Remove the server_root_path from local copy
            l_root = l_root.replace(server_root_path, '') # For first children of server_root_path
            local_dir_path = os.path.join(local_root_path, l_root, directory)
            if not os.path.exists(local_dir_path):
                os.makedirs(local_dir_path)

# Make local copy of cover art
def make_cover_art_copy(server_root_path, local_root_path, image_formats):
    print("Making local copy of cover art...")
    for root, dirs, files in os.walk(server_root_path):
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if file_extension in image_formats:
                l_root = root.replace(server_root_path+'/', '') # Remove the server_root_path from local copy
                l_root = l_root.replace(server_root_path, '') # For first children of server_root_path
                local_img_path = os.path.join(local_root_path, l_root, name)

                # Copy image
                if not os.path.exists(local_img_path):
                    img = "img"
                    shutil.copy(filedir, local_img_path)

# Make local copy of clips extracted from the original audio files
# Can take parameters for format of clip extraction (eg. location='middle', length='15')
# Any additional way of clip extraction should be defined by a set of parameters and handled in extract_single_clip
# eg. if implementing chorus extraction with 10 seconds, pass parameters (location='chorus', length='10')
def extract_all_clips(server_root_path, local_root_path, audio_formats, **kwargs):
    print("Making local copy of audio clips...")
    for root, dirs, files in os.walk(server_root_path):
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if file_extension in audio_formats:
                l_root = root.replace(server_root_path+'/', '') # Remove the server_root_path from local copy
                l_root = l_root.replace(server_root_path, '') # For first children of server_root_path
                local_aud_path = os.path.join(local_root_path, l_root, name)

                # Extract clip using the preferred parameters
                clip = "clip"
                extract_single_clip(filedir, local_aud_path, **kwargs)

# Extract a single clip using the specified method (middle, random, chorus, etc.) in '.wav' format
def extract_single_clip(original_audio_path, local_audio_path, **kwargs):
    
    # Append the extraction parameters to the filename to avoid overwriting
    filename, file_extension = os.path.splitext(local_audio_path)
    final_audio_path = filename
    for key, value in kwargs.items():
        final_audio_path += ("_" + str(value))
    final_audio_path += '.wav'

    if not os.path.exists(final_audio_path):

        # Case where clips extracted are from the middle, and given a length
        if kwargs.get('location') == 'middle':
            clip_length = kwargs.get('length')
            if clip_length == None:
                raise Exception('Provide a length for the extracted clips')
            full_duration = librosa.get_duration(filename=original_audio_path)
            if full_duration < clip_length:
                with open('clip_extraction_error_log.txt', 'a') as error_log_f:
                    error_log_f.write("Clip length error: " + '\n' + final_audio_path + '\n')
                return
            try:
                y, sr = librosa.load(original_audio_path, offset = (full_duration/2) - (clip_length/2), duration = clip_length, sr=44100)
            except:
                with open('clip_extraction_error_log.txt', 'a') as error_log_f:
                    error_log_f.write("Reading file error: " + '\n' + final_audio_path + '\n')
                return
            try:
                sf.write(final_audio_path, y, sr, 'PCM_16')
            except:
                with open('clip_extraction_error_log.txt', 'a') as error_log_f:
                    error_log_f.write("Writing file error: " + '\n' + final_audio_path + '\n')
                return
            print(final_audio_path)

        # Implement here other cases such as chorus extraction
        
# Delete local audio files
def cleanup_audio(local_audio_path, audio_formats):
    print("Cleaning local copy of audio clips...")
    for root, dirs, files in os.walk(local_audio_path):
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if file_extension in audio_formats:
                os.remove(filedir)
                print(filedir)

# Formats to consider for making a local copy (music and cover art)
aud_formats = set(['.wav', '.m4a', '.WAV', '.aiff', '.aif'])
img_formats = set(['.tif', '.jpg', '.JPG', '.png'])

if __name__ == "__main__":
    
    # Need to be absolute paths (start with '/')
    # Assumes Mac connected to the CDS-Carlos server (might need to modify server_path for Windows)
    server_path = "/Volumes/CDS-Carlos"
    local_path = "/Users/masc/Documents/Oscar/MaSC-Music-Visualization-master"

    # all_file_formats = get_file_formats(server_path)
    # make_directory_copy(server_path, local_path)
    # make_cover_art_copy(server_path, local_path, img_formats)
    extract_all_clips(server_path, local_path, aud_formats, location='middle', length=15)

