Theremin PI 2040 - 4 Layers Stacked

1. Reference Pitch - 6 options

Where does A live? ref_off = 12_log2(ref/440)

Baroque A 415Hz = -101c

Verdi A 432Hz = -32c

French A 435Hz = -20c

Modern A 440Hz = 0c

Euro A 442Hz = +8c

Love A 528Hz = +320c

2. Key / Root - 12 options

C, C#, D, D#, E, F, F#, G, G#, A, A#, B

Transposes the scale pattern. Pentatonic in C vs Pentatonic in F# = same shape, different notes.

3. Temperament - 7 options

How pure is each interval? -29 to +34 cents:

Off / Equal - modern piano

Just - pure thirds

Pythagorean - pure fifths, bright

Meantone - Renaissance mellow

Werckmeister 3 - Bach, key color

19 Tone Equal - microtonal

4. Scale - 11 options

Which notes survive in 2-oct field 48-72:

Off - continuous gliss, infinite

Chromatic - 12 notes, 24 spots

Major / Minor - 7 notes, 14 spots

Whole Tone - 6 notes, 12 spots

Blues - 6 notes, 12 spots

Pentatonic - 5 notes, 10 spots

Pelog - Javanese, 10 spots

Slendro - Indonesian, 10 spots

Hirajoshi - Japanese, 10 spots

Bhairav - Indian, 14 spots

Octave - 10 positions

-4 to +5 = freq _ 2^oct

Math:

12 keys x 11 scales x 7 temps x 6 refs = 5,544 tunings

5,544 x 10 oct = 55,440 distinct ranges

Off+Off = infinite

Range: OCT -4 = 15Hz to OCT +5 = 20kHz (wide amp)

So: REF = center, KEY = root, TEMP = tuning, SCALE = filter, OCT = window.

Use the smpGenerator to make some random samples. Run in the Thonny shell once.

# K0=SIN K1=SQU K2=SAW K3=TRI


# K4=SMP1 K5=SMP2 K6=SMP3 K7=SMP4  -> /smp/smp1.raw .. smp4.raw

# K8=ref K9=root/transpose K10=temp K11=scale K12=oct+ K13=lvl K15=oct-

# HOW TO MAKE SAMPLES (Audacity):

# 1. Trim to 0.5 sec (8000 samples @16k)

# 2. Mono, Project Rate 16000

# 3. Effect > Fade In 5ms at start, Fade Out 5ms at end for loop

# 4. Export Other uncompressed -> RAW Signed 16-bit PCM -> smp1.raw etc

# 5. Or WAV 16-bit mono 16k - code strips header

# 6. In Thonny: View > Files, make /smp on Pico, drag files in












