
from sys import path
import os
from .models import NextPath, Path, StorageHandler
class PathDataDialog(object):
	DEFAULT_PATH = "/"
	SENTINAL_PATH = "$PATH"
	SENTINAL_OPEN_PATH = "$OPEN_PATH"
	def __init__(self) -> None:
		self.show = False
		self.path = self.DEFAULT_PATH

	def displayPath(self)  -> None:
		print("[$Path]: {}".format(self.path))

	def showDialog(self) -> bool:
		return self.show

