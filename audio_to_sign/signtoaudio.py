from pydub import AudioSegment
from pydub.playback import play

def play_audio(file_path):
    sound = AudioSegment.from_file(file_path)
    play(sound)

# Replace 'your_audio_file.mp3' with the path to your audio file

def sign_language_to_audio(cv2):
    # Open the webcam (usually the default camera is 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Create a window with the name "Webcam Feed"
    cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)

    while cv2.getWindowProperty("Webcam Feed", cv2.WND_PROP_VISIBLE) > 0:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display the frame in the "Webcam Feed" window
        cv2.imshow("Webcam Feed", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:  # 'q' key or Esc key
            break

    # Release the webcam and close the window when done
    cap.release()
    cv2.destroyAllWindows()

    #play_audio('audio.m4a')