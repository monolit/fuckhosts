# requires: yt-dlp Pillow cryptg wget
import os, wget
from .. import loader, utils
from telethon.tl.types import DocumentAttributeAudio
from telethon import events
from telethon.tl.types import Message, Channel
from yt_dlp import YoutubeDL
from PIL import Image

@loader.tds
class YTDLMod(loader.Module):
	"""media downlod module with yt-dlp
	usage:
	.ytv +- thumb + reply
	.ytv url +- thumb
	same with yta"""
	strings = {
		"name": "YTDL"}
	def __init__(self):
		self.name = self.strings['name']
	async def client_ready(self, client, db):
		self.client = client
		self.db = db

	async def ytvcmd(self, message):
		""".ytv - dowmload video media"""
		args=utils.get_args(message)
		reply=await message.get_reply_message()
		await ses(self, message, args, reply, '')

	async def ytacmd(self, message):
		""".ytv - dowmload audio media"""
		args=utils.get_args(message)
		reply=await message.get_reply_message()
		await ses(self, message, args, reply, 'a')

async def ses(self, message, args, reply, type_):
	opts={
		'embed-thumbnail': True,
		'postprocessors':[
		#{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
		{'key': 'SponsorBlock'},
		{'key': 'ModifyChapters',
		'remove_sponsor_segments':[
		'sponsor', 'intro', 'outro', 'interaction', 'selfpromo', 'preview', 'music_offtopic']}],
		#'no-check-certificate': True, 'writethumbnail': True,
		'prefer_ffmpeg': True,
		'geo_bypass': True,
		'outtmpl': '%(title)s.%(ext)s',
		'add-metadata': True}
	text=reply.message if reply else None
	if args:
		if 'thumb' in args:thumb_=True
		else:thumb_=False
		if uri:=args[0]:
			if 'http' in uri:pass
			else:uri=text
	else:
		thumb_=False
		uri=text
	await message.edit("loading")

	if type_=='a':
		try:
			opts.update({'format':'ba[ext^=m4a]'})
			a, nama=await gget(uri,opts)
		except Exception as e:
			print(e)
			opts['format']='best[ext^=mp4][height<1400]'	#opts['format']='ba[ext^=mp3]'
			opts['postprocessors'].append({'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'})
			a, nama=await gget(uri,opts)

		nama=''.join(nama.split('.')[:-1])+'.m4a'
		_ = a['uploader'] if 'uploader' in a else 'umknown'

		th, thumb=await get_thumb(a, message)
		if thumb_:await self.client.send_file(message.to_id, th, force_document=False)

		await self.client.send_file(
			message.to_id,
			nama,
			supports_streaming=True,
			reply_to=reply.id if reply else None,
			thumb=th,
			attributes=[
			DocumentAttributeAudio(duration=int(a['duration']),
				title=str(a['title']),
				performer=_)],
			caption=await readable(a, type_))

	else:
		try:
			opts.update({'format': 'bestvideo[ext^=mp4][height<1400][fps>30]+ba[ext^=m4a]'})
			a, nama=await gget(uri,opts)
		except Exception as e:
			print(e)
			opts['format']='best[ext^=mp4][height<1400]'
			a, nama=await gget(uri,opts)

		th, thumb=await get_thumb(a, message)
		if thumb_:await self.client.send_file(message.to_id, th, force_document=False)

		await self.client.send_file(
			message.to_id,
			nama,
			thumb=th,
			force_document=False,
			reply_to=reply.id if reply else None,
			supports_streaming=True,
			caption=await readable(a, type_))

	[os.remove(i) for i in [nama, th, thumb]]
	await message.delete()

async def gget(uri, opts):
	import yt_dlp.utils
	yt_dlp.utils.std_headers['User-Agent'] ='" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"'
	with YoutubeDL(opts) as ydl:
		a=ydl.extract_info(uri, download=True)
		nama=ydl.prepare_filename(a)
	return a, nama
async def get_thumb(a, m):
	thumb=a['thumbnails'][-1]['url']
	thumb_=wget.download(thumb)
	th=f"{a['id']}.jpg"
	Image.open(thumb_).save(th, quality=100)
	await m.edit('uplowing')
	return th, thumb_
async def readable(a, type_):
	_=f"""<a href={a['original_url']}>{a['title']}</a>
ext:{a['ext']} """

	if type_=='a':_+=f"""bitrate:{a['abr']}Kb """
	else:
		try:fps=a['fps']
		except:fps=None
		_+=f"res:{a['format']}"
		_+=f"fps:{fps}" if fps else ''
	return _
