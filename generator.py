import torch
import numpy as np
import librosa
import cv2
import os
from model import MusicVideoGeneratorModel

class MusicVideoGenerator:
    def __init__(self, model_path='music_video_generator.pth', audio_length=100, video_frame_size=1024):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.audio_length = audio_length
        self.video_frame_size = video_frame_size
        self.model = MusicVideoGeneratorModel(audio_length, video_frame_size).to(self.device)
        
        # Load model if exists
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
        else:
            print(f"Warning: Model file {model_path} not found. Using untrained model.")
    
    def extract_audio_features(self, audio_path, sr=22050, hop_length=512):
        """Extract audio features from the audio file"""
        y, sr = librosa.load(audio_path, sr=sr)
        
        # Extract features (mel spectrogram)
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Normalize
        mel_spec_db = (mel_spec_db - mel_spec_db.min()) / (mel_spec_db.max() - mel_spec_db.min())
        
        # Reshape for model input
        segments = []
        for i in range(0, mel_spec_db.shape[1] - self.audio_length, self.audio_length // 2):
            segment = mel_spec_db[:, i:i+self.audio_length]
            if segment.shape[1] == self.audio_length:
                segments.append(segment)
        
        return segments, sr, hop_length, len(y)
    
    def generate_video_frames(self, audio_segments, frame_width=640, frame_height=480):
        """Generate video frames from audio segments"""
        frames = []
        
        for segment in audio_segments:
            # Reshape segment for model input
            segment_tensor = torch.FloatTensor(segment).unsqueeze(0).to(self.device)
            
            # Generate frame data
            with torch.no_grad():
                frame_data = self.model(segment_tensor).cpu().numpy()[0]
            
            # Reshape frame data to image dimensions
            frame_data = frame_data.reshape(frame_height, frame_width, 3)
            
            # Normalize to 0-255 range for image
            frame_data = (frame_data * 255).astype(np.uint8)
            
            frames.append(frame_data)
        
        return frames
    
    def create_video(self, frames, output_path, fps=30):
        """Create video from frames"""
        if not frames:
            raise ValueError("No frames to create video")
        
        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        for frame in frames:
            video_writer.write(frame)
        
        video_writer.release()
    
    def generate(self, audio_path, output_path):
        """Generate a music video from an audio file"""
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Extract audio features
        audio_segments, sr, hop_length, audio_length = self.extract_audio_features(audio_path)
        
        # Generate video frames
        frames = self.generate_video_frames(audio_segments)
        
        # Calculate appropriate FPS based on audio length and number of frames
        audio_duration = audio_length / sr
        fps = len(frames) / audio_duration
        
        # Create video
        self.create_video(frames, output_path, fps)
        
        return output_path