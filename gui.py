from tkinter import *
from tkinter import filedialog
from os import getcwd
from model import Model
from tkinter import messagebox

#Instantiate Model
model = Model()


# --------- ROOT WINDOW --------- #

root = Tk()
root.title("FatlirT's Model Maker")


main = Frame(root)
main.pack(padx=20, pady=20)


# --------- IMPORT DATA --------- #

filepath = StringVar()

def setdpcs():
    if len(filepath.get()) != 0:
        vcb['state'] = "normal"
        adb['state'] = "normal"
        scpb['state'] = "normal"
        slm.configure(state=NORMAL)
    else: 
        vcb['state'] = "disabled"
        adb['state'] = "disabled"
        scpb['state'] = "disabled"
        slm.configure(state=DISABLED)

def openfile():
    main.filename = filedialog.askopenfilename(initialdir=getcwd(), title="Select CSV file", filetypes=(("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")))
    if len(main.filename) != 0:
        try:
            model.readin(main.filename)
        except:
            messagebox.showerror(title="Invalid File Format", message="The file has an invalid format.")
    filepath.set(main.filename)
    add_options(slm, model.get_df().columns.tolist())
    setdpcs()


def add_options(menu, new_options):
    menu.children['menu'].delete(0, 'end')
    for o in new_options:
        menu.children['menu'].add_command(label=o, command=lambda opt=o: [slv.set(opt), setsfbstate()])



idl = Label(main, text="Import CSV File:")
idl.grid(row=0, sticky=E)

ide = Entry(main, textvariable=filepath, state=DISABLED, disabledbackground="white", disabledforeground="black")
ide.grid(row=0, column=1, sticky=W)

idnl = Label(main, text="(delimeter must be a comma)")
idnl.grid(row=1, column=1, sticky=W)

idb = Button(main, text="Select file...", command=openfile)
idb.grid(row=2, columnspan=2)

idsf = Frame(main)
idsf.grid(row=3, pady=10)



# --------- VIEW CORRELATIONS --------- #


vcb = Button(main, text="View correlations", state="disabled", command=model.showcorrelations)
vcb.grid(row=4, columnspan=2)

vcsf = Frame(main)
vcsf.grid(row=5, pady=10)


# --------- ATTR. RANGES --------- #

am = {}


def adw():
    top = Toplevel()
    top.title("Enter atribute ranges")

    genfrem = Frame(top)
    genfrem.pack()

    adc = Canvas(genfrem)
    adc.pack(side=LEFT, expand=1, padx=10, pady=10)
    adcsb = Scrollbar(genfrem, orient=VERTICAL, command=adc.yview)
    adcsb.pack(side=RIGHT, fill=Y)
    adc.configure(yscrollcommand=adcsb.set)
    adc.bind('<Configure>', lambda e: adc.configure(scrollregion=adc.bbox("all")))
    
    bfrem = Frame(top)
    bfrem.pack(side=BOTTOM)
    frem = Frame(adc)

    t = Label(top, text="(seperate categories with \",\" and define a range like \"1to5\")")
    t.pack(anchor="center")

    adc.create_window((0,0), window=frem, anchor="nw")

    tbvs = {}

    def savevals():
        for k in tbvs:
            am[k] = [tbvs[k][0].get(), tbvs[k][1].get()]
        print(am)
        model.df_set_attr_meta(am)
    
    attrs = [e for e in model.get_df().columns.tolist()]

    for a in attrs:
        r = attrs.index(a)
        v = StringVar()
        ael = Label(frem, text=a+": ")
        ael.grid(row=r)
        ccbv = IntVar()
        if model.get_df().dtypes[a] != object:
            ccb = Checkbutton(frem, text="Ordinal", variable=ccbv)
            ccb.grid(row=r, column=1)
        ae = Entry(frem, textvariable=v)
        ae.grid(row=r, column=2)
        tbvs[a] = [ccbv, v]
        
    cs = Button(bfrem, text="Confirm Definitions", command=savevals)
    cs.grid(padx=10, pady=10)


adb = Button(main, text="Define meta-data...", command=adw, state="disabled")
adb.grid(row=6, columnspan=2)

ead4 = Frame(main)
ead4.grid(row=7, pady=10)


# --------- CLEANSE PARAMETERS --------- #

cp = {}


def adw():
    top = Toplevel()
    top.title("Set Cleanse Parameters")

    frem = Frame(top)
    frem.pack(padx=20, pady=20)

    
    def savevals():
        cp["th"] = ts.get()
        cp["av"] = avv.get()
        print(cp)
    
    
    tl = Label(frem, text="pct invalid for column drop: ")
    tl.grid(row=0, sticky=E)
    ts = Scale(frem, from_=0, to=100, orient=HORIZONTAL)
    ts.grid(row=0, column=1)

    avv = StringVar()
    avl = Label(frem, text="averaging method for replacement values: ")
    avl.grid(row=1, sticky=E)
    avf = Frame(frem)
    avf.grid(row=1, column=1)
    avrmea = Radiobutton(avf, text="Mean", variable=avv, value="mean")
    avrmea.grid(row=0, column=0)
    avrmed = Radiobutton(avf, text="Median", variable=avv, value="median")
    avrmed.grid(row=0, column=1)
    avrmod = Radiobutton(avf, text="Mode", variable=avv, value="mode")
    avrmod.grid(row=0, column=2)

    cs = Button(frem, text="Set Parameters", command=savevals)
    cs.grid(row=2, columnspan=2, padx=10, pady=10)



