#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

#You should install mido to run this program
#pip(3) install mido

import argparse
import mido

MIDI_INSTRUMENTS = [
    #Piano:0 ~ 7
    "Acoustic Grand Piano",
    "Bright Acoustic Piano",
    "Electric Grand Piano",
    " Honky-tonk Piano",
    " Electric Piano 1",
    " Electric Piano 2",
    " Harpsichord",
    " Clavinet",

    #Chromatic Percussion: 8 ~ 15
    "Celesta",
    "Glockenspiel",
    "Music Box",
    "Vibraphone",
    "Marimba",
    "Xylophone",
    "Tubular Bells",
    "Dulcimer",

    #Organ: 16 ~ 23
    "Drawbar Organ",
    "Percussive Organ",
    "Rock Organ",
    "Church Organ",
    "Reed Organ",
    "Accordion",
    "Harmonica",
    "Tango Accordion",

    #Guitar: 24 ~ 31
    "Acoustic Guitar (nylon)",
    "Acoustic Guitar (steel)",
    "Electric Guitar (jazz)",
    "Electric Guitar (clean)",
    "Electric Guitar (muted)",
    "Overdriven Guitar",
    "Distortion Guitar",
    "Guitar harmonics",

    #Bass: 32 ~ 39
    "Acoustic Bass",
    "Electric Bass (finger)",
    "Electric Bass (pick)",
    "Fretless Bass",
    "Slap Bass 1",
    "Slap Bass 2",
    "Synth Bass 1",
    "Synth Bass 2",

    #Strings: 40 ~ 47
    "Violin",
    "Viola",
    "Cello",
    "Contrabass",
    "Tremolo Strings",
    "Pizzicato Strings",
    "Orchestral Harp",
    "Timpani",

    #Strings (continued):
    "String Ensemble 1",
    "String Ensemble 2",
    "Synth Strings 1",
    "Synth Strings 2",
    "Choir Aahs",
    "Voice Oohs",
    "Synth Voice",
    "Orchestra Hit",

    #Brass:
    "Trumpet",
    "Trombone",
    "Tuba",
    "Muted Trumpet",
    "French Horn",
    "Brass Section",
    "Synth Brass 1",
    "Synth Brass 2",

    #Reed:
    "Soprano Sax",
    "Alto Sax",
    "Tenor Sax",
    "Baritone Sax",
    "Oboe",
    "English Horn",
    "Bassoon",
    "Clarinet",

    #Pipe:
    "Piccolo",
    "Flute",
    "Recorder",
    "Pan Flute",
    "Blown Bottle",
    "Shakuhachi",
    "Whistle",
    "Ocarina",

    #Synth Lead:
    "Lead 1 (square)",
    "Lead 2 (sawtooth)",
    "Lead 3 (calliope)",
    "Lead 4 (chiff)",
    "Lead 5 (charang)",
    "Lead 6 (voice)",
    "Lead 7 (fifths)",
    "Lead 8 (bass + lead)",

    #Synth Pad:
    "Pad 1 (new age)",
    "Pad 2 (warm)",
    "Pad 3 (polysynth)",
    "Pad 4 (choir)",
    "Pad 5 (bowed)",
    "Pad 6 (metallic)",
    "Pad 7 (halo)",
    "Pad 8 (sweep)",

    #Synth Effects:
    "FX 1 (rain)",
    "FX 2 (soundtrack)",
    "FX 3 (crystal)",
    "FX 4 (atmosphere)",
    "FX 5 (brightness)",
    "FX 6 (goblins)",
    "FX 7 (echoes)",
    "FX 8 (sci-fi)",

    #Ethnic:
    "Sitar",
    "Banjo",
    "Shamisen",
    "Koto",
    "Kalimba",
    "Bag pipe",
    "Fiddle",
    "Shanai",

    #Percussive:
    "Tinkle Bell",
    "Agogo",
    "Steel Drums",
    "Woodblock",
    "Taiko Drum",
    "Melodic Tom",
    "Synth Drum",

    #Sound effects:
    "Reverse Cymbal",
    "Guitar Fret Noise",
    "Breath Noise",
    "Seashore",
    "Bird Tweet",
    "Telephone Ring",
    "Helicopter",
    "Applause",
    "Gunshot"]

g_channels = []
parser = argparse.ArgumentParser(description='midi file information')
parser.add_argument("--file", required = True, help="midi filename to parce")
args = parser.parse_args()

mid = mido.MidiFile(args.file)


def get_instrument(program):
    return  MIDI_INSTRUMENTS[program]

class Instrument:
    def __init__(self, name):
        self.name = name
        self.notes_on = 0    
        self.notes_off = 0    
        self.control_change = 0    
        self.program_change = 0    

class Channel:
    def __init__(self, id):
        self.id = id
        self.instruments = []    
    def last_instrument(self):
        cnt_instrument = len(self.instruments)
        if cnt_instrument == 0:
            return None
        return self.instruments[cnt_instrument - 1]    
    def add_instrument(self, name):
        inst = Instrument(name)
        self.instruments.append(inst)
        return inst

    def add_count(self, msg):  
        #Add instrument anyway.
        if(msg.type == 'program_change'):  
            instrument = get_instrument(msg.program)
            myinst = self.add_instrument(instrument)
            myinst.program_change += 1
        elif(msg.type == 'control_change'):
            myinst = self.last_instrument()
            if not myinst:
                print('ERROR no instrument for %s'%msg.type)
            else:            
                myinst.control_change += 1
        elif(msg.type == 'note_on'):
            myinst = self.last_instrument()
            if not myinst:
                print('ERROR no instrument for %s'%msg.type)        
            else:    
                myinst.notes_on += 1
        elif(msg.type == 'note_off'):
            myinst = self.last_instrument()
            if not myinst:
                print('ERROR no instrument for %s'%msg.type)        
            else:    
                myinst.notes_off += 1


def get_channel_obj(id):
    for ch in g_channels:
        if ch.id == id:
            return ch
    return None

def create_channel_obj(id):
    if not get_channel_obj(id):
        ch = Channel(id)
        g_channels.append(ch) 
        return ch
    return None

def get_or_create_channel_obj(id):
    ch = get_channel_obj(id)
    if not ch:
        ch = create_channel_obj(id)
    return ch    


#parcing 
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        #print(msg)
        if hasattr(msg, 'channel'):
            ch = get_or_create_channel_obj(msg.channel)
            ch.add_count(msg)

#Reporting 
for ch in g_channels:
    print('===== channel[%d] ====='%ch.id)
    sum = 0
    for inst in ch.instruments:
        s = inst.notes_on + inst.notes_off + inst.control_change + inst.program_change
        sum += s
        print('  instrument[%-17s] note_in[%4d] note_off[%4d] control_change[%4d] program_change[%4d]'%(inst.name, inst.notes_on , inst.notes_off, inst.control_change, inst.program_change))
    print('Total event :[%d]'%sum)
        
print('===============================================')
