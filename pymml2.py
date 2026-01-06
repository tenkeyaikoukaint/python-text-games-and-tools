import math
import wave
import struct

# --- 1. 設定 ---
SAMPLE_RATE = 44100

def create_base_tone():
    """
    標準機能だけで「一音」の波形データを計算する
    """
    duration = 1.0
    freq = 440.0
    num_samples = int(SAMPLE_RATE * duration)
    
    raw_data = []
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        
        # 倍音合成 (sin波の足し算)
        # numpyがないので math.sin を地道に回す
        val = math.sin(2 * math.pi * freq * t) * 1.0 + \
              math.sin(2 * math.pi * freq * 2 * t) * 0.5 + \
              math.sin(2 * math.pi * freq * 3 * t) * 0.2
        
        # 減衰エンベロープ (指数関数的減衰)
        envelope = math.exp(-3 * t)
        val = val * envelope
        
        raw_data.append(val)
        
    # 正規化（最大音量を1.0に合わせる）
    max_val = max(abs(v) for v in raw_data)
    return [v / max_val for v in raw_data]

# --- 2. ピッチ変換（間引き処理） ---
def change_pitch(data, semitones):
    if semitones == 0:
        return data[:]
    
    # 再生速度の倍率
    rate = 2 ** (semitones / 12.0)
    
    new_data = []
    # 浮動小数点のインデックス
    current_idx = 0.0
    
    while current_idx < len(data):
        # 最近傍法（Nearest Neighbor）
        # 最も近いインデックスのデータを拾う
        idx = int(current_idx)
        if idx < len(data):
            new_data.append(data[idx])
        current_idx += rate
        
    return new_data

# --- 3. 音階データの作成 ---
print("音階データを計算中（CPU演算）...")
base_tone = create_base_tone()
note_bank = {}
scale_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
base_note_index = 9 # A

for octave in range(3, 6):
    for i, name in enumerate(scale_names):
        dist = (octave - 4) * 12 + (i - base_note_index)
        key = f"{name}{octave}"
        note_bank[key] = change_pitch(base_tone, dist)

note_bank["R"] = [0.0] * int(SAMPLE_RATE * 0.2) # 休符

# --- 4. 演奏コンパイラ ---
def compile_mml(mml_string, tempo=120):
    beat_samples = int(SAMPLE_RATE * (60 / tempo))
    final_output = []
    
    notes = mml_string.split()
    
    for note in notes:
        if ":" in note:
            name, length_ratio = note.split(":")
            length_ratio = float(length_ratio)
        else:
            name = note
            length_ratio = 1.0
            
        if name in note_bank:
            sample = note_bank[name]
            target_len = int(beat_samples * length_ratio)
            
            # リストのスライスで長さを調整
            if len(sample) > target_len:
                final_output.extend(sample[:target_len])
            else:
                final_output.extend(sample)
                # 足りない分を0埋め
                final_output.extend([0.0] * (target_len - len(sample)))
        else:
            print(f"不明な音符: {name}")

    return final_output

# --- 5. バッハ「ゴルトベルク変奏曲」アリア ---
mml = """
G4 G5 F#5 G5 E5 E4
A4 B4 A4 G4 F#4 G4
C5 B4 C5 D5 B4 G4
A4 G4 F#4 G4 A4 D4
G4 G5 F#5 G5 E5 E4
A4 B4 A4 G4 F#4 G4
C5 B4 C5 D5 B4 G4
A4 G4 F#4 G4 A4 D4
G4 F#4 G4 A4 B4 A4
G4 F#4 G4 A4 B4 C5
"""

print("MMLを波形に変換中...")
audio_data = compile_mml(mml, tempo=80)

# --- 6. WAV書き出し（バイナリパック） ---
output_filename = "goldberg_pure.wav"
print(f"書き込み中: {output_filename}")

with wave.open(output_filename, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2) # 16bit
    wf.setframerate(SAMPLE_RATE)
    
    # 浮動小数点を16bit整数(-32767 ~ 32767)に変換してバイナリ化
    # struct.pack('<h') はリトルエンディアンのshort型(2byte)にする命令
    binary_data = bytearray()
    for v in audio_data:
        # クリップ防止
        v = max(min(v, 1.0), -1.0)
        int_val = int(v * 32767)
        binary_data.extend(struct.pack('<h', int_val))
        
    wf.writeframes(binary_data)

print("完了。再生してください。")