from mutagen.easyid3 import EasyID3

# audio=EasyID3("Taylor Swift  I Knew You Were Trouble.mp3")     #easyid3 used to change mp3 file details
# audio["title"]="I Knew You Were Trouble"
# audio["artist"]="Taylor Swift"
# audio.save()

# from tinytag import TinyTag
# tag=TinyTag.get("Cheap Thrills - Pitch Perfect 3 (Lyrics) (320  kbps).mp3",image=True)
# # print(tag.title)
# with open("hello.jpg","wb") as f:
#     f.write(tag.get_image())

# import eyed3 
# file=eyed3.load("Taylor Swift  I Knew You Were Trouble.mp3")  #image load
# file.initTag()  #  initialize tags
# file.tag.images.set(3,open("i knew trouble photo.jpg","rb").read(),"image/jpeg")  #changing image
# file.tag.save(version=eyed3.id3.ID3_V2_3) #encoding image