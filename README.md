# AIServices

## installation

`pip install git+https://github.com/Andalusia-Data-Science-Team/AHBS_AIServices`

## voice recognition

### voice recorder

1. create object from voice recorder , specify the recording folder

- VoiceRecorder parameters
    - *default_path*: default_path for recording files
    - *on_start_action*: on record start action , method to run when the record starts
    - *on record end action*  method to run when the record ends

```python
from AHBS_AIServices import voice_recogntion

voice_recorder = voice_recogntion.VoiceRecorder("./recordings")
```

2. you can use the voice recorder async or sync by two methods , either you control the start and end recording by space (press to talk) or you control it by start record and end record
 
- record by space , you can specify the record name or leave it none to be generated:
- you can get the recorded file path by `voice_recorder.last_audio_f_pat`
```python
voice_recorder.start_record_by_keyboard()
f_path=voice_recorder.last_audio_f_path
```

### voice recognition
#### simple task without abbreviation
```python
from AHBS_AIServices import voice_recogntion
voice_recorder=voice_recogntion.VoiceRecorder("./recordings")
voice_recorder.start_record_by_keyboard()
f_path=voice_recorder.last_audio_f_path
voice_recogntion.get_text(f_path)
```

### task with abbreviation
- record your voice abbreviations , upload them to server , load them to server memory , use them

```python
from AHBS_AIServices import voice_recogntion
voice_recorder=voice_recogntion.VoiceRecorder("./recordings")
voice_recorder.start_record_by_keyboard()

# first abbreviation
# load abbreviation medication
voice_recorder.start_record_by_keyboard("medication")

# upload to server
voice_recogntion.send_voice_abbreviation("./recordings/medication.wav")


voice_recorder.start_record_by_keyboard("labs")
# upload to server
voice_recogntion.send_voice_abbreviation("./recordings/labs.wav")
# or you can use path of last recorded file
voice_recogntion.send_voice_abbreviation(f_path=voice_recogntion.last_audio_f_path)


# load all abbreviations to memory
voice_recogntion.load_voice_abbreviations(['medication','labs'])

# use abbreviation by sending the abbreviation name
voice_recorder.start_record_by_keyboard()
f_path=voice_recorder.last_audio_f_path
# sending voice and abbreviation name to be used in the voice recognition
text=voice_recogntion.get_text(f_path,record_abbreviation='medication')
```