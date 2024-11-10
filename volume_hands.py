import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import objc
import osascript



vCam, hCam = 640, 480

# Initialize the pycaw module for Windows
# volume = AudioUtilities.GetMasterVolume()

# Function to set system volume on macOS
def set_system_volume(volume):
    objc.loadBundle('CoreAudio', bundle_path='/System/Library/Frameworks/CoreAudio.framework', module_globals=globals())
    device = CoreAudio.kAudioObjectSystemObject
    m = CoreAudio.AudioObjectPropertyAddress(CoreAudio.kAudioHardwareServiceDeviceProperty_VirtualMasterVolume, CoreAudio.kAudioObjectPropertyScopeOutput, 0)
    CoreAudio.AudioObjectSetPropertyData(device, m, 0, None, volume, CoreAudio.kAudioObjectPropertyElementMaster)

cap = cv2.VideoCapture(0)  # Open default camera
detector = htm.FindHands()  # Initialize hand detector
minVol = -65  # Minimum volume
maxVol = 0  # Maximum volume
#set_system_volume(100)

while True:
    success, img = cap.read()
    #img = detector.FindHands(img)
    lmList = detector.getPosition(img, range(21), draw=False)
    if len(lmList) != 0:
        if detector.index_finger_up(img):
            osascript.osascript("set volume output volume 100")
        if detector.little_finger_up(img):
            osascript.osascript("set volume output volume 50")
        #x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip coordinates
        #x2, y2 = lmList[8][1], lmList[8][2]  # Index finger tip coordinates
        #cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Center coordinates between thumb and index finger

        #length = math.hypot(x2 - x1, y2 - y1)
        #vol = np.interp(length, [50, 300], [minVol, maxVol])
        # volBar = np.interp(length, [50, 300], [400, 150])
        # volPer = np.interp(length, [50, 300], [0, 100])
        #print(int(length), vol)
        
        # Adjust system volume
        #set_system_volume(vol)

        #if length < 50:
            #cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
