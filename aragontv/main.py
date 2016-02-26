# -*- coding: UTF-8 -*-.
import threading, os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '300')

class Paso1(Screen):
    pass

class Paso2(Screen):
    pass

class Paso3(Screen):
    pass

class DescargarApp(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.paso1 = Paso1(name='Paso 1')
        self.paso2 = Paso2(name='Paso 2')
        self.paso3 = Paso3(name='Paso 3')
        self.screen_manager.add_widget(self.paso1)
        self.screen_manager.add_widget(self.paso2)
        self.screen_manager.add_widget(self.paso3)
        return self.screen_manager

    def url_ready(self,page_url):
        print "url_ready"

        self.paso1.page_url = page_url
        print self.paso1.page_url

        from core.item import Item
        item = Item(url=self.paso1.page_url)

        from channels import aragontv
        item = aragontv.detalle_episodio(item)
        print item.title
        print item.plot

        self.screen_manager.current = self.screen_manager.next()

        self.paso2.description = "[b]"+item.title+"[/b]\n"+item.plot

    def start_download(self):
        print "start_download"

        from servers import aragontv
        video_urls = aragontv.get_video_url(self.paso1.page_url)
        print video_urls

        media_url = video_urls[0][1]
        print media_url

        self.paso3.resultado = "Descargando "+media_url+"\n\n"

        self.screen_manager.current = self.screen_manager.next()

        # Start download in background
        exe = ['rtmpdump/darwin/rtmpdump','-r',media_url,'-o','out.mp4']
        self.download_thread = DownloadThread(exe,self.paso3)
        self.download_thread.start()

        Clock.schedule_interval(self.check_output_size, 0.5)

    def abort_download(self):
        print "abort_download"

        self.download_thread.abort()
        self.screen_manager.current = self.screen_manager.previous()

    def check_output_size(self,value):
        #print "check_output_size"

        if os.path.exists("out.mp4"):
            statinfo = os.stat('out.mp4')
            self.paso3.tamanyo = human_size(statinfo.st_size)

    def on_stop(self):
        print "on_stop!"
        self.download_thread.abort()

#http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def human_size(num,suffix="B"):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

# Download in background
class DownloadThread(threading.Thread):

    def __init__(self, exe, pantalla):
        print "DownloadThread.__init__ "+repr(exe)
        self.exe = exe
        self.pantalla = pantalla

        threading.Thread.__init__(self)

    def run(self):
        print "DownloadThread.run"

        import subprocess
        self.p = subprocess.Popen(self.exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while(True):
            retcode = self.p.poll() #returns None while subprocess is running
            line = self.p.stdout.readline()
            self.pantalla.resultado = self.pantalla.resultado + line
            
            if(retcode is not None):
                break

    def abort(self):
        print "DownloadThread.abort"
        self.p.kill()

if __name__ == '__main__':
    DescargarApp().run()
