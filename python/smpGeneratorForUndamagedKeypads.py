# RUN THIS ON PICO ONCE TO MAKE /smp/smp1-4.raw - GOOD KEYPAD VERSION
# K4=SMP1 K5=SMP2 K6=SMP3 K7=SMP4
import math, uos
try: uos.mkdir('/smp')
except: pass

def make_raw(name, func):
    with open('/smp/'+name,'wb') as f:
        for i in range(8000):
            t=i/16000
            v=func(t,i)
            v=max(-1,min(1,v))
            iv=int(v*32767)
            if iv<0: iv+=65536
            f.write(bytes([iv&0xFF, (iv>>8)&0xFF]))
    print(name,'done')

# SMP1 - warm bass 55Hz (good for scale steps)
make_raw('smp1.raw', lambda t,i: (math.sin(2*math.pi*55*t)*0.7 + math.sin(2*math.pi*110*t)*0.3) * min(1,i/800) * min(1,(8000-i)/800))

# SMP2 - plucky saw 110Hz (plucky decay, joy X pitch works great)
make_raw('smp2.raw', lambda t,i: ((2*((t*110)%1)-1)*0.6) * math.exp(-3*t))

# SMP3 - FM bell 220Hz (bell, nice with temperaments)
make_raw('smp3.raw', lambda t,i: math.sin(2*math.pi*220*t + math.sin(2*math.pi*440*t)*2*math.exp(-2.5*t)) * math.exp(-2.5*t))

# SMP4 - soft pad 110Hz with slow attack (for gliss mode)
make_raw('smp4.raw', lambda t,i: (math.sin(2*math.pi*110*t)*0.5 + math.sin(2*math.pi*220*t)*0.3 + math.sin(2*math.pi*330*t)*0.2) * min(1,i/2000) * math.exp(-1.2*t) * 0.8)

import uos; print(uos.listdir('/smp'))
print('Now reboot with v4.2h3-GOOD - K4-K7 should show [4,5,6,7]')
