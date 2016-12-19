from flask import Flask, render_template, Response
from StreamSource import streamsource

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(source):
    while(True):
        frame=source.get_video()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(streamsource()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    try:
        app.run(host='localhost',debug=True)
    except:
        print "shoutdown"
        pass
