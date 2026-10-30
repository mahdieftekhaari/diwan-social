import sys
def rooster(x,y,s,flip=False):
    # local coords ~ 420w x 520h, rooster facing left; origin top-left
    t=f'translate({x},{y}) scale({-s if flip else s},{s})'
    return f'''<g transform="{t}">
<defs>
<linearGradient id="tail" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#0f5d6b"/><stop offset=".55" stop-color="#1d8a86"/><stop offset="1" stop-color="#e3c46b"/></linearGradient>
<linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a2a1c"/><stop offset=".5" stop-color="#b4521f"/><stop offset="1" stop-color="#3a1a1c"/></linearGradient>
<linearGradient id="wing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e3a23a"/><stop offset="1" stop-color="#8c3d1c"/></linearGradient>
</defs>
<!-- tail feathers -->
<g stroke="#0b3f4c" stroke-width="3" stroke-linejoin="round">
<path d="M255 305 C340 300 430 210 408 52 C372 150 330 240 262 322 Z" fill="url(#tail)"/>
<path d="M258 312 C350 335 462 262 452 112 C410 210 340 290 262 330 Z" fill="url(#tail)"/>
<path d="M248 296 C322 262 366 170 330 28 C312 140 290 230 252 312 Z" fill="url(#tail)"/>
<path d="M254 322 C316 392 436 350 468 226 C420 300 340 338 260 334 Z" fill="#e3c46b"/>
<path d="M246 290 C290 230 270 140 232 70 C236 160 232 230 244 300 Z" fill="url(#tail)"/>
</g>
<g fill="#e3c46b" opacity=".9"><circle cx="392" cy="112" r="9"/><circle cx="433" cy="170" r="8"/><circle cx="322" cy="86" r="8"/></g>
<g fill="#0b3f4c"><circle cx="392" cy="112" r="4"/><circle cx="433" cy="170" r="3.5"/><circle cx="322" cy="86" r="3.5"/></g>
<!-- legs -->
<g stroke="#e3c46b" stroke-width="9" stroke-linecap="round" fill="none">
<path d="M165 415 L150 480 M150 480 L120 486 M150 480 L158 492 M150 480 L180 490"/>
<path d="M205 415 L215 480 M215 480 L185 488 M215 480 L224 492 M215 480 L246 488"/>
</g>
<!-- body -->
<path d="M112 150 C84 205 72 275 105 345 C140 425 235 440 280 350 C305 305 292 250 258 222 C220 190 168 178 140 140 Z" fill="url(#body)" stroke="#e3c46b" stroke-width="3"/>
<!-- neck hackles -->
<path d="M120 150 C100 190 96 230 112 270 C130 240 150 200 150 160 Z" fill="#e3a23a" opacity=".9"/>
<path d="M150 160 C128 200 126 250 142 290 C165 255 180 210 176 170 Z" fill="#c4722a" opacity=".9"/>
<!-- wing -->
<path d="M150 270 C170 245 240 250 275 290 C255 350 190 375 145 345 C130 315 135 290 150 270 Z" fill="url(#wing)" stroke="#3a1a1c" stroke-width="3"/>
<g stroke="#3a1a1c" stroke-width="3" fill="none" opacity=".7"><path d="M165 290 C200 280 235 290 255 305"/><path d="M160 315 C195 308 225 318 245 332"/></g>
<!-- head -->
<circle cx="125" cy="128" r="30" fill="#8c3d1c" stroke="#e3c46b" stroke-width="3"/>
<g fill="#c8261c"><circle cx="108" cy="98" r="12"/><circle cx="127" cy="91" r="13"/><circle cx="147" cy="98" r="11"/></g>
<ellipse cx="112" cy="162" rx="9" ry="17" fill="#c8261c"/>
<!-- beak open -->
<path d="M98 120 L52 118 L98 130 Z" fill="#e3c46b"/><path d="M98 134 L60 146 L102 142 Z" fill="#e3c46b"/>
<circle cx="116" cy="124" r="5" fill="#fff6dd"/><circle cx="115" cy="124" r="2.5" fill="#1b1a2e"/>
<!-- sound arcs -->
<g fill="none" stroke="#fff3c4" stroke-width="5" stroke-linecap="round" opacity=".85"><path d="M30 100 C16 125 16 150 30 172"/><path d="M8 84 C-14 120 -14 160 8 196" opacity=".6"/></g>
</g>'''
def art(W,H,focus=0.40):
    # sky
    import math
    wide=W>H
    if wide:
        cx,cy=W*0.73,H*0.5
        s=H*0.0017
    elif H/W>1.5:
        cx,cy=W/2,H*0.27
        s=W*0.0017
    else:
        cx,cy=W/2,H*0.30
        s=min(W,H)*0.0011
    R=min(W,H)*(0.30 if wide else 0.33)
    rays=''.join(f'<path d="M{cx} {cy} L{cx+3000*math.cos(a)} {cy+3000*math.sin(a)} L{cx+3000*math.cos(a+0.06)} {cy+3000*math.sin(a+0.06)} Z" fill="#fff0b8" opacity=".10"/>' for a in [i*0.2618 for i in range(24)])
    mt=H*0.80
    rw,rh=420*s,520*s
    rx=cx-230*s; ry=cy-270*s
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12123a"/><stop offset=".35" stop-color="#3a2a63"/><stop offset=".62" stop-color="#c8643a"/><stop offset=".82" stop-color="#f3b45a"/><stop offset="1" stop-color="#fbe3a0"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fffbe6"/><stop offset=".55" stop-color="#ffe08a"/><stop offset="1" stop-color="#f3a845" stop-opacity="0"/></radialGradient>
<linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2a52"/><stop offset="1" stop-color="#1a1530"/></linearGradient>
<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#241c3a"/><stop offset="1" stop-color="#0f0b1e"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g>{rays}</g>
<circle cx="{cx}" cy="{cy}" r="{R*1.5}" fill="url(#sun)"/>
<circle cx="{cx}" cy="{cy}" r="{R*0.75}" fill="#fff4c6"/>
<circle cx="{cx}" cy="{cy}" r="{R*0.75}" fill="none" stroke="#e3c46b" stroke-width="4" opacity=".8"/>
<g fill="#fff6dd" opacity=".8">{''.join(f'<circle cx="{(i*977)%int(W)}" cy="{(i*313)%int(H*0.33)}" r="{1.4+(i%3)}"/>' for i in range(34))}</g>
<path d="M0 {mt} L{W*0.12} {mt-H*0.07} L{W*0.26} {mt-H*0.02} L{W*0.42} {mt-H*0.09} L{W*0.58} {mt-H*0.03} L{W*0.74} {mt-H*0.08} L{W*0.9} {mt-H*0.02} L{W} {mt-H*0.05} L{W} {H} L0 {H} Z" fill="url(#m1)"/>
<path d="M0 {mt+H*0.07} L{W*0.18} {mt+H*0.0} L{W*0.34} {mt+H*0.05} L{W*0.55} {mt-H*0.01} L{W*0.8} {mt+H*0.05} L{W} {mt+H*0.0} L{W} {H} L0 {H} Z" fill="url(#m2)"/>
{rooster(rx,ry,s)}
</svg>'''
    return svg
if __name__=='__main__':
    for n,(W,H) in dict(ig=(1080,1350),tg=(1280,720),x=(1600,900),st=(1080,1920)).items():
        open(f'assets/cover_{n}.svg','w').write(art(W,H,0.40 if W<=H else 0.38))
