from tkinter import *
from PIL import Image,ImageTk 
from ttkthemes import themed_tk as tk
from tkinter import ttk
import os
import threading
from time import sleep
from pygame import mixer
from tkinter import filedialog
from tkinter import messagebox
from tinytag import TinyTag

mixer.init() 
mixer.music.set_volume(1)  #set volume here 
playlist_list=[]     # variable for playlist
muted=False     #variable for mute/unmute
paused=False  #variable for play_pause
running=True

def on_closing():
    global paused,running
    if(messagebox.askokcancel("Quit","Do you want to exit?")):
        mixer.music.stop()
        paused=True
        running=False
        sleep(1.2)
        root.destroy()

# adding song to playlist start function
def addPlaylist(filepath):
    filename=os.path.basename(filepath)   # we retrieve file name using file path and append into playlist_list
    playlist_list.append(filepath)
    playlist_box.insert(END,filename)
    # print(playlist_list)

def browse_file():
    filename=filedialog.askopenfilename(filetypes=[("song file","*.mp3")])    #ask file path *.mp3 means only mp3 files are allowed
    addPlaylist(filename)    #function defined

def browse_directory():
    directorPath=filedialog.askdirectory()   #ask path of folder
    os.chdir(directorPath)      #change directory
    for file in os.listdir(directorPath):
        if(file.endswith(".mp3")):           #check if file name ends with mp3
            playlist_box.insert(END,file)    # if yes then insert it into playlist
            playlist_list.append(os.path.abspath(file))     # we retrieve file path using file path and append into playlist_list
    print(playlist_list)
# adding song to playlist end function

# play music function start

def playMusic(event):  
    global running,paused
    running=False
    sleep(1.5)
    running=True
    mixer.music.stop()    #it will stop the music which is already playing
    selected_song=playlist_box.curselection()  # the song which we select this will return tuple of  index
    selected_song=int(selected_song[0])   #we are selecting first element of tuple
    song_path=playlist_list[selected_song]  #retriving song path
    mixer.music.load(song_path)    # loading songpath
    mixer.music.play()  #playing song
    play_pause_but.config(image=pauseimage)   #change image of play/pause button
    paused=False
    show_details(song_path)

def show_details(song_path):   #this function get all details of song path
    
    tag=TinyTag.get(song_path,image=True)    #get details of song
    song_name.config(text=f"Song Name : {tag.title}")  #set title of song
    artist_name.config(text=f"Artist : {tag.artist}")  #set artist of song
    mins,seconds=divmod(tag.duration,60)   #duration of song is divided and modulo by 60
    mins,seconds=round(mins),round(seconds)  #rounding of mins and second
    timeformat="{:02d}:{:02d}".format(mins,seconds)  
    song_length.config(text=f"Song Lenght : {timeformat}")  #set time format
    end_time.config(text=timeformat)
    with open("photo.jpg","wb") as file:
        file.write(tag.get_image())       #converting binary data to image
    img=Image.open("photo.jpg")   
    img=img.resize((460,300),Image.ANTIALIAS)    
    image=ImageTk.PhotoImage(img)    
    imagelabel.config(image=image)
    imagelabel.image=image
    
    t1=threading.Thread(target=start_count,args=(tag.duration,))
    t1.start() 

# play music function end

#mute and unmute function start

def mute_unmute():
    global muted
    if(muted):
        mixer.music.set_volume(1)
        muted=False
        mute_unmute_but.config(image=unmuteimage)
    else:
        mixer.music.set_volume(0)
        muted=True
        mute_unmute_but.config(image=muteimage)

#mute and unmute function end

#play pause button starts

def play_pause_music():
    global paused
    if(paused):
        mixer.music.unpause()
        paused=False
        play_pause_but.config(image=pauseimage)   #changing image to pause
    else:
        mixer.music.pause()    
        paused=True
        play_pause_but.config(image=playimage)  #changing image to play
    

#play pause button end

#volume increase/decrease function starts

def set_vol(vol):
    volume=float(vol)/100   #vol value is in string changed to float and divided by 100 so value between 0 to 1
    mixer.music.set_volume(volume)


#volume increase/decrease function ends

#forward/backward fucntion starts

def next_song():
    global running,paused
    running=False
    sleep(1.5)
    running=True
    mixer.music.stop()    
    
    selected_song=playlist_box.curselection() #return tuple of indexes 
    selected_song=int(selected_song[0])+1
    if(selected_song==playlist_box.size()):
        selected_song=0
    playlist_box.selection_clear(0,END)    #selectd song is cleared
    playlist_box.selection_set(selected_song)   #selecting song
    song_path=playlist_list[selected_song]  
    mixer.music.load(song_path)    
    mixer.music.play()  
    play_pause_but.config(image=pauseimage)  
    paused=False
    show_details(song_path)

