
import instaloader

ig=instaloader.Instaloader()

user = input("ENter your username = ")

ig.download_profile(user,profile_pic_only = True)

