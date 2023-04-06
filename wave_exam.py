import wave


obj = wave.open("output.wav", "rb")

# 파라미터 확인
print("Number of channels", obj.getnchannels())
print("sample width", obj.getsampwidth())
# 프레임 속도
print("frame rate", obj.getframerate())
# 프레임 수
print("Number of frames", obj.getnframes())
# 모든 매개변수
print("parameters", obj.getparams())
