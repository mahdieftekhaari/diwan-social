import json,sys,re,os
from playwright.sync_api import sync_playwright
DORAN=open('doran.css').read()
FA=str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹')
def fa(n): return str(n).translate(FA)
L=lambda s:f'<span dir="ltr" class="lt">{s}</span>'
N=5
XS=[1,2,4,5]
K='امکانات دیوان'
S=[
 dict(k='text',kicker=K,title='پانویس',body='واژه، نام یا اشاره‌ای که شاید برای خواننده\nآشنا نباشند، در دیوان به آسانی\nتوضیح داده می‌شوند.\n\nنویسنده توضیحش را در پانویس اضافه می‌کند\nو خواننده بی‌آن‌که از صفحه بیرون برود\nمی‌تواند پانویس را ببیند.'),
 dict(k='hover',kicker='',title='دیدن پانویس',cap='زیر واژه یک خط نقطه‌چین طلایی می‌بینی.\nنشانگر را روی آن ببر یا لمسش کن.\nمثلاً برای <span class="mkw">فیثاغورس</span> در متن زیر.',ptitle='فیثاغورس',pbody='فیلسوف و ریاضی‌دان یونانی،\nسدهٔ ششم پیش از میلاد.',plink='دیدن در واژه‌نامه'),
 dict(k='shot',title='چطور پانویس بگذاریم؟',cap='در ویرایشگر، واژه یا عبارت را انتخاب کن\nو از نوار ابزار «پانویس» را بزن.',img='assets/toolbar_c.png'),
 dict(k='form',title='چطور پانویس بگذاریم؟',cap='عنوان و توضیح کوتاه بنویس؛ تصویر اختیاری است.\nیا یکی از پانویس‌های موجود را جستجو کن.'),
 dict(k='text',kicker=K,title='واژه‌نامه‌ی دیوان',body='پانویس‌ها مشترک‌اند.\nهر نویسنده‌ی دیوان می‌تواند یکی بسازد\nو دیگران هم در آثارشان از همان استفاده کنند.\n\nصفحه‌ی «واژه‌نامه» همه‌ی آن‌ها را جمع می‌کند\nو نشان می‌دهد هر کدام در چند اثر آمده.'),
 dict(k='gloss',title='صفحه‌ی واژه‌نامه',cap='همین حالا این پانویس‌ها در دیوان هستند.\n<span dir="ltr">diwan.center/footnotes</span>'),
 dict(k='close',title='پانویس بعدی مال توست',body='واژه‌ای ناآشنا در نوشته‌ات هست؟\nتوضیحش را همان‌جا بگذار.',final='داستانت را بنویس و منتشر کن.',),
]
N=7; XS=[1,3,4,6]
assert len(S)==N
SIZES={'st':(1080,1920),'ig':(1080,1350),'tg':(1280,720),'x':(1600,900)}
CSS=DORAN+"""
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Regular.woff2) format('woff2');font-weight:400}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Medium.woff2) format('woff2');font-weight:500}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-SemiBold.woff2) format('woff2');font-weight:600}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Bold.woff2) format('woff2');font-weight:700}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-ExtraBold.woff2) format('woff2');font-weight:800}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;background:#faf7f2}
body{font-family:Vazirmatn,sans-serif;direction:rtl;color:#1c1a16}
.slide{position:relative;width:var(--W);height:var(--H);overflow:hidden;background:#faf7f2;display:flex}
.slide::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(201,168,76,.16),transparent 62%);pointer-events:none}
.lt{direction:ltr;unicode-bidi:isolate;display:inline-block;font-family:Vazirmatn,sans-serif}
.panel{position:relative;flex:1;display:flex;flex-direction:column;min-width:0;padding:var(--pad);gap:var(--gap)}
.imgp{position:relative;flex:0 0 var(--imgw);height:100%;background-size:cover;background-position:center}
.kick{display:flex;align-items:center;justify-content:center;gap:16px;color:#836a27;font-weight:600;font-size:var(--fk)}
.kick i{width:var(--rule);height:2px;background:#c9a84c}
h1,h2{font-family:Doran,Vazirmatn,sans-serif;font-weight:800;line-height:1.3;text-align:center;font-size:var(--ft)}
.body{font-size:var(--fb);line-height:1.95;text-align:center;white-space:pre-line}
.main{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:var(--gap2);align-items:center}
.foot{display:flex;align-items:center;justify-content:space-between;color:#836a27;font-weight:600;font-size:var(--ff)}
.foot b{font-family:Doran,Vazirmatn,sans-serif;font-size:calc(var(--ff)*1.45);color:#836a27}
.foot .pg{color:#6b6456;font-weight:500}
.frame{position:absolute;inset:var(--m);border:2px solid #c9a84c;pointer-events:none;z-index:3}
.frame::after{content:"";position:absolute;inset:9px;border:1px solid #c9a84c;opacity:.5}
.dia{position:absolute;width:24px;height:24px;background:#c9a84c;transform:rotate(45deg);z-index:4}
.dia.a{top:calc(var(--m) - 12px);left:calc(var(--m) - 12px)}.dia.b{top:calc(var(--m) - 12px);right:calc(var(--m) - 12px)}
.dia.c{bottom:calc(var(--m) - 12px);left:calc(var(--m) - 12px)}.dia.d{bottom:calc(var(--m) - 12px);right:calc(var(--m) - 12px)}
.verse{position:relative;text-align:center;font-size:var(--fv);line-height:2.05;font-weight:500;padding:0 28px}
.verse.sm{font-size:calc(var(--fv)*.82)}
.vcap{color:#836a27;font-weight:600;font-size:calc(var(--fb)*.85)}
.src{color:#6b6456;font-size:calc(var(--fb)*.72);text-align:center}
.chips{display:flex;gap:18px;justify-content:center;flex-wrap:wrap}
.chip{border:2px solid #c9a84c;border-radius:14px;padding:10px 26px;text-align:center;background:rgba(201,168,76,.10)}
.chip .w{font-size:calc(var(--fb)*1.25);font-weight:700;color:#1c1a16;direction:ltr}.chip .l{font-size:calc(var(--fb)*.66);color:#6b6456}
.note{font-size:calc(var(--fb)*.72);color:#6b6456;text-align:center}
.eq{font-family:Doran,Vazirmatn;font-size:calc(var(--ft)*1.05);color:#836a27;font-weight:800;text-align:center}
.chain{display:flex;flex-direction:var(--cdir);align-items:center;justify-content:center;gap:var(--cgap)}
.node{border:2px solid #c9a84c;border-radius:16px;padding:14px 22px;text-align:center;background:#fff9ec;min-width:var(--nw)}
.node .w{font-size:calc(var(--fb)*1.15);font-weight:700;direction:ltr}.node .l{font-size:calc(var(--fb)*.68);color:#836a27;font-weight:600}.node .m{font-size:calc(var(--fb)*.66);color:#6b6456}
.arr{color:#c9a84c;font-size:calc(var(--fb)*1.3);line-height:1}
.tree{display:flex;flex-direction:column;align-items:center;gap:var(--cgap);width:100%}
.kids{display:flex;gap:18px;width:100%;justify-content:center}
.kid{flex:1;border:2px solid #c9a84c;border-radius:16px;padding:14px 12px;text-align:center;background:#fff9ec}
.kid .w{font-family:Doran,Vazirmatn;font-size:calc(var(--fb)*1.3);font-weight:800}.kid .e{font-size:calc(var(--fb)*.62);color:#836a27;direction:ltr;font-weight:600;margin:4px 0}.kid .m{font-size:calc(var(--fb)*.66);color:#6b6456}
.root{border:2px solid #836a27;background:#836a27;color:#fff;border-radius:16px;padding:10px 34px;text-align:center}
.root .w{font-size:calc(var(--fb)*1.3);font-weight:800;direction:ltr}.root .m{font-size:calc(var(--fb)*.7)}
.tbl{width:100%;border-collapse:collapse;font-size:var(--ftb)}
.tbl th{background:#c9a84c;color:#0c0a07;padding:var(--tp) 14px;font-weight:700}
.tbl td{padding:var(--tp) 14px;border-bottom:1px solid #ddd8ce;text-align:center}
.tbl td:first-child{font-weight:700;font-family:Doran,Vazirmatn}
.tbl tr.win td{background:#fff1cc;font-weight:800;color:#1c1a16}.tbl td.bd{color:#836a27;font-weight:800;font-size:.72em}.tbl td:nth-child(2){font-family:Vazirmatn,sans-serif}.kk2{color:#836a27;font-weight:600;font-size:var(--fk)}.lead{font-size:calc(var(--fb)*.85);color:#6b6456;text-align:center}
.acard{width:100%;border:2px solid #d7d2c6;border-radius:26px;padding:var(--ap);display:flex;flex-direction:var(--cdir);align-items:center;justify-content:center;gap:var(--ag);background:linear-gradient(165deg,rgba(43,93,147,.09),#fffdf8 65%)}
.aav{display:flex;flex-direction:column;align-items:center;gap:14px}.arch{width:var(--aw);height:calc(var(--aw)*1.25);border-radius:999px 999px 14px 14px;border:3px solid rgba(43,93,147,.4);background-size:cover;background-position:center}
.lvl{border:1.5px solid #2b5d93;color:#2b5d93;border-radius:999px;padding:4px 22px;font-size:calc(var(--fb)*.6);font-weight:500}
.atx{text-align:center}.aname{font-family:Doran,Vazirmatn;font-weight:800;font-size:calc(var(--ft)*1.1)}.aact{color:#6b6456;font-size:calc(var(--fb)*.85);margin-top:6px}
.wk{display:flex;align-items:center;gap:16px;background:#fff;border:1.5px solid #e3ded3;border-radius:16px;padding:12px 16px;max-width:var(--wkw)}
.wt{font-weight:600;font-size:calc(var(--fb)*.62);line-height:1.7;text-align:right}.wc{flex:0 0 var(--cw);height:var(--cw);border-radius:10px;background-size:cover;background-position:center}
.final{white-space:pre-line;font-family:Doran,Vazirmatn;font-weight:800;color:#836a27;font-size:var(--fb2);text-align:center;line-height:1.6}
.link{direction:ltr;font-weight:700;letter-spacing:.06em;color:#836a27;font-size:var(--ff2);text-align:center}
.cover .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,8,0) 35%,rgba(20,16,8,.88) 100%);z-index:1}
.cover{background-size:cover}
.mkp .bl{filter:blur(4px);opacity:.55}.hv{position:relative;display:inline-block;padding:0 2px}
.cur{position:absolute;left:38%;top:70%;width:calc(var(--fb)*1.9);height:auto;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))}
.car{width:0;height:0;border:14px solid transparent;border-top-color:#d7d2c6;border-bottom:0;margin:-6px 0 -2px}
.shot{width:100%;border-radius:18px;border:1.5px solid #e3ded3;box-shadow:0 14px 34px -14px rgba(0,0,0,.35)}
.gp{width:100%;background:#faf7f2;border:1.5px solid #e3ded3;border-radius:20px;padding:16px;box-shadow:0 14px 34px -14px rgba(0,0,0,.35)}
.gh{font-family:Doran,Vazirmatn;font-weight:800;font-size:calc(var(--fb)*.9);text-align:right;margin-bottom:10px}
.gg{display:grid;grid-template-columns:repeat(var(--gcols),1fr);gap:10px}
.gc{background:#f5f2ec;border:1.5px solid #e3ded3;border-radius:16px;overflow:hidden;display:flex;flex-direction:column;text-align:right}
.gi{height:var(--gih);display:flex;align-items:center;justify-content:center;background:#ebe6db;color:#b3ab98;font-family:Doran,Vazirmatn;font-size:calc(var(--fb)*1.1)}
.gt{padding:8px 12px;display:flex;flex-direction:column;gap:4px}.gt b{font-family:Doran,Vazirmatn;font-size:calc(var(--fb)*.72)}
.gt span{font-size:calc(var(--fb)*.56);line-height:1.7;color:#6b6456;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.gt em{font-style:normal;font-size:calc(var(--fb)*.5);color:#a8883a}

.tb{display:flex;gap:6px;align-items:center;background:#fff;border:1.5px solid #d7d2c6;border-radius:14px;box-shadow:0 12px 28px -12px rgba(0,0,0,.35);padding:8px 10px;font-size:calc(var(--fb)*.85)}
.tbb{min-width:1.7em;height:1.7em;display:flex;align-items:center;justify-content:center;border-radius:8px;color:#3a352c;padding:0 6px}
.tbb.on{background:#f4e8c2;color:#6b5420;gap:8px;padding:0 14px;font-weight:700;border:1.5px solid #c9a84c}.tbb.on em{font-style:normal;font-size:.9em}
.sel{background:#cfe0ff;border-radius:4px;padding:0 4px}
.fm{width:82%;display:flex;flex-direction:column;gap:12px;background:#fffdf8;border:1.5px solid #d7d2c6;border-radius:18px;box-shadow:0 14px 34px -14px rgba(0,0,0,.35);padding:26px 28px;text-align:right}
.fi,.ft{border:1.5px solid #d7d2c6;border-radius:12px;padding:12px 16px;background:#fff;font-size:calc(var(--fb)*.85)}.fi{font-weight:700}.ft{line-height:1.8;color:#3a352c}
.fth{color:#836a27;font-size:calc(var(--fb)*.7);font-weight:600}
.fbtn{background:#c9a84c;color:#0c0a07;font-weight:800;text-align:center;border-radius:12px;padding:12px;font-size:calc(var(--fb)*.85)}
.fsr{text-align:center;color:#836a27;font-size:calc(var(--fb)*.7);text-decoration:underline dotted}
.ftr{width:100%;display:flex;gap:calc(var(--gap2)*1.2);justify-content:center;align-items:flex-start;background:#1c1a16;color:#e9e2d0;border-radius:18px;padding:30px 28px}
.fcol{display:flex;flex-direction:column;gap:10px;flex:1;text-align:right}.fh{font-size:calc(var(--fb)*.55);letter-spacing:.18em;color:#a89a74;margin-bottom:4px}
.fl{font-size:calc(var(--fb)*.8)}.fl.hi{background:#c9a84c;color:#0c0a07;font-weight:800;border-radius:8px;padding:2px 10px;align-self:flex-start}

.mk{width:100%;display:flex;flex-direction:column;align-items:center;gap:calc(var(--gap2)*.6)}
.mkp{width:100%;background:#fff;border:1.5px solid #e3ded3;border-radius:18px;padding:26px 30px;font-size:calc(var(--fb)*1.0);line-height:2;text-align:right}
.mkw{border-bottom:3px dotted #836a27;padding-bottom:2px}
.mkc{width:78%;background:#fffdf8;border:1.5px solid #d7d2c6;border-radius:18px;box-shadow:0 14px 34px -14px rgba(0,0,0,.35);padding:22px 26px;display:flex;flex-direction:column;gap:8px;text-align:right}
.mkc b{font-family:Doran,Vazirmatn;font-size:calc(var(--fb)*1.1);font-weight:800}
.mkc span{white-space:pre-line;font-size:calc(var(--fb)*.82);color:#3a352c;line-height:1.8}
.mkc i{font-style:normal;color:#836a27;font-weight:600;font-size:calc(var(--fb)*.7)}

.ol{list-style:none;width:100%;display:flex;flex-direction:column;gap:calc(var(--gap2)*.7)}.ol li{display:flex;gap:20px;align-items:flex-start;font-size:calc(var(--fb)*1.02);line-height:1.8}.ol b{flex:0 0 1.7em;height:1.7em;border-radius:50%;background:#c9a84c;color:#0c0a07;text-align:center;line-height:1.7em;font-family:Doran,Vazirmatn;font-size:.9em}
.cover .ct{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:var(--cpad);text-align:center;color:#faf7f2;display:flex;flex-direction:column;gap:18px;align-items:center}
.cover h1{color:#faf7f2;font-size:var(--fct)}
.cover .sub{font-size:var(--fb);color:#f1e7c9;line-height:1.8}
.cover .kk{color:#e3c46b;font-weight:600;font-size:var(--fk)}
"""
VARS={
'ig':"--W:1080px;--H:1350px;--m:44px;--pad:104px 100px 96px;--gap:34px;--gap2:30px;--fk:30px;--rule:60px;--ft:70px;--fb:40px;--ff:27px;--ff2:36px;--fv:48px;--ftb:35px;--tp:20px;--fb2:44px;--cdir:column;--cgap:20px;--nw:520px;--imgw:0px;--fct:104px;--cpad:90px 80px 100px",
'tg':"--W:1280px;--H:720px;--m:28px;--pad:56px 64px 46px;--gap:16px;--gap2:18px;--fk:21px;--rule:44px;--ft:42px;--fb:24px;--ff:20px;--ff2:24px;--fv:30px;--ftb:21px;--tp:8px;--fb2:32px;--cdir:row;--cgap:12px;--nw:170px;--imgw:700px;--fct:84px;--cpad:50px 60px 60px",
'x':"--W:1600px;--H:900px;--m:32px;--pad:70px 80px 56px;--gap:20px;--gap2:22px;--fk:24px;--rule:50px;--ft:52px;--fb:29px;--ff:23px;--ff2:28px;--fv:36px;--ftb:25px;--tp:10px;--fb2:38px;--cdir:row;--cgap:14px;--nw:200px;--imgw:860px;--fct:104px;--cpad:60px 80px 70px",
}
VARS['st']=VARS['ig'].replace('--H:1350px','--H:1920px')
BMSVG='<svg viewBox="0 0 24 24" width="1.1em" height="1.1em" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v8l3-2 3 2V2"/><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>'
def foot(i,plat):
    pos,tot=(XS.index(i)+1,len(XS)) if plat=='x' else (i,N)
    return f'<div class="foot"><span><b>دیوان</b> &nbsp;<span class="lt">diwan.center</span></span><span class="pg" dir="ltr">{fa(pos)} / {fa(tot)}</span></div>'
