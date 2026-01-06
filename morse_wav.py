import wave
import struct
import math

# モールス信号の定義
MORSE_CODE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',
    'F': '..-.',   'G': '--.',    'H': '....',   'I': '..',     'J': '.---',
    'K': '-.-',    'L': '.-..',   'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',    'S': '...',    'T': '-',
    'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',   'Y': '-.--',
    'Z': '--..',   '1': '.----',  '2': '..---',  '3': '...--',  '4': '....-',
    '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',  '9': '----.',
    '0': '-----',  ' ': '/'
}

def generate_morse_wav(text, filename="output.wav", wpm=20, frequency=800.0):
    # パラメータ設定
    sample_rate = 44100.0  # 44.1kHz
    amplitude = 16000      # 音量 (16-bit PCM の範囲内)
    
    # 時間計算 (PARIS規格: 1ユニット = 1.2 / WPM 秒)
    dot_duration = 1.2 / wpm 
    
    # 正弦波の1サンプルあたりの値を計算する数式
    # s(n) = A * sin(2 * pi * f * n / R)
    
    audio_data = []

    def add_signal(duration, is_on):
        num_samples = int(duration * sample_rate)
        for n in range(num_samples):
            if is_on:
                # 正弦波の生成
                value = int(amplitude * math.sin(2 * math.pi * frequency * n / sample_rate))
                audio_data.append(struct.pack('<h', value))
            else:
                audio_data.append(struct.pack('<h', 0))

    # テキストをパース
    text = text.upper()
    for char in text:
        if char in MORSE_CODE_DICT:
            code = MORSE_CODE_DICT[char]
            if code == '/':  # 単語間のスペース
                add_signal(dot_duration * 7, False)
            else:
                for symbol in code:
                    if symbol == '.':
                        add_signal(dot_duration, True)
                    elif symbol == '-':
                        add_signal(dot_duration * 3, True)
                    
                    # 記号間の隙間 (1ユニット)
                    add_signal(dot_duration, False)
                
                # 文字間の隙間 (3ユニット、ただし記号間で既に1消費してるので+2)
                add_signal(dot_duration * 2, False)

    # WAVファイル書き出し
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)      # モノラル
        wav_file.setsampwidth(2)      # 16-bit
        wav_file.setframerate(int(sample_rate))
        wav_file.writeframes(b''.join(audio_data))

    print(f"Saved: {filename}")

# 使用例
# message = "BINARY WHISPER STOP"
message = "MIX CD QUEST JET KILLER FOG ZONE"
generate_morse_wav(message, "morse_signal2.wav", wpm=25, frequency=800)