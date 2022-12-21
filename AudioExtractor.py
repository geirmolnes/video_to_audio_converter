import logging
import os
import moviepy.editor as mp
import time


class AudioExtractor:
    def __init__(self, video_dir: str, audio_dir: str) -> None:
        self.video_dir = video_dir
        self.audio_dir = audio_dir
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create a file handler and set the log level to debug
        fh = logging.FileHandler("mylog.log")
        fh.setLevel(logging.DEBUG)

        # create a formatter and add it to the file handler
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)

        # add the file handler to the logger
        self.logger.addHandler(fh)

    def get_created_time(self, video_path: str) -> str:
        modified_time = os.path.getmtime(video_path)
        # convert to strftime
        return time.strftime("%d-%m-%Y %H:%M", time.localtime(modified_time))

    def get_file_name(self, video_path: str) -> str:
        video_id = video_path.split("#")[1].replace(".mp4", "")
        created_time = self.get_created_time(video_path)
        return f"{created_time} {video_id}.mp3"

    def is_converted(self, video_path: str) -> bool:
        file_name = self.get_file_name(video_path)
        audio_path = os.path.join(self.audio_dir, file_name)
        return os.path.exists(audio_path)

    def get_audio_from_video(self) -> None:
        video_files = os.listdir(self.video_dir)

        for video in video_files:
            video_path = os.path.join(self.video_dir, video)
            if self.is_converted(video_path):
                self.logger.info(f"{video} has already been converted, skipping...")
                continue

            file_name = self.get_file_name(video_path)
            clip = mp.VideoFileClip(video_path)
            clip.audio.write_audiofile(f"{self.audio_dir}/{file_name}")
            self.logger.info(f"Converted {video} to {file_name}")


if __name__ == "__main__":
    extractor = AudioExtractor("video_files", "audio_files")
    extractor.get_audio_from_video()
