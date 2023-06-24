import requests
import dotenv
import os
from constants import SESSION_HEADERS
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import torch
import soundfile as sf
from datasets import load_dataset


class Deepfake:
    """
    DeepFake class helps to generate deepfake video . 
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = SESSION_HEADERS
        self.response = None
        self.id = 0
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embeddings = torch.tensor(self.embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def generate_tts(self,prompt,ini):
        """
        generate_tts function help to generate audio in continuos format Beacuse pretrained models can only generate 
        audio till 600 tokens .

        """
        inputs = self.processor(text=prompt, return_tensors="pt")
        speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder)

        return np.concatenate((ini , speech.numpy()))

    def generate_video(self,prompt : str):
        """
        generate_video function queries heygen api to generate deepfake video.
        """
        data = {
            "background": "#ffffff",
            "clips": [
                {
                "avatar_id": "Daisy-inskirt-20220818",
                "avatar_style": "normal",
                "input_text": prompt,
                "offset": {
                    "x": 0,
                    "y": 0
                },
                "scale": 1,
                "voice_id": "1bd001e7e50f421d891986aad5158bc8"
                }
            ],
            "ratio": "16:9",
            "test": True,
            "version": "v1alpha"
        }

        self.response = self.session.post('https://api.heygen.com/v1/video.generate',data = data).json()
    
    def tts(self,prompt):
        """
        tts means text to speech function which genrates and saves audio file .
        """
        inputs = self.processor(text=prompt[:50], return_tensors="pt")
        speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder).numpy()

        for i in range(100,300,50):
            speech = self.generate_tts(prompt[i-50:i],speech)

        sf.write(f"speech{self.id}.wav", speech, samplerate=16000)
        
        return f"speech{self.id}.wav"

    def generate_deepfake(self,prompt):
        """
        The main deepfake video generator function which combines video from heygen with audio from 
        pretrained models .

        outputs the path of file store on disk .

        """
        self.id += 1
        video = requests.get(self.response['data']['video_url'])
        f = open(f"Video{self.id}.mp4","wb")
        f.write(video.content)
        f.close()

        video_clip = VideoFileClip(f"Video{self.id}.mp4")
        audio_clip = AudioFileClip(self.tts(prompt))
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(f"Final{self.id}.mp4")
        
        return f"Video{self.id}.mp4"