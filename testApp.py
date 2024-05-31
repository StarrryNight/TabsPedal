
from tkinter import *
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
import PyPDF2
from screeninfo import get_monitors

main=  Tk()

#Home page

page1 = Frame(main, padx=100, pady=100)
page1.grid(row=0, column=0)


title1 = Label(page1, text="home")
title1.grid(row=0, column=0, pady=20)

selectVideo = Button(page1, text="Video", command=lambda: page3.tkraise())
selectPdf = Button(page1, text="PDF", command=lambda: page2.tkraise())

selectPdf.grid(row=1, column=0)
selectVideo.grid(row=2, column=0)

#PDF
page2 = Frame(main, padx=100)
page2.grid(row=0, column=0)

title2 = Label(page2, text="pdf analysis")
title2.grid(column=0, row=0, pady=20)


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
Next.grid(row=9)









#video
page3 = Frame(main,padx=100, pady=100)
page3.grid(row=0, column=0)

title3 = Label(page3, text="video analysis")
title3.grid(pady=20, column=0, row=0)


page1.tkraise()

page1.tkraise()

page1.tkraise()

page1.tkraise()



main.title("TabsPedal")
main.mainloop()

