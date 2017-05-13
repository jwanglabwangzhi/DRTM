# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import webbrowser
import time
import commands,os,subprocess
from get_peak_calling import *
path = sys.path[0]

try:
    from Tkinter import *
    import tkFont
    import tkFileDialog
except ImportError as err:
    print ("error: %s. Tkinter library is required for using the GUI.") % err.message
    sys.exit(1)

#from AutomataTheory import *

dotFound = False   #hhhhhhhhhhh这是可以换成bedtools found的


class myprogramme:
    

    def __init__(self, root, dotFound):
        self.root = root
        self.initUI()
        self.selectedButton = 0
        self.dotFound = dotFound              
        self.basicButton()
        



    def hello(self):
        print 'hello'
    def hell(self):
        print 'hell'




    def initUI(self):
        self.root.title("DRTM")


        ScreenSizeX = self.root.winfo_screenwidth()   #这个为了得到每个人电脑屏幕的尺寸
        ScreenSizeY = self.root.winfo_screenheight()
        ScreenRatioX = 0.7
        ScreenRatioY = 0.8
        self.FrameSizeX  = int(ScreenSizeX * ScreenRatioX)
        self.FrameSizeY  = int(ScreenSizeY * ScreenRatioY)
        print self.FrameSizeY, self.FrameSizeX
        FramePosX   = (ScreenSizeX - self.FrameSizeX)/2
        FramePosY   = (ScreenSizeY - self.FrameSizeY)/2
        padX = 10
        padY = 10
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX,self.FrameSizeY,FramePosX,FramePosY))
        self.root.resizable(width=False, height=False)
        parentFrame = Frame(self.root, width = int(self.FrameSizeX - 2*padX), height = int(self.FrameSizeY - 2*padY))
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)



        introFrame = Frame(parentFrame)             #这个是一个frame上面有几个字
        welcomeLabel = Label(introFrame, text="Welcome to DRTM !",width=20,height=5,font=("Helvetica", 19, "bold"))
        #buildRegexButton = Button(introFrame, text="Build", width=10, command=self.hello)
        welcomeLabel.grid(row=0, column=0, sticky=W)
        introLabel   = Label(introFrame, text="DRTM is a tool with three main functions,call_peaks,intergenetic_miRNA\nannotation,TSS of miRNA recognition respectively.",width=70)
        introLabel.grid(row=1,column=0,sticky=W)
        #buildRegexButton.grid(row=1, column=1, padx=5)
        introFrame.grid(row=0, column=0, sticky=W, padx=(50,0))
        #这边还缺两个功能


        buttonGroup = Frame(parentFrame)        
        peak_calling_Button = Button(buttonGroup, text="peak calling", width=15, command=self.handle_peak_calling_Button)     
        intergenetic_Button = Button(buttonGroup, text="intergenetic miRNA", width=15, command=self.handle_intersect_gene_Button)
        TSS_Button = Button(buttonGroup, text="miRNA TSS finder", width=15, command=self.handle_TSS_Button)
        peak_calling_Button.grid(row=0, column=0)
        intergenetic_Button.grid(row=0, column=1)
        TSS_Button.grid(row=0, column=2)
        buttonGroup.grid(row=1, column=0,sticky=W, pady=10)



        self.automataCanvasFrame = Frame(parentFrame, height=100, width=100)     #尽量不要继承画布，而是用画布的添加命令
        self.cwidth = int(self.FrameSizeX - (2*padX + 20))
        self.cheight = int(self.FrameSizeY * 0.6)
        self.automataCanvas = Canvas(self.automataCanvasFrame, bg='#FFFFFF', width= self.cwidth, height = self.cheight,scrollregion=(0,0,self.cwidth,self.cheight))
        hbar=Scrollbar(self.automataCanvasFrame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.automataCanvas.xview)
        vbar=Scrollbar(self.automataCanvasFrame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.automataCanvas.yview)
        self.automataCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvasitems = []        
        self.automataCanvas.pack()
        self.automataCanvasFrame.grid(row=2, column=0, sticky=E+W+N+S)



        self.bottomLabel = Label(parentFrame, text="The project was developed in Jwang laboratory ")
        self.bottomLabel.grid(row=3, column=0, sticky=W, pady=10)



    def handle_peak_calling_Button(self):
        self.selectedButton = 0
        self.displayAutomata()
    def handle_intersect_gene_Button(self):
        self.selectedButton = 1
        self.displayAutomata()
    def handle_TSS_Button(self):
        self.selectedButton = 2
        self.displayAutomata()



    def basicButton(self):
        self.createAutomata()
        self.displayAutomata()



    def createAutomata(self):
        for item in self.canvasitems:
            self.automataCanvas.delete(item)
        header = "Peak calling"
        use_protocal="This section apply an easy way to call peaks , you can load bam file to run it."
        RUN_button=Button(self.automataCanvasFrame,text="RUN",command=self.hello)   #把函数改掉
        RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)





    def displayAutomata(self):
        
        
        for item in self.canvasitems:
            self.automataCanvas.delete(item)      #把画布上的东西都清楚
        if self.selectedButton == 0:
            header = "Peak calling"
            use_protocal="This section apply an easy way to call peaks , you can load bam file to run it."
            result_var=(" ")        #初始的按钮文本
            RUN_button=Button(self.automataCanvasFrame,text="RUN",command=self.get_peak)   #把函数改掉
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(130, 110, anchor=NW, window=RUN_button)
            
            
        elif self.selectedButton == 1:
            header = "intergentic miRNA finder"
            use_protocal="This section help you find intergenetic miRNA that you load , \nplease load miRNA name in a txt file."
            result_var=(" ")
            RUN_button=Button(self.automataCanvasFrame,text="RUN",command=self.get_intergentic_miRNA)   #把函数改掉
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(300, 110, anchor=NW, window=RUN_button)

        elif self.selectedButton == 2:
            header = "MiRNA TSS finder"
            use_protocal="This section will find TSS of miRNA that you load , please load pol II peak file."
            result_var=(" ")
            RUN_button=Button(self.automataCanvasFrame,text="RUN",command=self.get_miRNA_tss)   #把函数改掉
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(300, 110, anchor=NW, window=RUN_button)



        elif self.selectedButton == 3:
            header = "Peak calling"
            use_protocal=" "
            result_var=("Warning: file has something wrong , please reload file .")        #初始的按钮文本
            RUN_button=Button(self.automataCanvasFrame,text="CLOSE",command=self.handle_peak_calling_Button)   #把函数换成返回到0的
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(130, 110, anchor=NW, window=RUN_button)
        elif self.selectedButton == 4:
            header = "Peak calling"
            use_protocal="  "
            result_var=("peak calling is running,please wait ...")        #初始的按钮文本
            RUN_button=Button(self.automataCanvasFrame,text="RUNNING...",command=self.hello)   #把函数换成返回到0的
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(130, 110, anchor=NW, window=RUN_button)
        elif self.selectedButton == 5:
            header = "Peak calling"
            use_protocal=" "
            result_var=("Peak calling has been finished , %s peaks have been found , you can find specific content \nin %s/NA_peaks.Peak ."%(self.number,path))        #初始的按钮文本
            RUN_button=Button(self.automataCanvasFrame,text="FINISH",command=self.handle_peak_calling_Button)   #把函数换成返回到0的
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(130, 100, anchor=NW, window=RUN_button)
        elif self.selectedButton == 6:
            header = "intergentic miRNA finder"
            use_protocal=" "
            result_var=("Warning: file has something wrong , please reload file .")        #初始的按钮文本
            RUN_button=Button(self.automataCanvasFrame,text="CLOSE",command=self.handle_intersect_gene_Button)   #把函数换成返回到0的
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(130, 110, anchor=NW, window=RUN_button)
        elif self.selectedButton == 7:
            header = "intergentic miRNA finder"
            use_protocal=" "
            result_var=("The intergentic miRNA has been selected , you can find specific content \nin %s/expressed_intergentic_miRNA.txt ."%path)
            RUN_button=Button(self.automataCanvasFrame,text="FINISH",command=self.handle_intersect_gene_Button)   #把函数改掉
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(300, 110, anchor=NW, window=RUN_button)  
        elif self.selectedButton == 8:
            header = "MiRNA TSS finder"
            use_protocal=" "
            result_var=("Warning: file has something wrong , please reload file .")        #初始的按钮文本
            RUN_button=Button(self.automataCanvasFrame,text="CLOSE",command=self.handle_TSS_Button)   #把函数换成返回到0的
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(130, 110, anchor=NW, window=RUN_button)
        elif self.selectedButton == 9:
            header = "MiRNA TSS finder"
            use_protocal=" "
            result_var=("The intergentic miRNA TSS has been found , you can find specific content \nin %s/mirna_tss.bed ."%path)
            RUN_button=Button(self.automataCanvasFrame,text="FINISH",command=self.handle_TSS_Button)   #把函数改掉
            RUN_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            RUN_button_window = self.automataCanvas.create_window(300, 110, anchor=NW, window=RUN_button)  


        

        font = tkFont.Font(family="Courier New", size=20)
        (w,h) = (font.measure(header),font.metrics("linespace"))
        headerheight = h + 10
        header_txt = self.automataCanvas.create_text(10,10,text=header, font=font, anchor=NW)       #搞一堆为了把控件添加到list中
        protocal_txt =self.automataCanvas.create_text(10,80,text=use_protocal, font=tkFont.Font(family='Fixdsys', size=20),anchor=W)
        result_txt =self.automataCanvas.create_text(10,70,text=result_var, font=tkFont.Font(family='Fixdsys', size=20),anchor=W)

        self.canvasitems.append(header_txt)
        self.canvasitems.append(protocal_txt)
        self.canvasitems.append(RUN_button_window)
        self.canvasitems.append(result_txt)
        font = tkFont.Font(family="times", size=13)

        textheight = headerheight


        totalwidth = self.cwidth + 10
        totalheight = textheight + 10
        if totalheight < self.cheight:
            totalheight = self.cheight
        if totalwidth < self.cwidth:
            totalwidth = self.cwidth
        self.automataCanvas.config(scrollregion=(0,0,totalwidth,totalheight))



    def get_peak(self):
        #print original_bam_file
        try:
            os.remove('NA_peaks.Peak')
        except:
            pass
        
        if original_bam_file[-3:]<>'bam':
            self.selectedButton = 3       
            self.displayAutomata()
        else:
            try:                
                self.selectedButton = 4             #这里怎么搞都搞不出please，wait的效果，先这样凑合着吧      
                self.displayAutomata() 
                try:
                    number=get_peak_call(original_bam_file)   #这里如果不多用一个调试文件get_peak_call，出不来结果
                    #number=8
                except:
                    print 'your file has something wrong'
                self.number=number
                self.selectedButton = 5  
                self.displayAutomata()               
                                                                                                                            
            except:
                self.selectedButton = 3       
                self.displayAutomata()



    def get_intergentic_miRNA(self):
        try:
            os.remove('expressed_intergentic_miRNA.txt')
        except:
            pass
        
        if original_bam_file[-3:]<>'txt':
            self.selectedButton = 6       
            self.displayAutomata()
        else:
            try:  
                all_inter_mirna_set=set()
                expressed_intergentic_miRNA=open('expressed_intergentic_miRNA.txt','w')
                with open('./pre_loaded_data/please_inter_mirna_region.bed') as all_inter_mirna:
                    all_inter_mirna_lines=all_inter_mirna.readlines()
                for all_inter_mirna_line in all_inter_mirna_lines:
                    all_inter_mirna_split=all_inter_mirna_line.rstrip('\n').split('\t')
                    all_inter_mirna_set.add(all_inter_mirna_split[3])
                with open(original_bam_file) as all_expressed_mirna:
                    all_expressed_mirna_lines=all_expressed_mirna.readlines()
                for all_expressed_mirna_line in all_expressed_mirna_lines:
                    if all_expressed_mirna_line.rstrip() in all_inter_mirna_set:
                        expressed_intergentic_miRNA.write(all_expressed_mirna_line)

                expressed_intergentic_miRNA.close
            except:
                self.selectedButton = 6       
                self.displayAutomata()
        self.selectedButton = 7       
        self.displayAutomata()



    def get_miRNA_tss(self):
        try:
            os.remove('mirna_tss.bed')
        except:
            pass        
        if original_bam_file[-4:]<>'Peak':
            self.selectedButton = 8       
            self.displayAutomata()
        else:
            try:
                os.system('python main6.py %s'%original_bam_file)
                with open('new_sort_three.bed') as new_sort_three:
                    new_sort_three_lines=new_sort_three.readlines()


                e=set()
                for new_sort_three_line in new_sort_three_lines:
                    new_sort_three_split=new_sort_three_line.rstrip('\n').rstrip('\r').split('\t')
                    e.add(new_sort_three_split[-4])




                mirna_peak_site_score_file=open('mirna_peak_site_score.bed','w')
                for mirna_name in e:
                    for new_sort_three_line in new_sort_three_lines:
                        new_sort_three_split=new_sort_three_line.rstrip('\n').rstrip('\r').split('\t')
                        if new_sort_three_split[-4]==mirna_name:
                           mirna_peak_site_line=new_sort_three_split[0]+'\t'+str(int((int(new_sort_three_split[1])+int(new_sort_three_split[2]))*0.5))+'\t'+str(int((int(new_sort_three_split[1])+int(new_sort_three_split[2]))*0.5)+1)+'\t'+new_sort_three_split[-4]+'\t'+str(float(new_sort_three_split[6])+float(new_sort_three_split[-1])*10)+'\t'+new_sort_three_split[-2]+'\n'
                           mirna_peak_site_score_file.write(mirna_peak_site_line)



                dic6={}       
                mirna_peak_site_score_file.close()
                with open('mirna_peak_site_score.bed') as mirna_peak_site_score:
                    mirna_peak_site_score_lines=mirna_peak_site_score.readlines()
                for mirna_peak_site_score_line in mirna_peak_site_score_lines:
                    mirna_peak_site_score_split=mirna_peak_site_score_line.rstrip('\n').split('\t')
                    dic6.setdefault(mirna_peak_site_score_split[3],[]).append(float(mirna_peak_site_score_split[4]))
                mirna_tss=open('mirna_tss.bed','w')
                for mirna_score_name in dic6.keys():
                    for mirna_peak_site_score_line in mirna_peak_site_score_lines:
                        mirna_peak_site_score_split=mirna_peak_site_score_line.rstrip('\n').split('\t')
                        if mirna_peak_site_score_split[3]+mirna_peak_site_score_split[4]==mirna_score_name+str(max(dic6[mirna_score_name])):
                            mirna_tss.write(mirna_peak_site_score_line)
                mirna_tss.close()
                    

                os.remove('mirna_peak_site_score.bed')
                os.remove('new_sort_three.bed')        
                    
            except:
                self.selectedButton = 8       
                self.displayAutomata()


        self.selectedButton = 9       
        self.displayAutomata()                   


              
                     