def prev_song():
    global running,paused
    running=False
    sleep(1.5)
    running=True
    mixer.music.stop()    
    
    selected_song=playlist_box.curselection()  
    selected_song=int(selected_song[0])
    if(selected_song>0):
        selected_song-=1
    playlist_box.selection_clear(0,END)    #selectd song is cleared
    playlist_box.selection_set(selected_song)   #selecting song
    song_path=playlist_list[selected_song]  
    mixer.music.load(song_path)    
    mixer.music.play()  
    play_pause_but.config(image=pauseimage)  
    paused=False
    show_details(song_path)
    

#forward/backward fucntion ends

#seek function starts

def start_count(t):

    global running,current_time
    time.config(to=t)   
    current_time=0
    # print(t)
    while(current_time<=t and running):
        if(not paused):    
            mins,seconds=divmod(current_time,60)   #duration of song is divided and modulo by 60
            mins,seconds=round(mins),round(seconds)  #rounding of mins and second
            timeformat="{:02d}:{:02d}".format(mins,seconds)
            curr_time.config(text=timeformat)
            time.set(current_time)
            sleep(1)
            current_time+=1
    # print(current_time)
    if(current_time==int(t)+1):
        next_song()

def change_pos(new_pos):
    global current_time
    new_pos=round(float(new_pos))  #
    if(current_time!=new_pos):
        current_time=new_pos      #updated current_time with new time
        mixer.music.rewind()      #rewind music
        mixer.music.set_pos(new_pos)   #set new position of song

#seek function ends


root=tk.ThemedTk()
root.get_themes()  #get all themes present
root.set_theme("breeze")   # theme for seek kebab
root.iconbitmap("music.ico")
root.title("PITCH PERFECT")

# root size
root.geometry("1000x700+200+40")
root.resizable(False,False)
# end


f1=Frame(root,bg="red",width=10,height=700)
f1.grid(row=0,column=0,sticky="nsew")

f2=Frame(root,bg="black",width=10,height=700)
f2.grid(row=0,column=1,sticky="nsew")

# playlist start
Label(f1,text="PLAYLIST",font=("algerian",25)).pack(pady=5)
playlist_box=Listbox(f1,selectmode=SINGLE)
playlist_box.pack(expand=True,fill=BOTH,pady=25,padx=24)
playlist_box.bind("<<ListboxSelect>>",playMusic)    #whenever we select anything in list box the function  will be called 
# playlist end

# IMAGE PART START

img=Image.open("black_background.png")
img=img.resize((460,300),Image.ANTIALIAS)   #image resiszed
cheap_img=ImageTk.PhotoImage(img)  
imagelabel=Label(f2,image=cheap_img,height=300,width=460)
imagelabel.image=cheap_img  #image set
imagelabel.place(x=75,y=50)   

# IMAGE PART END

#SEEK start

time=ttk.Scale(f2,from_=0,to=100,orient=HORIZONTAL,length=460,command=change_pos)
time.place(x=75,y=400)

#SEEK end

# seek labels start

curr_time=Label(f2,text="00:00",font=('ALGERIAN',10),bg="black",fg="white")
end_time=Label(f2,text="00:00",font=('ALGERIAN',10),bg="black",fg="white")
curr_time.place(x=20,y=400)
end_time.place(x=548,y=400)

# seek labels end

# buttons starts
# extracted images
playimage=PhotoImage(file="play-button.png")
pauseimage=PhotoImage(file="pause.png")
muteimage=PhotoImage(file="mute.png")
forwardimage=PhotoImage(file="forward.png")
backwardimage=PhotoImage(file="backward.png")
unmuteimage=PhotoImage(file="volume.png")

# image button made
play_pause_but=Button(f2,image=playimage,command=play_pause_music)
forward_but=Button(f2,image=forwardimage,command=next_song)
backward_but=Button(f2,image=backwardimage,command=prev_song)
mute_unmute_but=Button(f2,image=unmuteimage,command=mute_unmute)

# imgage button place

play_pause_but.place(x=270,y=450)
forward_but.place(x=370,y=450)
backward_but.place(x=170,y=450)
mute_unmute_but.place(x=550,y=480)

# buttons ends

# song name start

song_name=Label(f2,text="Song Name : ",font=('times new roman',12,"bold"),bg="black",fg="white")
song_name.place(x=35,y=550)
artist_name=Label(f2,text="Artist : ",font=('times new roman',12,"bold"),bg="black",fg="white")
artist_name.place(x=35,y=580)
song_length=Label(f2,text="Song Lenght : 00:00",font=('times new roman',12,"bold"),bg="black",fg="white")
song_length.place(x=35,y=610)
# song name end

# sound bar start

volume=ttk.Scale(f2,from_=0,to=100,orient=HORIZONTAL,length=300,command=set_vol)
volume.place(x=160,y=650)
volume.set(70)  #by default volume 70
mixer.music.set_volume(0.7)

# sound bar end

# menubar start

myMenu=Menu(root)
menu1=Menu(myMenu)
menu1.add_command(label="Open Song",command=browse_file)
menu1.add_command(label="Open Folder", command=browse_directory)
menu1.add_command(label="Exit",command=quit)

myMenu.add_cascade(label="File",menu=menu1)
root.config(menu=myMenu)


# menubar end


root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=3)
root.rowconfigure(0,weight=1)

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()