def html(i,s,plat):
    k=s['k']; W,H=SIZES[plat]; wide=plat!='ig'
    frame='<div class="frame"></div><div class="dia a"></div><div class="dia b"></div><div class="dia c"></div><div class="dia d"></div>'
    def kick(): return ''
    if k=='cover':
        return f'<div class="slide cover" style="background-image:url(../{s["img"]});background-position:center 22%"><div class="shade"></div><div class="ct"><div class="kk">{s["kicker"]}</div><h1>{s["title"]}</h1><div class="sub">{s["sub"]}</div></div></div>'
    inner=''
    if k=='chips':
        inner=f'<h2>{s["title"]}</h2><div class="body">{s["body"]}</div><div class="chips">'+''.join(f'<div class="chip"><div class="w">{w}</div><div class="l">{l}</div></div>' for w,l in s['chips'])+f'</div><div class="note">{s["note"]}</div>'
    elif k=='text':
        inner=(f'<div class="kk2">{s["kicker"]}</div>' if s.get('kicker') else '')+f'<h2>{s["title"]}</h2><div class="body">{s["body"]}</div>'
    elif k=='word':
        inner=f'<h2>{s["title"]}</h2><div class="eq">{s["eq"]}</div><div class="body">{s["body"]}</div>'
    elif k=='verse':
        inner=f'<div class="vcap">{s["cap1"]}</div><div class="verse">{"<br>".join(s["v1"])}</div><div class="vcap">{s["cap2"]}</div><div class="verse">{"<br>".join(s["v2"])}</div><div class="src">{s["src"]}</div>'
    elif k=='chain':
        parts=[]
        for n,(w,l,m) in enumerate(s['chain']):
            if n: parts.append('<div class="arr">'+('◀' if wide else '▼')+'</div>')
            parts.append(f'<div class="node"><div class="w">{w}</div><div class="l">{l}</div><div class="m">{m}</div></div>')
        inner=f'<h2>{s["title"]}</h2><div class="chain">{"".join(parts)}</div><div class="note">{s["note"]}</div>'
    elif k=='tree':
        r=s['root']
        inner=f'<h2>{s["title"]}</h2><div class="tree"><div class="root"><div class="w" style="direction:rtl">{r[0]}</div><div class="m">{r[1]}</div></div><div class="arr">▼</div><div class="kids">'+''.join(f'<div class="kid"><div class="w">{a}</div><div class="e">{b}</div><div class="m">{c}</div></div>' for a,b,c in s['kids'])+'</div></div>'
    elif k=='table':
        inner=f'<h2>{s["title"]}</h2><table class="tbl"><tr>'+''.join(f'<th>{h}</th>' for h in s['head'])+'</tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in s['rows'])+'</table>'
    elif k=='aotw':
        inner=(f'<div class="kk2">{s["kicker"]}</div><h2 style="font-size:calc(var(--ft)*1.25)">{s["title"]}</h2><div class="lead">{s["lead"]}</div>'
          f'<div class="acard"><div class="aav"><div class="arch" style="background-image:url(../'+CFG['avatar']+')"></div></div>'
          f'<div class="atx"><div class="aname">{s["name"]}</div><div class="aact">{s["act"]}</div></div>'
          f'<div class="wk"><div class="wt">{s["work"]}</div><div class="wc" style="background-image:url(../'+CFG['cover']+')"></div></div></div>')
    elif k=='lb':
        rows=''.join('<tr'+(' class="win"' if n==0 else '')+'>'+''.join(f'<td>{c}</td>' for c in r)+('<td class="bd">'+s['badge']+'</td>' if n==0 else '<td class="bd"></td>')+'</tr>' for n,r in enumerate(s['rows']))
        inner=f'<h2>{s["title"]}</h2><table class="tbl"><tr>'+''.join(f'<th>{h}</th>' for h in s['head'])+'<th></th></tr>'+rows+f'</table><div class="note">{s["note"]}</div>'
    elif k=='mock':
        inner=(f'<div class="kk2">{s["kicker"]}</div><h2>{s["title"]}</h2><div class="mk"><p class="mkp">{s["para_a"]}<span class="mkw">{s["word"]}</span>{s["para_b"]}</p><div class="mkc"><b>{s["ptitle"]}</b><span>{s["pbody"]}</span><i>{s["plink"]}</i></div></div><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div>')
    elif k=='hover':
        inner=(f'<div class="kk2">{s["kicker"]}</div><h2>{s["title"]}</h2><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div><div class="mk"><div class="mkc"><b>{s["ptitle"]}</b><span>{s["pbody"]}</span><i>{s["plink"]}</i></div><div class="car"></div><p class="mkp"><span class="bl">دیرزمانی است که ریاضی‌دانان می‌گویند جهان را باید با عدد خواند و هر نظمی</span> <span class="mkw hv">فیثاغورس<svg class="cur" viewBox="0 0 24 24" width="64" height="64"><path d="M5 3l14 8-6 1.8L9.6 19z" fill="#111" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg></span> <span class="bl">را به یاد می‌آورد؛ آنچه او آغاز کرد در سده‌ها ادامه یافت.</span></p></div>')
    elif k=='shot':
        inner=(f'<h2>{s["title"]}</h2><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div><img class="shot" src="file://{os.getcwd()}/{s["img"]}">')
    elif k=='gloss':
        cards=[('جلال آل احمد','منظور بزرگراه جلال آل احمد در تهران است.'),('Kinko','سرویس پستی و پرینت که در سال ۱۹۷۰ تأسیس شد و در ۲۰۰۴ شرکت پستی فد-اکس آن را خرید.'),("Bloomingdale's",'نام یک فروشگاه زنجیره‌ای در آمریکا'),('whole food','نام فروشگاهی زنجیره‌ای در آمریکا'),('روزهای سرکشی','روزهای سرکشی در برابر Days of being wild از ساخته های ونگ کار وای است.'),('ونگ کار وای','فیلمساز هنگ‌کنگی متولد چین.')]
        cs=''.join(f'<div class="gc"><div class="gi">{t[0]}</div><div class="gt"><b>{t}</b><span>{b}</span><em>استفاده‌شده در ۱ اثر</em></div></div>' for t,b in cards)
        inner=(f'<h2>{s["title"]}</h2><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div><div class="gp"><div class="gh">واژه‌نامه</div><div class="gg">{cs}</div></div>')
    elif k=='toolbar':
        inner=(f'<h2>{s["title"]}</h2><div class="mk"><div class="tb"><span class="tbb"><b>B</b></span><span class="tbb"><i>I</i></span><span class="tbb"><u>U</u></span><span class="tbb"><s>S</s></span><span class="tbb">&#128279;</span><span class="tbb on">BMSVG<em>پانویس</em></span></div><p class="mkp">ریاضی‌دانان از روزگار <span class="sel">فیثاغورس</span> می‌دانستند که کار با عدد، کار با نظم جهان است.</p></div><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div>').replace('BMSVG',BMSVG)
    elif k=='form':
        inner=(f'<h2>{s["title"]}</h2><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div><div class="fm"><div class="fi">فیثاغورس</div><div class="ft">فیلسوف و ریاضی‌دان یونانی،<br>سدهٔ ششم پیش از میلاد.</div><div class="fth">&#128247; افزودن تصویر بندانگشتی (اختیاری)</div><div class="fbtn">افزودن پانویس</div><div class="fsr">جستجوی پانویس‌های موجود...</div></div>')
    elif k=='footer':
        def col(h,items,hl=None): return f'<div class="fcol"><span class="fh">{h}</span>'+''.join(f'<span class="fl{" hi" if x==hl else ""}">{x}</span>' for x in items)+'</div>'
        inner=(f'<h2>{s["title"]}</h2><div class="ftr">'+col('ساختار',['جشنواره','مجله','وبلاگ','واژه‌نامه','آثار','نقشه سایت'],'واژه‌نامه')+col('امکانات',['نام‌نویسی','ورود','حساب ویژه','کلاس‌ها','بازار'])+col('چیستی دیوان',['درباره ما','تماس','حمایت مالی','شرایط استفاده','حریم خصوصی'])+f'</div><div class="body" style="font-size:calc(var(--fb)*.9)">{s["cap"]}</div>')
    elif k=='list':
        inner=f'<h2>{s["title"]}</h2><ol class="ol">'+''.join(f'<li><b>{fa(n+1)}</b><span>{t}</span></li>' for n,t in enumerate(s['items']))+'</ol>'
    elif k=='close':
        inner=f'<h2>{s["title"]}</h2><div class="body">{s["body"]}</div><div class="final">{s["final"]}</div><div class="link">diwan.center</div>'+(f'<div class="note">{s["src"]}</div>' if s.get('src') else '')
    elif k in('imgtext','imgverse'):
        t=(f'<div class="kk2">{s["kicker"]}</div>' if s.get('kicker') else '')+f'<h2>{s["title"]}</h2>'
        if s.get('body'): t+=f'<div class="body">{s["body"]}</div>'
        if s.get('verse'): t+=f'<div class="verse sm">{"<br>".join(s["verse"])}</div><div class="src">{s["src"]}</div>'
        if wide:
            return f'<div class="slide"><div class="panel" style="--pad:44px 56px 40px">{kick()}<div class="main">{t}</div>{foot(i,plat)}</div><div class="imgp" style="background-image:url(../{s.get("imgw",s["img"])});background-position:{s.get("tpos","50%")} center;{("flex-basis:%dpx"%s["pw"][plat]) if s.get("pw") else ""}"></div></div>'
        # ig: image top, text bottom
        ih=s.get('ih',720)
        return (f'<div class="slide" style="flex-direction:column"><div style="height:{ih}px;background-image:url(../{s.get("imgw",s["img"])});background-size:cover;background-position:center {s.get("pos","50%")};border-bottom:3px solid #c9a84c"></div>'
                f'<div class="panel" style="--pad:18px 90px 26px;--gap:10px">{kick()}<div class="main" style="--gap2:14px">{t}</div>{foot(i,plat)}</div></div>')
    return f'<div class="slide">{frame}<div class="panel">{kick()}<div class="main">{inner}</div>{foot(i,plat)}</div></div>'
