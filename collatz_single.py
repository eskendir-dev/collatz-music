import numpy as np
from scipy.io.wavfile import write

# ---------- Параметры ----------
SAMPLE_RATE = 44100   # качество звука (Гц)
AMPLITUDE = 0.7       # мягкая громкость
BASE_MIDI = 60        # базовая нота (До)
DUR_SHORT = 0.18      # длительность чётных чисел
DUR_LONG  = 0.35      # длительность нечётных чисел
GAP = 0.05            # пауза между нотами

# ---------- Цепочка Коллатца ----------
def collatz_sequence(n):
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3*n + 1
        seq.append(n)
    return seq

# ---------- Преобразование MIDI -> частота ----------
def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12.0))

# ---------- Генерация мягкой ноты ----------
def make_tone(freq, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE*duration), False)

    # Основная мягкая синусоида
    tone = np.sin(freq * t * 2 * np.pi)

    # Добавим лёгкие обертоны (очень тихие, для теплоты)
    tone += 0.2 * np.sin(2 * freq * t * 2 * np.pi)   # вторая гармоника
    tone += 0.1 * np.sin(3 * freq * t * 2 * np.pi)   # третья гармоника

    # Плавный fade-in / fade-out (чтобы звук не был резким)
    fade_len = int(0.05 * len(t))  # 5% от длины ноты
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    envelope = np.ones(len(t))
    envelope[:fade_len] = fade_in
    envelope[-fade_len:] = fade_out
    tone = tone * envelope

    # Нормализация и мягкая громкость
    tone = tone / np.max(np.abs(tone))
    return tone * AMPLITUDE

# ---------- Ввод числа ----------
start_number = int(input("Введите число для музыки Коллатца: "))
sequence = collatz_sequence(start_number)

# ---------- Создание аудио ----------
audio = np.array([], dtype=np.float32)

for n in sequence:
    midi = BASE_MIDI + (n % 7)
    freq = midi_to_freq(midi)
    dur = DUR_SHORT if n % 2 == 0 else DUR_LONG
    tone = make_tone(freq, dur)
    audio = np.concatenate([audio, tone, np.zeros(int(GAP*SAMPLE_RATE))])

# ---------- Нормализация и сохранение ----------
audio_int16 = np.int16(audio/np.max(np.abs(audio)) * 32767)
write("collatz_soft.wav", SAMPLE_RATE, audio_int16)

print("Файл collatz_soft.wav создан! Он будет звучать мягко и уютно 🎶")

