import cv2
import plotly.graph_objects as go
import numpy as np


def find_bball(f, coordinates):
    ##lower = [r,g,b]
    ## upper = [r,g,b]

    ## Color values found
    #[255,135,101] HSV= [7,154,255]
    #[50,12,24]     [171,194,50]
    #[53,28,27]     [1,125,53]
    
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([0,100,40]) 
    upper_red = np.array([181,205,255]) 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(f,f, mask= mask) 
    #cv2.imshow("mask", res)
    # Read image
    
    # Convert to grayscale. 
    
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) 
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,     #param1=50,param2=30,minRad=10,maxRad=30
                param2 = 30, minRadius = 40, maxRadius = 80)   #minRadius = 90, maxRadius = 120
    
    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
        
        #print(detected_circles)
        #print(detected_circles[0,:])
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            if(len(detected_circles[0,:])==1):
                coordinates.append([a,b])
            # Draw the circumference of the circle. 
            cv2.circle(f, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(f, (a, b), 1, (0, 0, 255), 3)  
    return f
    
def videoCapture(path):
    # Create a VideoCapture object and read from input file 
    cap = cv2.VideoCapture(path) 
    coordinates=[]
    video=[]
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Check if camera opened successfully 
    #if (cap.isOpened()== False):  
    #print("Error opening video  file") 
   
    # Read until video is completed 
    while(cap.isOpened()): 
        
        # Capture frame-by-frame 
        ret, frame = cap.read() 
        if ret == True: 
        
            # Display the resulting frame 
            frame1 =  cv2.flip(frame,0) 
            #cv2.imshow('Frame', frame1)
            #img = cv2.imread(frame1)
            height, width, layers = frame1.shape
            size = (width,height)
            f=find_bball(frame1,coordinates)
            video.append(f)
            # Press Q on keyboard to  exit 
            if cv2.waitKey(35) & 0xFF == ord('q'): 
                break
        
        # Break the loop 
        else:  
            break
    #print(coordinates)
    
    # When everything done, release  
    # the video capture object 
    cap.release() 
    out = cv2.VideoWriter("assets/videos/temp.mp4",cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    for f in video:
        out.write(f)
    
    # Closes all the frames 
    cv2.destroyAllWindows() 
    return coordinates
    

def plotting(coordinates):

    x=[]
    y=[]
    frame=[]
    count=0


    for element in coordinates:
        x.append(element[0])
        y.append((element[1]*-1))
        frame.append(count)
        count+=1

    minimum=min(y)
    print(minimum)
    c=0
    for ele in y:
        y[c]=ele-minimum
        c+=1

    #print (y)
    # y2 - y1/x2-x1
    def slope(x1,y1,x2,y2):
        return (y1-y2)/(x1-x2)

    slope_list=[]
    for i in range(len(y)-1):
        x1=frame[i]
        x2=frame[i+1]
        y1=y[i]
        y2=y[i+1]
        slope_list.append(slope(x1,y1,x2,y2))
    peaks = []
    x_peaks = []
    left = 0
    curr = 1
    right =2 
    while (right<len(slope_list)):
        if(slope_list[left]>0 and ((slope_list[right])<0  or (slope_list[curr])<0) ):
            peaks.append(y[curr])
            x_peaks.append(frame[curr])

        left+=1
        curr+=1
        right+=1

    print(peaks)

    y_bad = []
    x_bad = []
    mean_peak = sum(peaks)/len(peaks)
    for idx, peak in enumerate(peaks):
        if(peak-mean_peak>10):
            print("bad",peak)
            y_bad.append(peak)
            x_bad.append(x_peaks[idx])

    print(slope_list)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=frame, y=y, name='ball position'))
    fig.add_trace(go.Scatter(x=x_bad, y=y_bad, mode="markers",name='outliers'))
    return fig


#points=videoCapture(r'assets/videos/bball14.mp4')
#plotting(points)