scpb = Button(main, text="Cleansing Parameters", command=adw, state="disabled")
scpb.grid(row=8, columnspan=2)

scp4 = Frame(main)
scp4.grid(row=9, pady=10)



# --------- SELECT LABEL --------- #

def setsfbstate():
    if len(slv.get()) != 0:
        d4.clear()
        sfb['state'] = "normal"
    else: 
        sfb['state'] = "disabled"

sll = Label(main, text="Select label:")
sll.grid(row=10, sticky=E)
slo = ["l"]
slv = StringVar()
slm = OptionMenu(main, slv, *slo)
slm.configure(state=DISABLED)
slm.grid(row=10, column=1, sticky=W)

slsf = Frame(main)
slsf.grid(row=11, pady=10)


# --------- SELECT FEATURES --------- #

d4 = {}


def fsw():
    top = Toplevel()
    top.title("Select Features")

    genfrem = Frame(top)
    genfrem.pack()

    sfc = Canvas(genfrem)
    sfc.pack(side=LEFT, expand=1, padx=10, pady=10)
    sfcsb = Scrollbar(genfrem, orient=VERTICAL, command=sfc.yview)
    sfcsb.pack(side=RIGHT, fill=Y)
    sfc.configure(yscrollcommand=sfcsb.set)
    sfc.bind('<Configure>', lambda e: sfc.configure(scrollregion=sfc.bbox("all")))
    
    bfrem = Frame(top)
    bfrem.pack(side=BOTTOM)
    frem = Frame(sfc)

    sfc.create_window((0,0), window=frem, anchor="nw")

    cbvs = {}

    def savevals():
        for k in cbvs:
            d4[k] = cbvs[k].get()
        if not all(value == 0 for value in d4.values()):
            smm.configure(state=NORMAL)
        else:
            smm.configure(state=DISABLED)
        print(d4)
    
    temp_cols = [e for e in model.get_df().columns.tolist()]
    if slv.get() in temp_cols:
        temp_cols.remove(slv.get())
    fs = temp_cols

    for f in fs:
        r = fs.index(f)
        v = IntVar()
        fc = Checkbutton(frem, text=f, variable=v)
        if not d4 or d4[f] == 1:
            fc.select()
        fc.grid(row=r)
        cbvs[f] = v
        
    cs = Button(bfrem, text="Confirm Selection", command=savevals)
    cs.grid(row=0, padx=10, pady=10)

sfb = Button(main, text="Select Features...", command=fsw, state="disabled")
sfb.grid(row=12, columnspan=2)

esf4 = Frame(main)
esf4.grid(row=13, pady=10)


# --------- SELECT MODEL --------- #

sml = Label(main, text="Select Algorithm:")
sml.grid(row=14, sticky=E)

smv = StringVar()

def setscbstate(event):
    prb['state'] = "normal"
    if smv.get().split(' ')[-1] == "Classifier":
        scb['state'] = "normal"
    else: 
        scb['state'] = "disabled"

    
smo = model.algmap.keys()
smm = OptionMenu(main, smv, *smo, command=setscbstate)
smm.configure(state=DISABLED)
smm.grid(row=14, column=1, sticky=W)

smsf = Frame(main)
smsf.grid(row=15, pady=10)





# --------- SET CLASSES --------- #

doc = {}

def sc():

    doc.clear()
    scw = Toplevel()
    scw.title("Set classes for " + slv.get())

    m = Frame(scw)
    m.pack(padx=20, pady=20)

    zz = Label(m, text="Range:")
    zz.grid(row=0, sticky="ew")

    vv = Label(m, text="Name:")
    vv.grid(row=0, column=1, sticky="ew")

    r = Frame(m, bg="white")
    r.grid(row=1)

    n = Frame(m, bg="white")
    n.grid(row=1, column=1)


    #load saved classes

    #add new class

    def anc():
        try:
            if int(fov.get()) >= int(tov.get()):
                return
        except: 
            return
        if nov.get() in doc.keys() or [fov.get(), tov.get()] in doc.values():
            return
        for e in doc.values():
            if int(e[1]) >= int(fov.get()):
                return
        gs = r.grid_size()[1]
        bgc = "lightgrey"
        if gs % 2 != 0:
            bgc = 'white'
        rl = Label(r, text=fov.get()+"-"+tov.get(), bg=bgc)
        rl.grid(sticky="ew")
        nl = Label(n, text=nov.get(), bg=bgc)
        nl.grid(sticky="ew")
        doc[nov.get()] = [fov.get(),tov.get()]
        print(doc)

           

        

    fov = StringVar()
    tov = StringVar()
    nov = StringVar()

    bot = Frame(scw)
    bot.pack(side="bottom", pady=20, padx=20)

    cf = Frame(bot)
    cf.grid(row=0, columnspan=3) 
    foe = Entry(cf, textvariable=fov)
    foe.grid(sticky=W)
    tol = Label(cf, text="to")
    tol.grid(row=0, column=1, sticky=EW, ipadx=10)
    toe = Entry(cf, textvariable=tov)
    toe.grid(row=0, column=2, sticky=W)
    fl = Label(cf)
    fl.grid(row=0, column=3, sticky=EW, ipadx=30)
    nl = Label(cf, text="Name:")
    nl.grid(row=0, column=4, sticky=EW)
    ne = Entry(cf, textvariable=nov)
    ne.grid(row=0, column=5, sticky=W)


    

    reb = Button(bot, text="+ class", command=anc)
    reb.grid(row=1, column=1, pady=10)


