import struct
import wave
import os

sample_rate = 44100
duration = 272  # 4分32秒
num_samples = int(duration * sample_rate)

print(f"Generating {duration} seconds of audio...")

# 使用简单的正弦波，加快生成速度
values = []
for i in range(num_samples):
    t = i / sample_rate
    # 简单的正弦波混合
    sample = 0.4 * (
        int(32767 * 0.6 * (1 if (int(t * 4) % 2) == 0 else -1)) +  # 方波基础
        int(32767 * 0.3 * ((t * 440 * 2 % 256) - 128) / 128)  # 类钢琴音色
    ) / 2
    
    # 淡入淡出
    if t < 1:
        sample = sample * t
    elif t > duration - 2:
        sample = sample * (duration - t) / 2
    
    values.append(int(max(-32768, min(32767, sample))))

print("Writing WAV file...")
wav_path = "public/music/your-hand-in-mine.wav"
with wave.open(wav_path, 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    for v in values:
        wav.writeframes(struct.pack('<h', v))

file_size = os.path.getsize(wav_path)
minutes = int(duration / 60)
seconds = duration % 60
print(f"✓ Created: {minutes}:{seconds:02d} audio")
print(f"  Size: {file_size / 1024 / 1024:.2f} MB")
