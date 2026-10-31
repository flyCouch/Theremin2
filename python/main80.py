# v4.2h2 - YOUR v4.2h EXACT + K0=sin K1=squ K2=saw K3=tri
import time, math
from machine import Pin, ADC, I2C, PWM
PITCH_CURVE = 0.65
PIN_AUDIO=6
PIN_RST=15
rst=Pin(PIN_RST, Pin.OUT)
rst.value(0)
time.sleep_ms(250)
rst.value(1)
time.sleep_ms(400)
pwm=PWM(Pin(PIN_AUDIO))
pwm.freq(440)
pwm.duty_u16(0)
i2cR=I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
from ssd1306 import SSD1306_I2C
oledR=SSD1306_I2C(128,64,i2cR,addr=0x3C)
adc_x=ADC(28)
adc_y=ADC(27)
ROW_PINS=[10,9,8,7]
COL_PINS=[11,12,13,14]
rows=[Pin(p,Pin.OUT,value=1) for p in ROW_PINS]
cols=[Pin(p,Pin.IN,Pin.PULL_UP) for p in COL_PINS]
KEY_MAP=[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
scan_r = 0
scan_keys_buf = []
scan_last = []
scan_stable = 0
key_event = None
prev_had_key = False
hold_start = 0
key_hold = False
def scan_one_row():
    global scan_r, scan_keys_buf, scan_last, scan_stable, key_event, prev_had_key, hold_start, key_hold
    for rr in range(4):
        rows[rr].value(1)
    rows[scan_r].value(0)
    time.sleep_us(150)
    cur_row=[]
    for c in range(4):
        if cols[c].value()==0:
            cur_row.append(KEY_MAP[scan_r][c])
    if scan_r==0:
        scan_keys_buf=[]
    scan_keys_buf.extend(cur_row)
    rows[scan_r].value(1)
    scan_r=(scan_r+1)%4
    if scan_r==0:
        cur=sorted(scan_keys_buf)
        if cur==scan_last:
            scan_stable+=1
        else:
            scan_stable=0
        scan_last=cur
        has_key = len(cur)>0
        if scan_stable>=2:
            if has_key and not prev_had_key and key_event is None:
                key_event=cur[0]
                if cur[0]==8:
                    hold_start=time.ticks_ms()
            if not has_key:
                prev_had_key=False
                hold_start=0
                key_hold=False
            elif not prev_had_key:
                prev_had_key=True
            if has_key and hold_start and time.ticks_diff(time.ticks_ms(), hold_start)>900:
                key_hold=True

SCALES=['OFF','MAJ','MIN','PNT','CHROM','WHO','BLU','PEL','SLN','HIRA','BHR']
SCALE_MAP={'MAJ':[0,2,4,5,7,9,11],'MIN':[0,2,3,5,7,8,10],'PNT':[0,2,4,7,9],'CHROM':list(range(12)),'WHO':[0,2,4,6,8,10],'BLU':[0,3,5,6,7,10],'PEL':[0,1,5,7,10],'SLN':[0,2,5,7,9],'HIRA':[0,2,3,7,8],'BHR':[0,1,4,5,7,8,11]}
ROOTS=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
REFS=[415,432,435,440,442,528]
REF_NAMES=['A415','A432','A435','A440','A442','A528']
LVLS=['MUTE','LOW','MED','HIGH']
GAINS=[0,0.25,0.6,1.0]
TEMPS=['OFF','EQT','JST','PYT','MEANT','WERCK','19TET']
TEMP_MAP={'OFF':[0]*12,'EQT':[0]*12,'JST':[0,-29,4,-6,-14,-2,-20,2,-12,16,-18,-10],'PYT':[0,4,8,-8,12,-4,16,2,6,10,-12,14],'MEANT':[0,-24,-7,10,-6,-27,-3,14,-13,4,-20,-10],'WERCK':[0,-6,2,-4,4,-2,6,-2,2,4,-4,2],'19TET':[0,3,6,9,13,16,19,22,25,28,31,34]}

def midi_to_hz(m): return 440.0*(2**((m-69)/12.0))
def hz_to_midi(f): return 69+12*math.log2(f/440.0) if f>0 else 69

cur_wave='SQU'
scale_idx=0
temp_idx=0
ref_idx=3
lvl_idx=3
octave=0
root_idx=0
smooth_x=adc_x.read_u16()
smooth_y=adc_y.read_u16()
oled_ms=0
key_action_ms=0
oledR.fill(0)
oledR.text('v4.2h2 SIN/SQU/SAW/TRI',0,0,1)
oledR.show()
time.sleep_ms(400)

while True:
    smooth_x=(smooth_x*2+adc_x.read_u16())//3
    smooth_y=(smooth_y*2+adc_y.read_u16())//3
    norm_lin=1.0-(smooth_x/65535.0)
    norm = math.pow(max(0,min(1,norm_lin)), PITCH_CURVE)
    vol_raw=1.0-(smooth_y/65535.0)
    vol_raw=max(0,min(1,vol_raw))
    s_name=SCALES[scale_idx]
    t_name=TEMPS[temp_idx]
    ref=REFS[ref_idx]
    ref_off=12*math.log2(ref/440.0)
    base_scale = SCALE_MAP.get(s_name,list(range(12))) if s_name!='OFF' else list(range(12))
    transposed_scale = [(x+root_idx)%12 for x in base_scale]
    if s_name=='OFF' and t_name=='OFF':
        base=48+(norm*24.0)
        af=midi_to_hz(base+12*octave+ref_off)
        is_step=False
    else:
        slist=transposed_scale if s_name!='OFF' else list(range(12))
        tlist=TEMP_MAP.get(t_name,[0]*12)
        scaled=[]
        for m in range(48,84):
            if (m%12) in slist:
                scaled.append(m+tlist[m%12]/100.0)
        if not scaled:
            scaled=[60]
        idx=int(norm*len(scaled))
        idx=max(0,min(len(scaled)-1,idx))
        af=midi_to_hz(scaled[idx]+12*octave+ref_off)
        is_step=True

    vol_log = vol_raw*vol_raw  # LOG VOL as ear hears - your original

    if vol_raw<0.005 or GAINS[lvl_idx]==0:
        pwm.duty_u16(0)
    else:
        f=int(af)
        f=max(15,min(20000,f))
        pwm.freq(f)
        # keep duty handling identical to your no-hum version
        # but give each wave a slightly different duty for timbre
        base_duty = int(32768*GAINS[lvl_idx]*vol_log)
        if cur_wave=='SQU':
            pwm.duty_u16(base_duty)
        elif cur_wave=='SIN':
            pwm.duty_u16(int(base_duty*0.9))
        elif cur_wave=='SAW':
            pwm.duty_u16(int(base_duty*0.35))
        elif cur_wave=='TRI':
            pwm.duty_u16(int(base_duty*0.55))
        else:
            pwm.duty_u16(base_duty)

    scan_one_row()
    now=time.ticks_ms()
    if key_event is not None and time.ticks_diff(now,key_action_ms)>300:
        key_action_ms=now
        k=key_event
        key_event=None
        # YOUR REQUESTED MAP
        if k==0:
            cur_wave='SIN'
        elif k==1:
            cur_wave='SQU'
        elif k==2:
            cur_wave='SAW'
        elif k==3:
            cur_wave='TRI'
        elif k==8:
            ref_idx=(ref_idx+1)%len(REFS)
        elif k==9:
            root_idx=(root_idx+1)%12
        elif k==10:
            temp_idx=(temp_idx+1)%len(TEMPS)
        elif k==11:
            scale_idx=(scale_idx+1)%len(SCALES)
        elif k==12:
            if octave<5: octave+=1
        elif k==13:
            lvl_idx=(lvl_idx+1)%4
        elif k==14:
            pass
        elif k==15:
            if octave>-4: octave-=1

    if time.ticks_diff(now,oled_ms)>200:
        oled_ms=now
        oledR.fill(0)
        midi=int(hz_to_midi(af))
        notes=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        note_str = notes[midi%12] + str(midi//12-1)
        oledR.text(str(int(af))+"Hz",0,0,1)
        oledR.text(note_str,52,0,1)
        oledR.text(cur_wave,92,0,1)
        oledR.text("K:"+ROOTS[root_idx],0,14,1)
        oledR.text(LVLS[lvl_idx],44,14,1)
        oledR.text('STEP' if is_step else 'GLISS',80,14,1)
        oledR.text(REF_NAMES[ref_idx],0,28,1)
        oct_s="+"+str(octave) if octave>=0 else str(octave)
        oledR.text("OCT:"+oct_s,60,28,1)
        oledR.text("T:"+TEMPS[temp_idx],0,42,1)
        oledR.text("S:"+SCALES[scale_idx],64,42,1)
        oledR.fill_rect(0,56,int(vol_log*128),8,1)
        oledR.show()