def page(i,s,plat):
    # tweak: imgtext on IG uses smaller text sizes
    pv={'ig':'--gcols:2;--gih:40px;--ap:40px 36px;--ag:22px;--aw:200px;--wkw:100%;--cw:84px','st':'--gcols:2;--gih:40px;--ap:44px 36px;--ag:26px;--aw:250px;--wkw:100%;--cw:92px','tg':'--gcols:3;--gih:30px;--ap:22px 40px;--ag:40px;--aw:130px;--wkw:46%;--cw:64px','x':'--gcols:3;--gih:30px;--ap:26px 50px;--ag:46px;--aw:160px;--wkw:46%;--cw:76px'}[plat]
    extra=(('.body{line-height:1.65!important}') if plat=='tg' else '')+':root{'+pv+'}'+('.pg{display:none}' if plat=='st' else '')+'.body{font-size:calc(var(--fb)*1.2)}h2{font-size:calc(var(--ft)*1.12)}'
    if plat in('tg','x'): extra+='.mkc{width:52%;padding:12px 20px;gap:4px}.mkp{padding:12px 22px;line-height:1.8}.gp{padding:10px}.gt{padding:5px 10px}.gh{margin-bottom:6px}.gg{gap:8px}.car{margin:-4px 0 -2px}'
    if plat=='ig' and s['k'] in('imgtext','imgverse'): extra='.body{font-size:33px;line-height:1.85}h2{font-size:56px}.verse.sm{font-size:37px}.kick{font-size:26px}'
    if plat=='ig' and s['k']=='chain' and len(s['chain'])>3: extra+='.node{padding:8px 20px}.chain{gap:10px}.node .w{font-size:36px}'
    return f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><style>{CSS}:root{{{VARS[plat]}}}{extra}</style></head><body>{html(i,s,plat)}</body></html>'
