import time
from threading import Thread

import pyaudio
import wave
import keyboard
import uuid
import requests
import os

FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate (samples per second)
CHUNK = 1024  # Number of frames per buffer
RECORD_SECONDS = 5  # Duration of recording

SERVER_URL = 'http://10.24.105.160:8585'
TEST_URL = 'http://localhost:8585'


class VoiceRecorder:
    def __init__(self, default_path, on_start_action=None, on_stop_action=None):
        """

        :param default_path: default_path for recording files
        :param on_start_action: on record start action , method to run when the record starts
        :param on_stop_action: on record end action , method to run when the record ends
        """
        # Set the parameters for audio recording
        # Initialize PyAudio
        self.default_path = default_path
        self.audio = None
        self._is_recording = False
        self.stream = None
        self.recording_thread: Thread = None
        self._current_frames = []
        self.on_start_action = on_start_action
        self.on_stop_action = on_stop_action
        self.last_audio_f_path = None
        self.record_started = False
        self.record_ended = False
        self.rec_f_name = None

    def _record_voice_stream(self):
        print("Recording...")
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        if self.on_start_action is not None:
            self.on_start_action()
        while self.record_started and not self.record_ended:
            data = self.stream.read(CHUNK)
            self._current_frames.append(data)

    def start_record(self, async_record=True):
        self.record_ended = False
        self.record_started = True
        self._current_frames = []

        if async_record:
            self.recording_thread = Thread(name="voice_recorder", daemon=True, target=self._record_voice_stream)
            self.recording_thread.start()
        else:
            self._record_voice_stream()

    def stop_recording_stream(self):
        self.record_ended = True
        self.recording_thread = None
        self.record_started = False
        f_name = str(uuid.uuid4()) + ".wav" if self.rec_f_name is None else f"{self.rec_f_name}.wav"
        file_path = f"{self.default_path}\\{f_name}"

        self.rec_f_name = None

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Recording finished.")
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self._current_frames))

        print(f"Audio saved as {file_path}")
        self.last_audio_f_path = file_path
        time.sleep(0.3)
        if self.on_start_action is not None:
            self.on_start_action()

    def space_press_action(self, e):
        if not self.record_started:
            self.start_record()

    def space_release_action(self, e):
        if self.record_started and not self.record_ended:
            self.stop_recording_stream()
            keyboard.unhook_all()

    def start_record_by_keyboard(self, fname=None, async_record=False):
        self.rec_f_name = fname
        keyboard.on_press_key("space", self.space_press_action)
        keyboard.on_release_key("space", self.space_release_action)

        while not async_record and not self.record_started:
            time.sleep(0.5)
        time.sleep(0.1)
        while not async_record and not self.record_ended:
            time.sleep(0.5)


def send_voice_abbreviation(file_path, url=None):
    if url is None:
        url = SERVER_URL
    with open(file_path, 'rb') as f:
        files = {'voice_file': (os.path.basename(file_path), f)}
        response = requests.post(url + '/upload_abbreviations', files=files)

    return response.json


def load_voice_abbreviations(abbreviation_names: list, url=None):
    if url is None:
        url = SERVER_URL
    json_request = {"abbreviations": abbreviation_names}

    response = requests.post(url + '/load_abbreviations', json=json_request)
    if response.json() is not None:
        print(str(response.status_code) + "\n" + response.json()['status'])
    else:
        print("error loading abbreviations")


def get_text_from_voice(file_path, url=None, keep_record_file=False, record_abbreviation=None):
    if url is None:
        url = SERVER_URL
    with open(file_path, 'rb') as f:
        files = {'voice_file': (os.path.basename(file_path), f)}

        if record_abbreviation is not None:
            data = {
                'abbreviation': record_abbreviation
            }

            response = requests.post(url + '/voice_recognition', files=files, data=data)
        else:
            response = requests.post(url + '/voice_recognition', files=files)

    if not keep_record_file:
        os.remove(file_path)
    if response.status_code == 200:
        text = response.json()['text']
        return text
    else:
        print("Error:", response.text)
    return None


def is_voice_server_connected(url=None):
    if url is None:
        url = SERVER_URL
    response = requests.post(url + '/test')
    return response.status_code == 200 and response.text == 'test-ok'
