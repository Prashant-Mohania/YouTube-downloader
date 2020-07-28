from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar
from kivy.lang import Builder
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.snackbar import Snackbar
import sys, threading, time
from pytube import YouTube

#from kivymd.toast import toast

kv = '''
BoxLayout:
	url: url
	orientation: 'vertical'
			
	MDToolbar:
		id: toolbar
		title: 'YouTube Downloader'
		elevation: 10
		md_bg_color: 1, 0, 0, 1
		#right_action_items: [['download', lambda x: app.show_toast("Download")]]
	GridLayout:
		cols:1
		pos: 200, 200
		size: 100, 100
		padding: 20
		spacing: 10
		
		MDLabel:
			text: "YouTube Downloader"
			halign: 'center'
		
		TextInput:
			id: url
			hint_text: "enter url"
			multiline: False
			halign: 'center'
			size_hint: .2, .2
		
		MDRoundFlatButton:
			id: btn
			text: "Select Resolution"
			on_release: app.show_snackbar("Please enter URL") if url.text ==" " else app.new_thread(url.text)
			
		MDSpinner:
			id: spnr
			size_hint: None, None
			size: dp(46), dp(46)
		#	pos_hint: {"x": 0, "y": 1}
			active: False
	
		MDProgressBar:
			id: prgsbr
			value: 0
		
		MDLabel:
			id: dl
			text: ""
			halign: 'center'
'''

file_size = 0

class Main(MDApp):
	def build(self):
		return Builder.load_string(kv)
	
	def new_thread(self, url):
		thread = threading.Thread(self.select_res(url))
		thread.start()
	
	def show_snackbar(self, instance):
		Snackbar(text=instance).show()
		
	def progress_check(self, stream, chunk, bytes_remaining):
		self.root.ids.spnr.active = False
		percent = ((fileSize - bytes_remaining)/fileSize)*100
		self.root.ids.btn.text = f"{percent:0.00f} % Downloading"
		self.root.ids.prgsbr.value = int(percent)
		self.root.ids.dl.text = f"{percent:0.00f} Download"
	
	def download_complete(self, stream, file_path):
		Snackbar(text="Dowloading Complete")
		time.sleep(5)
		self.root.ids.btn.text = "Select Resolution"
		self.root.ids.prgsbr.value = 0
		
	def select_res(self , instance):
		try:
			self.root.ids.spnr.active = True
			self.v_yt = YouTube(instance)
			self.v_yt.register_on_progress_callback(self.progress_check)
			self.v_yt.register_on_complete_callback(self.download_complete)
			self.bottomsheet = MDListBottomSheet()
		
			try:
				self.r144 = self.v_yt.streams.filter(file_extension='mp4', res='144p', progressive=True).all()
				self.bottomsheet.add_item(f"144p            {self.r144[0].filesize:.2f} MB", lambda x: self.Download(self.r144))
				
			except:
				self.bottomsheet.add_item(f"144p            Unavailable", lambda x: sys.exit())
				
			try:
				self.r240 = self.v_yt.streams.filter(file_extension='mp4', res='240p', progressive=True).all()
				self.bottomsheet.add_item(f"240p            {self.r240[0].filesize:.2f} MB", lambda x: self.Download(self.r240))
				
			except:
				self.bottomsheet.add_item(f"240p            Unavailable", lambda x: sys.exit())

			try:
				self.r360 = self.v_yt.streams.filter(file_extension='mp4', res='360p', progressive=True).all()
				self.bottomsheet.add_item(f"360p            {self.r360[0].filesize/1000000:.2f} MB", lambda x: self.Download(self.r360))
				
			except:
				self.bottomsheet.add_item(f"360p            Unavailable", lambda x: sys.exit())

			try:
				self.r480 = self.v_yt.streams.filter(file_extension='mp4', res='480p', progressive=True).all()
				self.bottomsheet.add_item(f"480p            {self.r480[0].filesize:.2f} MB", lambda x: self.Download(self.r480))
				
			except:
				self.bottomsheet.add_item(f"480p            Unavailable", lambda x: sys.exit())

			try:
				self.r720 = self.v_yt.streams.filter(file_extension='mp4', res='720p', progressive=True).all()
				self.bottomsheet.add_item(f"720p            {self.r720[0].filesize:.2f} MB", lambda x: self.Download(self.r720))
				
			except:
				self.bottomsheet.add_item(f"720p            Unavailable", lambda x: sys.exit())

			self.bottomsheet.open()
		
		except:
			self.show_snackbar("Connect to the Internet")
			self.root.ids.spnr.active = False
			
			
	def Download(self, instance):
		global fileSize
		fileSize = instance[0].filesize
		self.show_snackbar("Downloading Start")
		instance[0].download(r"\sdcard")

if __name__ == "__main__":
	Main().run()