import sublime, sublime_plugin
import functools, inspect, os, sys

settings = sublime.load_settings('LaTeXing.sublime-settings')

def debug(s = "", details = 0):
	if details <= 1:
		sublime.set_timeout(functools.partial(do_debug, ("{1}:{2} {3} ".format(*inspect.stack()[1]) if len(inspect.stack()) > 1 else " ") + s), 0)
	
def do_debug(s):
	if settings.get("debug", False):
		print "debug:", s

from latexing.bibsonomy import BibsonomyImportCommand
from latexing.clean import CleanCommand
from latexing.check_system import CheckSystemCommand
from latexing.compiler import CompilerCommand
from latexing.completions import CompletionsListener
from latexing.fill import FillAnywhereCommand, FillCommand
from latexing.menu import BuyLicenseCommand, LtxOpenDocumentationCommand
from latexing.online_lookup import OnlineLookupCommand
from latexing.open import OpenCommand
from latexing.listener import OnLoadListener, OnPostSaveListener
from latexing.settings import TogglePreferencesCommand, OpenDocumentationCommand
from latexing.viewer import JumpToPdfCommand, OpenPdfCommand
from latexing.texcount import TexcountCommand