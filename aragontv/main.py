# -*- coding: UTF-8 -*-.
import threading, os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock

from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '350')

class Paso1(Screen):
    pass

class Paso2(Screen):
    pass

class Paso3(Screen):
    pass

class MessageDialog(BoxLayout):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class DescargarApp(App):

    # Desactiva el cuadro de configuración genérico de Kivy
    use_kivy_settings = False

    def build(self):
        self.download_thread = None

        self.store = JsonStore("descargar-aragontv.json")

        if not self.store.exists("target_folder"):
            self.store.put("target_folder",value=os.path.expanduser("~"))

        self.screen_manager = ScreenManager(transition=FadeTransition())
        
        self.paso1 = Paso1(name='Paso 1')
        self.paso1.ids.target_folder.text = self.store.get("target_folder")["value"]

        self.paso2 = Paso2(name='Paso 2')
        self.paso3 = Paso3(name='Paso 3')
        self.screen_manager.add_widget(self.paso1)
        self.screen_manager.add_widget(self.paso2)
        self.screen_manager.add_widget(self.paso3)
        return self.screen_manager

    def dismiss_popup(self):
        self._popup.dismiss()

    def target_selected(self, path, filename):
        self._popup.dismiss()
        self.paso1.ids.target_folder.text = path

    def target_selection(self):
        content = LoadDialog(load=self.target_selected, cancel=self.dismiss_popup)
        content.ids.filechooser.path = self.paso1.ids.target_folder.text
        self._popup = Popup(title="Elige destino", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def message(self,title,body):

        content = MessageDialog()
        content.ids.message_body.text = body
        self._popup = Popup(title=title, content=content, size_hint=(0.8, 0.8))
        self._popup.open()

    def url_ready(self,page_url):
        print "url_ready"

        print self.paso1.ids.page_url.text

        if not self.paso1.ids.page_url.text.startswith("http://") and not self.paso1.ids.page_url.text.startswith("https://"):
            self.message("Hay un problema...","La URL que has introducido no es válida")
            return

        from core.item import Item
        item = Item(url=self.paso1.ids.page_url.text)

        from channels import aragontv
        item = aragontv.detalle_episodio(item)
        print item.title
        print item.plot

        self.video_title = item.title
        self.media_url = item.media_url

        if self.media_url=="":
            self.message("Hay un problema...","No se puede encontrar un vídeo en esa URL")
            return

        self.store.put("target_folder",value=self.paso1.ids.target_folder.text)

        self.screen_manager.current = self.screen_manager.next()

        self.paso2.ids.description.text = "[b]"+item.title+"[/b]\n"+item.plot

    def start_download(self):
        print "start_download"

        self.paso3.resultado = "Descargando "+self.media_url+"\n\n"

        self.screen_manager.current = self.screen_manager.next()

        # Start download in background
        from core import downloadtools
        clean_file_name = downloadtools.limpia_nombre_caracteres_especiales(self.video_title)+".mp4"

        self.target_file = os.path.join( self.paso1.ids.target_folder.text , clean_file_name )

        exe = ['rtmpdump/darwin/rtmpdump','-r',self.media_url,'-o',self.target_file]
        self.download_thread = DownloadThread(exe,self.paso3)
        self.download_thread.start()

        Clock.schedule_interval(self.check_output_size, 0.5)

    def abort_download(self):
        print "abort_download"

        self.download_thread.abort()
        self.screen_manager.current = self.screen_manager.previous()

    def check_output_size(self,value):
        #print "check_output_size"

        if os.path.exists(self.target_file):
            statinfo = os.stat(self.target_file)
            self.paso3.tamanyo = human_size(statinfo.st_size)

    def on_stop(self):
        print "on_stop!"

        if self.download_thread is not None:
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
        self.running = False

        threading.Thread.__init__(self)

    def run(self):
        print "DownloadThread.run"

        import subprocess
        self.p = subprocess.Popen(self.exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.running = True
        while(True):
            retcode = self.p.poll() #returns None while subprocess is running
            line = self.p.stdout.readline()
            self.pantalla.resultado = self.pantalla.resultado + line
            
            if(retcode is not None):
                break

        self.running = False
        app = App.get_running_app()
        app.message("Proceso concluido","Ya tienes el fichero descargado en "+app.target_file)
        #App.get_running_app().stop()

    def abort(self):
        print "DownloadThread.abort"
        
        if self.running:
            self.p.kill()

Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    DescargarApp().run()
