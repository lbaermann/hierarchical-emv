import math
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


def prepare_srt(lines: List[str], frame_duration: float):
    srt_content = []
    for i, line in enumerate(lines):
        start_time = i * frame_duration
        end_time = start_time + frame_duration

        # Convert times to hours, minutes, seconds, and milliseconds
        start_hours, start_remainder = divmod(start_time, 3600)
        start_minutes, start_seconds = divmod(start_remainder, 60)
        start_seconds_int = int(start_seconds)
        start_milliseconds = int((start_seconds - start_seconds_int) * 1000)

        end_hours, end_remainder = divmod(end_time, 3600)
        end_minutes, end_seconds = divmod(end_remainder, 60)
        end_seconds_int = int(end_seconds)
        end_milliseconds = int((end_seconds - end_seconds_int) * 1000)

        # Format time for SRT
        start_str = f"{int(start_hours):02}:{int(start_minutes):02}:{start_seconds_int:02},{start_milliseconds:03}"
        end_str = f"{int(end_hours):02}:{int(end_minutes):02}:{end_seconds_int:02},{end_milliseconds:03}"

        # Append the formatted subtitle entry to the list
        srt_content.append(f"{i + 1}\n{start_str} --> {end_str}\n{line.strip()}\n")
    return '\n\n'.join(srt_content)


def create_video_from_images(image_pattern, output_video, framerate=1):
    command = [
        'ffmpeg',
        '-framerate', str(framerate),
        '-i', image_pattern,
        '-r', str(framerate),
        '-pix_fmt', 'yuv420p',
        output_video
    ]

    subprocess.run(command, check=True)


def burn_subtitles(video_file, subtitles_file, output_video):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-vf', f"subtitles={subtitles_file}:force_style='FontSize=24,PrimaryColour=&HFFFFFF&'",
        '-c:a', 'copy',
        output_video
    ]

    subprocess.run(command, check=True)


def main():
    all_files_with_date = [
        (datetime.fromtimestamp(int(p.parent.parent.name) / 1e6), p)
        for p in Path('.').glob('*/*/0/image.rgb.png')
    ]
    all_files_with_date.sort()

    all_distances = [all_files_with_date[i + 1][0] - all_files_with_date[i][0] for i in
                     range(len(all_files_with_date) - 1)]
    avg_distance = sum(all_distances, start=timedelta()) / len(all_distances)
    fps = math.ceil(1 / avg_distance.total_seconds())  # ceil because FPS is usally lower than target value

    img_link_dir = Path('_tmp_images')
    subtitle_file = Path('_tmp_dates.srt')
    img_link_dir.mkdir(exist_ok=True)
    for i, (d, p) in enumerate(all_files_with_date):
        (img_link_dir / f'img{i:05}.png').symlink_to(p.resolve())

    srt = prepare_srt([
        d.strftime('%Y/%m/%d %H:%M:%S') for d, p in all_files_with_date
    ], frame_duration=1 / fps)
    subtitle_file.write_text(srt)

    create_video_from_images('_tmp_images/img%05d.png', 'episode.mp4', framerate=fps)
    burn_subtitles('episode.mp4', str(subtitle_file), 'episode-with-times.mp4')

    for p in img_link_dir.iterdir():
        p.unlink()
    img_link_dir.rmdir()
    subtitle_file.unlink()


if __name__ == '__main__':
    main()