if __name__=='__main__':
    only=[1] if 'card' in sys.argv else ([int(x) for x in sys.argv[1:]] or range(1,N+1))
    PL=lambda i:[p for p in SIZES if p!='st' and not (p=='x' and i not in XS)]+(['st'] if i==1 else [])
    os.makedirs('out',exist_ok=True)
    over=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for i in only:
            s=S[i-1]
            for plat in PL(i):
                W,H=SIZES[plat]
                open(f'out/_s{i}_{plat}.html','w').write(page(i,s,plat))
                pg=b.new_page(viewport={'width':W,'height':H})
                pg.goto(f'file://{os.getcwd()}/out/_s{i}_{plat}.html'); pg.wait_for_timeout(300)
                bad=pg.evaluate("""()=>{const m=document.querySelector('.main');const p=document.querySelector('.panel');const r=[];if(m&&m.scrollHeight>m.clientHeight+2)r.push('main');if(p&&p.scrollHeight>p.clientHeight+2)r.push('panel');const sl=document.querySelector('.slide');if(sl.scrollHeight>sl.clientHeight+2||sl.scrollWidth>sl.clientWidth+2)r.push('slide');return r}""")
                if bad: over.append((i,plat,bad))
                pg.screenshot(path=f'out/s{i:02d}_{plat}.png',clip={'x':0,'y':0,'width':W,'height':H}); pg.close()
        b.close()
    print('overflow:',over)
