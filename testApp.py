from tkinter import *
import datetime
import time
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
import PyPDF2
import tkVideoPlayer as video
main=  Tk()


#Home page
main.state('zoomed')
page1 = Frame(main, background='white')
page1.place(anchor='nw', relwidth=1, relheight=1)
currentPage=0
def openVideoPage():
    global currentPage
    page3.tkraise()
    currentPage=2

def openPDFPage():
    global currentPage
    page2.tkraise()
    currentPage=1
title1 = Label(page1, text="",  font=('ariel', 25))
title1.place(anchor='center', relx=0.5, rely=0.3)
selectVideo = Button(page1, text="Video", command=openVideoPage)
selectPdf = Button(page1, text="PDF", command=openPDFPage)


selectPdf.place(anchor='center', relx=0.5, rely=0.5)
selectVideo.place(anchor='center', relx=0.5, rely=0.6)

#PDF
page2 = Frame(main)
page2.place(anchor='nw', relwidth=1, relheight=1)

title2 = Label(page2, text="pdf analysis")
title2.grid(column=0, row=0, pady=20)

home2 = Button(page2, text="Home", command=lambda: page1.tkraise())
home2.grid(column=1, row=0)
#-------------------PDF stuff----------------------
#Add go-to-page function
class ShowPdf(pdf.ShowPdf):
    def goto(self, page):
        try:
            self.text.see(self.img_object_li[page - 1])
        except IndexError:
            if self.img_object_li:
                self.text.see(self.img_object_li[-1])
#Open pdf stuff
pdfviewer = ShowPdf()
Button(page2, text="Go to page 3", command=lambda: pdfviewer.goto(3)).grid(row=3)
#Resize pdf


def display():
    open_file = filedialog.askopenfilename()

    pdf = open_file
    pdf = PyPDF2.PdfReader(pdf)
    writer = PyPDF2.PdfWriter() 
    for i in range(len(pdf.pages)):
        page0 = pdf.pages[i]
        page0.scale_to(int(0.9*page2.winfo_screenheight()/1.41), int(0.9*page2.winfo_screenheight())) # float representing scale factor - this happens in-place # create a writer to save the updated results
        writer.add_page(page0)
    resizedPdf = "temp.pdf"
    with open(resizedPdf, "wb") as fp:
        writer.write(fp)
    


    pdfframe = pdfviewer.pdf_view(page2, pdf_location="temp.pdf", width=71, height=50 )
    pdfframe.grid(column=2, rowspan=10, row=0)
pdfStart = Button(page2, text="Start", command=display)
pdfStart.grid(row=2,column=0)


#Select looping range
t1 = Label(page2, text="Looping from")
t1.grid(row=4,column=0)
e1 = Entry(page2)
e1.grid(row=5)
t2 = Label(page2, text="to")
t2.grid(row=6)
e2 = Entry(page2)
e2.grid(row=7)
#Initiate looping
loopList = []
currentLoop =0
def loopStarts():
    global currentLoop
    global loopList
    loopList = []
    currentLoop=0
    i=int(e1.get())
    e=int(e2.get())
    while i!=e+1:
        loopList.append(i)
        i=i+1
    pdfviewer.goto(loopList[currentLoop])
    currentLoop=currentLoop+1

def forwardLoop():
    global currentLoop
    if currentLoop<len(loopList):
        pdfviewer.goto(loopList[currentLoop])
        currentLoop=currentLoop+1
    else:
        currentLoop=0
        pdfviewer.goto(loopList[currentLoop])
        currentLoop=currentLoop+1

startLooping = Button(page2, text="start looping", command=loopStarts)
startLooping.grid(row=8)
Next = Button(page2, text="nextpage", command=forwardLoop)

Next.grid(column = 10)









#video
page3 = Frame(main)
page3.place(anchor='nw', relwidth=1, relheight=1)

title3 = Label(page3, text="video analysis")
title3.grid(pady=20, column=0, row=0)

home3 = Button(page3, text="Home", command=lambda: page1.tkraise())
home3.grid(column=2, row=0)

videoplayer=video.TkinterVideo(page3)
def displayVid():
    global videoplayer
    vid_location = filedialog.askopenfilename()
    
    videoplayer.bind("<<Loaded>>", lambda e: e.widget.config(width=0.7*main.winfo_screenwidth(), height=0.7*main.winfo_screenheight()))
    videoplayer.load(vid_location)
    videoplayer.consistant_frame_rate=True
    #videoplayer.set_size((0.9*main.winfo_screenheight()/1.41, 0.9*main.winfo_screenheight()))
    videoplayer.play()
    videoplayer.grid(column=3, row=4)

startVid = Button(page3, text="Select video file", command=displayVid)
startVid.grid()

container= Frame(page3)
container.grid(row=2, column=3, rowspan=1)
vidLooplist=[]
labelList=[]

