#!/usr/bin/python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.garden.iconfonts import *
from os.path import dirname, join
import os

class PlayerWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_position(self, inst):
        if inst.value > round(self.ids.cur_vid.position/60,2) or inst.value < round(self.ids.cur_vid.position/60,2):
            seek = ((inst.value/inst.max)*100)/100
            self.ids.cur_vid.seek(seek)

    def play_pause(self):
        vid = self.ids.cur_vid
        if vid.state == 'play':
            vid.state = 'pause'
        else:
            vid.state = 'play'

    def play_file(self, filepath):
        vid = self.ids.cur_vid
        if filepath.endswith('.mp4') or filepath.endswith('.mkv'):
            vid.state = 'stop'
            vid.source = filepath
            vid.state = 'play'
        self.ids.pages.page = 0
        container = self.ids.list_container
        name = filepath[filepath.rfind('/')+1:]
        real_path = filepath
        if len(name) > 30:
            name = name[:20]+'...'+name[-8:]
            filepath = filepath[:20]+'...'+filepath[-14:]
        duplicate = 0
        for d in container.data:
            if real_path == d['real_path']:
                duplicate = 1
        if duplicate == 0:
            container.data.insert(0,{'vid_name':name,'vid_path':filepath,'real_path':real_path,'height':50})

    def play_folder(self, filepath):
        vid = self.ids.cur_vid
        files = os.listdir(filepath)
        videos = []
        for f in files:
            if f.endswith('.mp4') or f.endswith('.mkv'):
                video = '/'.join([filepath,f])
                videos.append(video)
        # print(videos
        vid.source = videos[0]
        vid.state = 'play'

        container = self.ids.list_container
        for v in videos:
            name = v[v.rfind('/')+1:]
            real_path = v
            if len(name) > 30:
                name = name[:20]+'...'+name[-8:]
                v = v[:20]+'...'+v[-14:]
            container.data.insert(0,{'vid_name':name,'vid_path':v,'real_path':real_path,'height':50})
        self.ids.pages.page = 0

    def play_next(self):
        vid = self.ids.cur_vid
        cur_video = vid.source
        container = self.ids.list_container
        cur_idx = 0
        last_idx = len(container.data)-1
        for i,d in enumerate(container.data):
            if cur_video == d['real_path']:
                cur_idx = i
        if cur_idx != last_idx:
            next_vid = container.data[cur_idx+1]['real_path']
            self.play_file(next_vid)
        else:
            next_vid = container.data[0]['real_path']
            self.play_file(next_vid)
    
    def play_prev(self):
        vid = self.ids.cur_vid
        cur_video = vid.source
        container = self.ids.list_container
        cur_idx = 0
        last_idx = len(container.data)-1
        for i,d in enumerate(container.data):
            if cur_video == d['real_path']:
                cur_idx = i
        if cur_idx != 0:
            prev_vid = container.data[cur_idx-1]['real_path']
            self.play_file(prev_vid)
        else:
            prev_vid = container.data[last_idx]['real_path']
            self.play_file(prev_vid)

    

class PlayerApp(App):
    def build(self):

        return PlayerWindow()

if __name__=='__main__':
    register('flat_icons',join(dirname(__file__),'assets/fonts/Material-Design-Iconic-Font.ttf'),'assets/fonts/zmd.fontd')
    PlayerApp().run()
