from flask import Flask, render_template, Response,jsonify
import numpy as np
import cv2
import time
import matplotlib.pylab as plt
from scipy import fftpack
#import io
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure

app = Flask(__name__)

cap = cv2.VideoCapture(0) 


def gen_frames():
    t1 = time.time()
    t = 0
    video = []
    cnt = 0
    while(t<10):
        t2 = time.time()
        t = t2-t1
        if t <10:
            a,b = cap.read() 
            if not a:
                cap.release()
                break
            else:
                
                gray = np.array(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY))
                cv2.waitKey(20)
                video.append(np.sum(gray))
                cnt+=1
    cap.release() 
    video2 = np.array(video)
    video2 = video2/np.mean(video2)
    
    x = video2
    f_s = 30
    X = fftpack.fft(x)
    freqs = fftpack.fftfreq(len(x)) * f_s
    s = np.sort(np.abs(X))
    i = np.where(np.isclose(np.abs(X), s[-2]))
    j = np.where(np.isclose(np.abs(X), s[-3]))
    k = np.where(np.isclose(np.abs(X), s[-4]))
    val = round(freqs[i][0]*60,2)
    # print("pulse = ",val,"bpm")
    # print("secondary peak = ",round(freqs[j][0]*60,2),"per minutes")
    # print("tertiary peak = ",round(freqs[k][0]*60,2),"per minutes")
    
    return val

    

@app.route('/video_feed')
def video_feed():
    
    return Response(gen_frames())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    val = gen_frames()
    print("pulse = ",val,"bpm")
    return render_template('result.html',val=val)


if __name__ == '__main__':
    app.run(threaded=True)