scb = Button(main, text="Define Classes...", command=sc, state="disabled")
scb.grid(row=16, columnspan=2)

scsf = Frame(main)
scsf.grid(row=17, pady=10)





# --------- TRAIN AND TEST --------- #

def rp():

    fs = []
    for f in d4:
        if d4[f] == 1:
            fs.append(f)
    print(fs)


    predata = model.tnt(smv.get(), fs, slv.get(), doc, cp)

    if predata is None:
        messagebox.showerror("Algorithm Error", "Cannot use a Regression algorithm on a discrete label.")
        return

    
    rpw = Toplevel()
    rpw.title("Results")

    genfrem = Frame(rpw)
    genfrem.pack()

    prc = Canvas(genfrem)
    prc.pack(side=LEFT, expand=1, padx=10, pady=10)
    prcsb = Scrollbar(genfrem, orient=VERTICAL, command=prc.yview)
    prcsb.pack(side=RIGHT, fill=Y)
    prc.configure(yscrollcommand=prcsb.set)
    prc.bind('<Configure>', lambda e: prc.configure(scrollregion=prc.bbox("all")))
    
    bfrem = Frame(rpw)
    bfrem.pack(side=BOTTOM)
    frem = Frame(prc)

    prc.create_window((0,0), window=frem, anchor="n")

    m = Frame(frem)
    m.grid(padx=20, pady=20)

    zz = Label(m, text="Actual:")
    zz.grid(row=0)

    vv = Label(m, text="Predicted:")
    vv.grid(row=0, column=1)

    a = Frame(m, bg="white")
    a.grid(row=1, padx=10, pady=10)

    p = Frame(m, bg="white")
    p.grid(row=1, column=1, padx=10, pady=10)
    
    for idx, v in enumerate(predata[1]):
        bgc = "white"
        if idx%2 == 1: bgc = "lightgrey"
        g = Label(a, text=v, bg=bgc)
        g.grid(row=idx, sticky=EW, ipadx=30)

    for idx, v in enumerate(predata[2]):
        bgc = "white"
        if idx%2 == 1: bgc = "lightgrey"
        g = Label(p, text=v, bg=bgc)
        g.grid(row=idx, sticky=EW, ipadx=30)
    
    bot = Frame(rpw)
    bot.pack(side="bottom", pady=20)

    al = Label(bot, text="Accuracy: " +  str(round(predata[0], 3)))
    al.grid(row=0, columnspan=2)


    sf1 = Frame(bot)
    sf1.grid(row=1, pady=10)    

    cvstl = Label(bot, text="Cross-Val Accuracy (10 Fold):")
    cvstl.grid(row=2, columnspan=2, sticky=EW)

    cvsvl = Label(bot, text=str(round(predata[6], 3)) + " +/- " + str(round(predata[7], 4)))
    cvsvl.grid(row=3, columnspan=2)

    sf2 = Frame(bot)
    sf2.grid(row=4, pady=10) 

    if "Classifier" in smv.get():
        coml = Label(bot, text="Confusion Matrix:")
        coml.grid(row=5, columnspan=2, sticky=EW)
        com = Label(bot, text=predata[3])
        com.grid(row=6, columnspan=2)

        sfcclf = Frame(bot)
        sfcclf.grid(row=7, pady=10)

        clfrepl = Label(bot, text="Classification Report:")
        clfrepl.grid(row=8, columnspan=2, sticky=EW)
        clfrep = Label(bot, text=predata[4])
        clfrep.grid(row=9, columnspan=2) 
    else:
        msel = Label(bot, text="Mean Squared Error:")
        msel.grid(row=5, sticky=E)
        mse = Label(bot, text=round(predata[5], 3))
        mse.grid(row=5, column=1, sticky=W)



prb = Button(main, text="Train and Test Model", command=rp, state="disabled")
prb.grid(row=18, columnspan=2)

prbsf = Frame(main)
prbsf.grid(row=19, pady=10)



root.mainloop()