def bubbleSort(arr):
    
    n = len(arr)

    # For loop to traverse through all 
    # element in an array
    for i in range(n):
        for j in range(0, n - i - 1):
            
            # Range of the array is from 0 to n-i-1
            # Swap the elements if the element found 
            #is greater than the adjacent element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                labelList[j], labelList[j+1] = labelList[j+1], labelList[j]
def getSeconds():
    return round(videoplayer._frame_number/int(videoplayer._video_info['framerate']))
def update():
    bubbleSort(vidLooplist)
    for i in range(len(labelList)):
        labelList[i].grid(row=0,column=i)
def restart():
    global vidLooplist
    for i in range(len(vidLooplist)):
        vidLooplist[i].gmaster.destroy()
    vidLooplist=[]
def addTimestampt():
    global vidLooplist
    mtime = getSeconds()
    
    timestamp = Button(container, text=mtime)
    timestamp.config(command=lambda:remove(timestamp))
    timestamp.grid(row=0, column=len(vidLooplist))
    labelList.append(timestamp)
    vidLooplist.append(mtime)
def remove(self):
    print(self.grid_info()['column'])
    vidLooplist.pop(self.grid_info()['column'])
    
    self.destroy()

  

recordTime = Button(page3, text="mark timestamp", command=addTimestampt)
recordTime.grid(row=1, column=2)

updateList= Button(page3, text="update list", command=update)
updateList.grid(row=0, column=1)
#Select looping range









#Video player

controller = Frame(page3)
controller.grid(row=6, columnspan=5)

def update_duration(event):
    """ updates the duration after finding the duration """
    duration = videoplayer.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_value.set(videoplayer.current_duration())


def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename()

    if file_path:
        videoplayer.load(file_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def seek(value):
    """ used to seek a specific timeframe """
    print(value)
    videoplayer.seek(int(value))
    progress_value.set(value)


def skip(value: int):
    """ skip seconds """
    videoplayer.seek(int(progress_slider.get())+value)
    progress_value.set(progress_slider.get() + value)


def play_pause():
    """ pauses and plays """
    if videoplayer.is_paused():
        videoplayer.play()
        play_pause_btn["text"] = "Pause"

    else:
        videoplayer.pause()
        play_pause_btn["text"] = "Play"


def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)



play_pause_btn = Button(controller, text="Play", command= play_pause)
play_pause_btn.pack()

skip_plus_5sec = Button(controller, text="Skip -5 sec", command=lambda:  skip(-5))
skip_plus_5sec.pack(side="left")

start_time = Label(controller, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_value = IntVar(controller)

progress_slider = Scale(controller, variable=progress_value, from_=0, to=0, orient="horizontal", command= seek)

progress_slider.pack(side="left", fill="x", expand=True)

end_time = Label(controller, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

videoplayer.bind("<<Duration>>",  update_duration)
videoplayer.bind("<<SecondChanged>>",  update_scale)
videoplayer.bind("<<Ended>>",  video_ended )

skip_plus_5sec = Button(controller, text="Skip +5 sec", command=lambda:  skip(5))
skip_plus_5sec.pack(side="left")


#--------------------------------------------

#Looping options
vidCurrentLoop=0
def vidStartLoop():
    global vidCurrentLoop
    global vidLooplist
    vidCurrentLoop=0
    
    seek(vidLooplist[vidCurrentLoop])
    print(vidLooplist[vidCurrentLoop])
    vidCurrentLoop= vidCurrentLoop+1
    videoplayer.play()
    time.sleep(0.1)
    videoplayer.pause()
def vidForwardLoop():
    global vidCurrentLoop
    if vidCurrentLoop<len(vidLooplist):
        
        seek(vidLooplist[vidCurrentLoop])
        print(vidLooplist[vidCurrentLoop])
        vidCurrentLoop=vidCurrentLoop+1
        videoplayer.play()
        time.sleep(0.1)
        videoplayer.pause()
    else:
        vidCurrentLoop=0
        
        seek(vidLooplist[vidCurrentLoop])
        print(vidLooplist[vidCurrentLoop])
        vidCurrentLoop=vidCurrentLoop+1
        videoplayer.play()
        time.sleep(0.1)
        videoplayer.pause()

vidStartLooping = Button(page3, text="start looping", command=vidStartLoop)
vidStartLooping.grid(row=0, column=3)


vidNext = Button(page3, text="nextpage", command=vidForwardLoop)
vidNext.grid(row=0, column=6)


def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == 1:
        # Stop listener
        if(currentPage==1):
            forwardLoop()
            print('pressed')
        elif (currentPage==2):
            vidForwardLoop()
        return False

def key_pressed(event):
   
    if event.keycode == 39:
        # Stop listener
        if(currentPage==1):
            forwardLoop()
            print('pressed')
        elif (currentPage==2):
            vidForwardLoop()
        return False
    
main.bind("<Key>",key_pressed)
# Collect events until released


        
#Settings for window
page1.tkraise()
w, h = main.winfo_screenwidth(), main.winfo_screenheight()
main.geometry("%dx%d+0+0" % (w, h))

main.title("TabsPedal")
main.mainloop()