def selectfile(): 
    global original_bam_file       
    original_bam_file = tkFileDialog.askopenfilename(filetypes=[("bam file", "*.bam"),("txt files", "*.txt"),("Peak files", "*Peak")])
    #print 'your file '+original_bam_file+' has been chosen,you can call peaks by pressing RUN'+original_bam_file[-3:]



def get_tools_web():
    url='http://mcube.nju.edu.cn/jwang/cn/software.html'
    webbrowser.open(url,new=1,autoraise=True)
def get_protocal_web():
    url=''#pumin的博客
    webbrowser.open(url,new=1,autoraise=True)
          
def hello():
    print 'hello'

def main():
    global dotFound     #hhhhhhhhhhh
    
    
    root = Tk()
    menubar = Menu(root)
    def filemenu(menubar):
    # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load file", command=selectfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

    def othertoolsmenu(menubar):
        othertoolsmenu=Menu(menubar,tearoff=0)
        othertoolsmenu.add_command(label='connection',command=get_tools_web)
        menubar.add_cascade(label='Other tools',menu=othertoolsmenu)


    def protocalmenu(menubar):
        protocalmenu=Menu(menubar,tearoff=0)
        protocalmenu.add_command(label='puminboke',command=get_protocal_web)
        menubar.add_cascade(label='Protocal tools',menu=protocalmenu)

    def aboutmenu(menubar):
        aboutmenu=Menu(menubar,tearoff=0)
        aboutmenu.add_command(label="wz",command=hello)
        menubar.add_cascade(label='About',menu=aboutmenu)
    filemenu(menubar)
    othertoolsmenu(menubar)
    protocalmenu(menubar)
    aboutmenu(menubar)
    root.config(menu=menubar)
    app = myprogramme(root, dotFound)    #dotFound倒是可以改成bedtools found
    root.mainloop()


if __name__ == '__main__':
    main()
