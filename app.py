import urllib.request
import threading
import numpy as np

from tkinter import *
from tkinter import messagebox

import os
import time
import signal
from subprocess import Popen

from stock import Stock
from query import datarequest, datarequestv1
from signalgen import signalAnalyze


class Application(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.grid()
        root.protocol("WM_DELETE_WINDOW", self.close)	# self-callback for closing

        # frame0
        self.p = None  # show/killshow handler
        self.pFrame0 = LabelFrame(self, text="COMMANDS", font="Menlo 12 bold", borderwidth=1, labelanchor=N+W)
        self.pFrame0.grid(columnspan=4, sticky=E+W, padx=4, pady=4)
        # first row of widgets ref https://www.youtube.com/watch?v=FwKQwx91NAM
        self.refreshButton = Button(self.pFrame0, text="Refresh", command=lambda: threading.Thread(target=self.refresh, daemon=True).start, font="Menlo 12 bold", pady=4)
        self.saveButton = Button(self.pFrame0, text="Save", command=self.save, font="Menlo 12 bold", pady=4)
        self.quitButton	= Button(self.pFrame0, text="Quit", command=self.close, font="Menlo 12 bold", pady=4)
        self.deleteButton = Button(self.pFrame0, text="Delete", command=self.delete, font="Menlo 12 bold", pady=4)
        self.showButton = Button(self.pFrame0, text="Show", command=self.show, font="Menlo 12 bold", pady=4)
        self.killshowButton = Button(self.pFrame0, text="KillShow", command=self.killshow, font="Menlo 12 bold", pady=4)
        # grid the first row of widgets
        self.refreshButton.grid(row=0, column=0, sticky=W)
        self.saveButton.grid(row=0, column=1, sticky=W)
        self.quitButton.grid(row=0, column=2, sticky=W)
        self.deleteButton.grid(row=0, column=3, sticky=W)
        self.showButton.grid(row=0, column=4, sticky=W)
        self.killshowButton.grid(row=0, column=5, sticky=W)

        # frame1
        self.pFrame1 = LabelFrame(self, text="SELECT SECURITY CATEGORY", font="Menlo 12 bold", borderwidth=1, labelanchor=N+W)
        self.pFrame1.grid(columnspan=4, sticky=E+W, padx=4, pady=4)
        self.switch=IntVar()
        Radiobutton(self.pFrame1, text='Stock', variable=self.switch, value=0).pack(side=LEFT, anchor=W)
        Radiobutton(self.pFrame1, text='Future', variable=self.switch, value=1).pack(side=LEFT, anchor=W)

        # frame1
        self.pFrame2 = LabelFrame(self, text="INPUT YOUR SEUCURITIES", font="Menlo 12 bold", borderwidth=1, labelanchor=N+W)
        self.pFrame2.grid(columnspan=4, sticky=E+W, padx=4, pady=4)
        # second row of widgets
        self.addButton = Button(self.pFrame2, text="Add", command=self.addStock, font="Menlo 12 bold", pady=3)
        # 1
        self.entry = Entry(self.pFrame2, width=30, fg="#757575")
        self.entry.insert(0, "Enter stock ticker symbol")
        self.entry.bind("<Button-1>", self.resetEntry)
        self.entry.bind("<Return>", self.addStock)
        self.entry.grid(row=1, column=1, columnspan=1, pady=3)
        # 2
        self.entry1 = Entry(self.pFrame2, width=30, fg="#757575")
        self.entry1.insert(0, "Enter market symbol")
        self.entry1.bind("<Button-1>", self.resetEntry1)
        self.entry1.bind("<Return>", self.addStock)
        self.entry1.grid(row=1, column=0, columnspan=1, pady=3)
        # 3
        self.addButton.grid(row=1, column=2)

        # add the frame that will display the portfolio widget
        self.pFrame3 = LabelFrame(self, text="PORTFOLIO", font="Menlo 12 bold", borderwidth=1, labelanchor=N+W)
        self.pFrame3.grid(columnspan=10, sticky=E+W, padx=4, pady=4)
        self.pFrame3.columnconfigure(0, weight=1)
        # label-1 
        self.Label = Label(self.pFrame3, text="code     open      high      low       close     volume", font="Menlo 12 bold")
        self.Label.grid(row=2, column=0, columnspan=1, sticky=W)
        # label-2
        self.Label1 = Label(self.pFrame3, width=25, text="signal", font="Menlo 12 bold", anchor='w')
        self.Label1.grid(row=2, column=1, columnspan=1, sticky=W)
        # part-1 code open high low close volume
        self.portfolio = Listbox(self.pFrame3, width=55, height=20, font="Menlo 12 bold")
        self.portfolio["bg"] = "#404040"
        self.portfolio["cursor"] = "hand"
        self.portfolio["bd"] = 0 
        self.portfolio["selectborderwidth"] = 2
        self.portfolio["activestyle"] = "none"
        self.portfolio.grid(row=3, column=0, sticky=E+W, columnspan=1)
        # part-2 signal portfolio
        self.portfolio1 = Listbox(self.pFrame3, width=10, height=20, font="Menlo 12 bold")
        self.portfolio1["bg"] = "#404040"
        self.portfolio1["cursor"] = "hand"
        self.portfolio1["bd"] = 0 
        self.portfolio1["selectborderwidth"] = 2
        self.portfolio1["activestyle"] = "none"
        self.portfolio1.grid(row=3, column=1, sticky=E+W, columnspan=1)
        # some less gui related variables needed
        self.myPortfolio = []		# stores all the stock objects in portfolio widget
        self.myPortfolio1 = []		# stores all the signal objects in portfolio1 widget
        self.portFile = "./config/portfolio.txt"	# cache file
       
        # try to initialize portfolio via input file if present
        try:
            f = open(self.portFile, "r")
            for item in f:
                lst = item.split() 
                tmpStock = Stock(lst[2], lst[1], lst[0], lst[3])
                self.myPortfolio.append(tmpStock)	# Use tickers only
                self.myPortfolio1.append(tmpStock)	# Use tickers only
            f.close()
            # lambda: threading.Thread(target=self.refresh, daemon=True).start()
            self.refresh()  # Refresh to update all stocks and the GUI
        except FileNotFoundError:
            pass

        # enables automatic refreshes, first refresh set 10s(preheating) after app bootstrap
        self.after(5000, self.refreshWrapper)


    # handles all actions related to adding a new stock to portfolio
    def addStock(self, event = None):
        # check for valid input 
        if self.entry.get().strip() == "" or not self.entry1.get().strip().isdigit():
            messagebox.showwarning("No Entry", "Enter a valid stock ticker symbol")
            self.entry.delete(0, END)
        else:
            # make the API request and save the response
            company = self.entry.get().strip().upper()
            market = self.entry1.get().strip().upper()
            data = datarequest(switch=self.switch.get(), marketcode=int(market), stockcode=company)
            if(np.isnan(data[2])):  # invalid
                message = "Pytdx connection to tdxserver succeed, Reading data suceed, But no valid input, please re-enter your security."
                messagebox.showinfo("Done!", message)
            else:  # valid
                # ['2022-04-22 23:00', 21665.0, 21675.0, 21660.0, 21660.0, 40] -> OHLCV
                text = [str(company), str(data[1]), str(data[2]), str(data[3]), str(data[4]), str(data[5]), str(data[0])]
                prev = data[4]
                # create a new stock object with the raw parameters for processing
                newStock = Stock(str(self.switch.get()), market, company, str(prev), text)
                # check if stock is already in portfolio, else --> add it
                for s in self.myPortfolio:
                    if s.getTicker() == newStock.getTicker():
                        messagebox.showwarning("Repeated Entry", "Already in your portfolio!")
                        self.resetEntry(None)
                        self.resetEntry1(None)
                        return
                self.myPortfolio.append(newStock)  # for base info
                toDisplay = newStock.stringify()  
                self.myPortfolio1.append(newStock)  # for signal
                toDisplay1 = newStock.stringify1()
                # add to portfolio and determine color (gain/loss)
                self.portfolio.insert(END, toDisplay[0])
                self.portfolio.see(END)
                self.portfolio1.insert(END, toDisplay1[0])
                self.portfolio1.see(END)
                # if toDisplay[1] == "gain":
                #     self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#66b266")
                # elif toDisplay[1] == "loss":
                #     self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#da2020")
                # else:
                #     self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#404040")

        # clear the entry field regardless
        self.resetEntry(None)
        self.resetEntry1(None)

    # deleting a stock from the portfolio
    def delete(self):
        # check if anything to delete
        if len(self.myPortfolio) == 0:
            return
        # find the stock in portfolio and remove
        ticker = self.portfolio.get(ACTIVE).split()[0]
        for idx, item in enumerate(self.myPortfolio):
            if item.getTicker() == ticker:
                self.myPortfolio.remove(item)  # delete stock
                del self.myPortfolio1[idx]  # delete related signal
        # rehighlight the next stock
        self.portfolio.delete(ACTIVE)
        self.portfolio.selection_set(ACTIVE)

    # used when user refreshes portfolio OR portfolio is initialized by text file
    def refresh(self):
        # check if anything to refresh
        if len(self.myPortfolio) == 0:
            return
        # save the active index before refresh
        activeIndex = self.portfolio.index(ACTIVE)
        # delete all current entries	
        self.portfolio.delete(0, END)

        # construct a chain of ticker symbols for the companies in the portfolio
        companies = ""
        marketlst = []
        switchlst = []
        for s in self.myPortfolio:
            companies += s.getTicker() + " "
            marketlst.append(s.getMarket())
            switchlst.append(s.getSwitch())
        companies = companies[:-1]  # CF2205,CF2209 (str)
        companies = companies.split()  # ['CF2205', 'CF2209'] (list)
          
        threadlst = [None]*len(marketlst)
        datalst = [None]*len(marketlst)

        # update all the stocks in some separate thread, keep mainloop alive when requesting data
        for _ in range(len(threadlst)):
            threadlst[_] = threading.Thread(target=datarequestv1, args=(int(switchlst[_]), int(marketlst[_]), companies[_], datalst, _))
            threadlst[_].start()
        # wait for all thread end
        for _ in range(len(threadlst)):
            threadlst[_].join()
        # update portfolio 
        flag = 0
        for _ in range(len(threadlst)):
            company = companies[_]
            if(flag==0):
                if(np.isnan(datalst[_][1])):
                    message = "Pytdx connection to tdxserver timeout, try click refresh to reload."
                    messagebox.showinfo("Done!", message)
                    flag = flag+1
                elif(np.isnan(datalst[_][5])):
                    message = "Pytdx connection to tdxserver other type error occurs, try click refresh to reload."
                    messagebox.showinfo("Done!", message)
                    flag = flag+1
                elif(np.isnan(datalst[_][2])):
                    message = "Pytdx connection to tdxserver succeed, but return none data, try click refresh to reload."
                    messagebox.showinfo("Done!", message)
                    flag = flag+1
            text = [str(company), str(datalst[_][1]), str(datalst[_][2]), str(datalst[_][3]), str(datalst[_][4]), str(datalst[_][5]), str(datalst[_][4])]
            self.myPortfolio[_].update(text)
        # add the updated stocks back to the portfolio
        for s in self.myPortfolio:
            toDisplay = s.stringify()
            self.portfolio.insert(END, toDisplay[0])
            self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#314F79")
            # status
            # if toDisplay[1] == "gain":
            #     self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#66b266")
            # elif toDisplay[1] == "loss":
            #     self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#da2020")
            # else:
            #     self.portfolio.itemconfig(END, fg="#e5e5e5", selectbackground="#404040")
        # re-activate the index saved
        self.portfolio.activate(activeIndex)
        self.portfolio.selection_set(ACTIVE)
        self.portfolio.see(ACTIVE)

    def refreshSignal(self):
        # check if anything to refresh
        if len(self.myPortfolio1) == 0:
            return
        # delete all current entries	
        self.portfolio1.delete(0, END)
        # todo: ensure when deriving info in myportfolio, myportfolio are not empty by func: refresh()
        # construct a chain of signal symbols using myportfolio, for data request for signal in myportfolio1
        companies = ""
        marketlst = []
        switchlst = []
        siglst = []
        for s in self.myPortfolio:
            companies += s.getTicker() + " "
            marketlst.append(s.getMarket())
            switchlst.append(s.getSwitch())
            siglst.append(s.getSignal())
        companies = companies[:-1]  # CF2205,CF2209 (str)
        companies = companies.split()  # ['CF2205', 'CF2209'] (list)
        # update all the signal in some separate thread, keep mainloop alive when requesting & analysing data
        threadlst = [None]*len(self.myPortfolio)
        for _ in range(len(threadlst)):
            threadlst[_] = threading.Thread(target=signalAnalyze, args=(int(switchlst[_]), int(marketlst[_]), companies[_], siglst, _))
            threadlst[_].start()
        # wait for all thread end
        for _ in range(len(threadlst)):
            threadlst[_].join()
        # update signal in stock obj
        for _ in range(len(threadlst)):
            sig = siglst[_]
            self.myPortfolio1[_].updateSignal(sig)
        # add the updated signal back to the portfolio1
        for s in self.myPortfolio1:
            toDisplay = s.stringify1()
            self.portfolio1.insert(END, toDisplay[0])
            # status1
            if toDisplay[1] == "gain":
                self.portfolio1.itemconfig(END, fg="#e5e5e5", selectbackground="#66b266")
            elif toDisplay[1] == "loss":
                self.portfolio1.itemconfig(END, fg="#e5e5e5", selectbackground="#da2020")
            else:
                self.portfolio1.itemconfig(END, fg="#e5e5e5", selectbackground="#404040")

    # used to enable automatic refresh 1s a time
    def refreshWrapper(self):
        self.refresh()
        self.refreshSignal()
        self.after(1000, self.refreshWrapper)

    # event handler when user first clicks on the entry field
    def resetEntry(self, event):
        self.entry.delete(0, END)
        self.entry["fg"] = "white"
    def resetEntry1(self, event):
        self.entry1.delete(0, END)
        self.entry1["fg"] = "white"

    # when user explicitly saves the file
    def save(self):
        if(self.portfolio.size()==0):
            # open the portfolio text file and save all the tickers
            f = open(self.portFile, "w")
            for s in self.myPortfolio:
                print(s.getTicker()+" "+s.getMarket()+" "+s.getSwitch()+" "+s.getPrev(), file = f)
            f.close()
            # display failure message
            message = "No companies in your portfolio."
            messagebox.showinfo("Done!", message)
        else:
            # open the portfolio text file and save all the tickers
            f = open(self.portFile, "w")
            for s in self.myPortfolio:
                # Name: 601225 | Ticker: 601225 | Price: 16.57 | ∆: +16.57 | %: +16.57 | Status: gain
                print(s.getTicker()+" "+s.getMarket()+" "+s.getSwitch()+" "+s.getPrev(), file = f)
            f.close()
            # display success message
            message = "Saved " + str(self.portfolio.size()) + " companies to your portfolio."
            messagebox.showinfo("Saved!", message)

    def show(self):
        # check if anything to show
        if len(self.myPortfolio) == 0:
            return
        # derive active idx
        activeIndex = self.portfolio.index(ACTIVE)
        # build global config obj 
        sw = int(self.myPortfolio[activeIndex].getSwitch())
        from pytdx.params import TDXParams
        tdx = 8  # 1min
        m_c = self.myPortfolio[activeIndex].getMarket()
        s_c = self.myPortfolio[activeIndex].getTicker()
        # write a ini file using params above -> ref: https://docs.python.org/zh-tw/3/library/configparser.html
        import configparser
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'switch':sw, 'period':tdx, 'marketcode':m_c, 'stockcode':s_c, 'start':0, 'num':800}
        with open('./config/default.ini', 'w') as cfg:
            config.write(cfg)
        # run show
        self.p = Popen('./shell/start.sh', shell=True, preexec_fn=os.setsid)
        # self.p = Popen('./shell/test.sh', shell=True)

    def killshow(self):
        self.p = Popen('./shell/kill.sh', shell=True, preexec_fn=os.setsid)
        # self.p = Popen('./shell/kill.sh', shell=True)

    # when user explicitly presses my "close" button or [X] out of the window
    def close(self):
        if messagebox.askyesno("Quit", "Are you sure? Did you save first?"):
            self.quit()

