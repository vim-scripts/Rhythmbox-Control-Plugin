#!/usr/bin/env python

## xchatrb.py for VIM
## (c) 2004 JinHyung Park <jinhyung@gmail.com>

## Implements command /psong, which prints the currently playing song
## in RhythmBox.
## (c) 2003 Gustavo J. A. M. Carneiro <gjc@inescporto.pt>
## 	    G-LiTe / <stephan@wilkogazu.nl>

## REQUIRES: gnome-python >= 2.0
##           Rhythmbox >= 0.5.3 (>= 0.5.99 recommended)

## WARNING: before trying this plugin, and if xchat <= 2.0.5, install
## the xchat python interface replacement:
## 	http://yang.inescn.pt/~gjc/pyxchat-0.1.tar.bz2
## Alternatively, wait for xchat 2.0.6 to be released.

## Changes in version 0.5.1:
##	- Remove .mp3 or .ogg suffix from song title (G-LiTe)

## Changes in version 0.5:
##	- Make it work with recent CVS build of Rhythmbox, including
##	  more info (Gustavo, G-LiTe)

## Changes in version 0.4:
##	- Code cleanup (Gustavo)
##      - Added missing import string (Gustavo)
##      - Make psong a subcommand of /rb (Gustavo)
##      - Added /rb prev|next|play to change and pause song (Gustavo)

## Changes in version 0.3:
##      - Prettier song display, using bold text (G-LiTe)
##      - Print song length next to the title, when using CVS Rhythmbox (G-LiTe)
##      - Detect when RB isn't playing anything, when using CVS Rhythmbox (G-LiTe)
##      - Make G-LiTe's changes not break with RB 0.5.3 (Gustavo)

import pygtk; pygtk.require("2.0")
import CORBA
import bonobo.activation
import string
import sys

__module_name__        = "xchatrbforVIM"
__module_version__     = "0.5.1"
__module_description__ = "Show song playing in rhythmbox"

# missing consts from the typelib
_ACTIVATION_FLAG_NO_LOCAL = 1<<0;      # No shared libraries
_ACTIVATION_FLAG_PRIVATE = 1<<1;       # start a new server and don't register it
_ACTIVATION_FLAG_EXISTING_ONLY = 1<<2; # don't start the server if not started


_rhythmbox = None
def get_rhythmbox():
    global _rhythmbox

    def get_new(): return bonobo.activation.activate(
	"repo_ids.has('IDL:GNOME/Rhythmbox:1.0')",
	[], _ACTIVATION_FLAG_EXISTING_ONLY)

    if _rhythmbox is None:
	_rhythmbox = get_new()
    else:
	# Check if the cached reference points to a server that is
	# still alive, otherwise ask bonobo-activation for a new fresh
	# reference.
	try:
	    # basically this means: _rhythmbox.ping()
	    _rhythmbox.ref()
	    _rhythmbox.unref()
	except CORBA.COMM_FAILURE:
	    _rhythmbox = get_new()
    return _rhythmbox

def psong(word):
    rb = get_rhythmbox()
    if rb is None:
	print "Rhythmbox is not running"
	return
    
    outlist = []
    try:
	outlist.append(rb.getPlayingTitle())
	duration = None
    except AttributeError:
	pb = rb.getPlayerProperties()
	info = pb.getValue("song").value()
	pb.unref()
	if info is None:
	    print "Rhythmbox is not playing anything"
	    return
	if info.artist:
	    outlist.append(info.artist)
	if info.album:
	    outlist.append(info.album)
	if info.track_number != -1:
	    tracknumber = "%i." % info.track_number
	else:
	    tracknumber = ""
	if info.title:
	    title = info.title
	    if title.endswith('.mp3') or title.endswith('.ogg'):
		title = title[:-4]
	    outlist.append(' '.join((tracknumber, title)))
	duration = info.duration

    if duration is None:
	try:
	    duration = rb.getPlayingSongDuration()
	except AttributeError:
	    pass

    if duration is None or duration == 0:
	duration_str = ""
    else:
	if duration == -1:
	    print "Rhythmbox is not playing anything"
	    return
	else:
	    hours    = duration // 3600
	    duration = duration % 3600
	    minutes  = duration // 60
	    duration = duration % 60
	    duration_str = str(minutes) + ":" + str(duration).zfill(2)
	    if hours == 0:
		duration_str = '%s:%s' % (str(minutes), str(duration).zfill(2))
	    else:
		duration_str = '%s:%s:%s' % (str(hours), str(minutes).zfill(2),
					     str(duration).zfill(2))

    print "Rhythmbox is playing -< %s (%s) >-" % \
                (' - '.join(outlist), duration_str)

def rb_next(word):
    rb = get_rhythmbox()
    if rb is None:
	print "Rhythmbox is not running"
	return
    try:
	rb.next()
	psong(word[1:])
    except AttributeError():
	print "Your Rhythmbox version doesn't support this operation"

def rb_prev(word):
    rb = get_rhythmbox()
    if rb is None:
        print "Rhythmbox is not running"
    return

    try:
        rb.previous()
        psong(word[1:])
    except AttributeError():
        print "Your Rhythmbox version doesn't support this operation"

def rb_play(word):
    rb = get_rhythmbox()
    if rb is None:
	print "Rhythmbox is not running"
	return

    try:
	rb.playPause()
    except AttributeError():
	print "Your Rhythmbox version doesn't support this operation"
    return

def rb_command_cb(word):
    if word[1].lower() == 'psong':
        return psong(word[1:])
    if word[1].lower() == 'next':
        return rb_next(word[1:])
    if word[1].lower() == 'prev':
        return rb_prev(word[1:])
    if word[1].lower() == 'play':
        return rb_play(word[1:])
    return

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    rb_command_cb(sys.argv)
# EOF
# vim:ts=4:sw=4:sts=4:et
