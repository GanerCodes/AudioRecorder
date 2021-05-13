import pyaudio, audioop, wave, threading, os

DELAY = 0.275


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

WAVE_OUTPUT_FILENAME = str(len(os.listdir()))+".wav"



p = pyaudio.PyAudio()
stream = p.open(input_device_index = 1, format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)


frames = []
frameIndex = 0
can = 15
cont = True

def inp():
	global frameIndex, frames, cont
	while 1:
		print(inp := input("Enter a command (<Enter>, b, e): "))
		inp = inp.strip().lower()
		if inp == '':
			frameIndex += 1
			print("Going to next index, index:", frameIndex)
		elif inp == 'b':
			# frameIndex -= 1
			if len(frames) > 0:
				frames.pop()
				print("Retrying, index:", frameIndex)
			else:
				print("Can't go back any farther.")
		elif inp == 'e':
			print("Ending.")
			cont = False
			break
		else:
			print("Not a valid command.")
threading.Thread(target = inp).start()

print("Starting recording.")

while cont:
	data = stream.read(CHUNK)
	vol = audioop.rms(data, 2) / RATE
	if vol < 0.003:
		can -= 1
	else:
		can = DELAY * RATE / CHUNK
	if can > 0:
		while (theIndex := frameIndex) + 1 > len(frames):
			frames.append([])
		frames[theIndex].append(data)

print("Finished Recording.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
for i in frames:
	wf.writeframes(b''.join(i))
wf.close()