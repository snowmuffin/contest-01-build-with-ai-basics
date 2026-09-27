"""Controlled native G0 probe. Only temporary test-owned windows receive synthetic input.
Requires an idle interactive Windows desktop, .NET G0 Release build, and Python stdlib.
Creates no desktop shortcuts, reads no window titles, and never targets the user's apps.
The bounded automation is test infrastructure, not an app feature. Human checks remain required.
"""
from __future__ import annotations
import ctypes as c
from ctypes import wintypes as w
import json, os, struct, subprocess, threading, time, zlib, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/g0/native';OUT.mkdir(parents=True,exist_ok=True)
STATE=OUT/'state.json'
u=c.WinDLL('user32',use_last_error=True);g=c.WinDLL('gdi32');k=c.WinDLL('kernel32');d=c.WinDLL('dwmapi')
LRESULT=c.c_ssize_t
WNDPROC=c.WINFUNCTYPE(LRESULT,w.HWND,w.UINT,w.WPARAM,w.LPARAM)
class WC(c.Structure):
 _fields_=[('style',w.UINT),('proc',WNDPROC),('clsExtra',c.c_int),('wndExtra',c.c_int),('instance',w.HINSTANCE),('icon',w.HICON),('cursor',w.HANDLE),('brush',w.HBRUSH),('menu',w.LPCWSTR),('name',w.LPCWSTR)]
class MI(c.Structure):
 _fields_=[('dx',w.LONG),('dy',w.LONG),('data',w.DWORD),('flags',w.DWORD),('time',w.DWORD),('extra',c.c_size_t)]
class IU(c.Union): _fields_=[('mi',MI),('padding',c.c_byte*32)]
class INPUT(c.Structure): _fields_=[('type',w.DWORD),('u',IU)]
class LAST(c.Structure): _fields_=[('size',w.UINT),('tick',w.DWORD)]
class BI(c.Structure):
 _fields_=[('size',w.DWORD),('width',w.LONG),('height',w.LONG),('planes',w.WORD),('bits',w.WORD),('compression',w.DWORD),('image',w.DWORD),('x',w.LONG),('y',w.LONG),('used',w.DWORD),('important',w.DWORD)]

def api(lib,name,result,args):
 f=getattr(lib,name);f.restype=result;f.argtypes=args;return f
api(u,'SetProcessDpiAwarenessContext',w.BOOL,[c.c_void_p])(-4)
api(u,'DefWindowProcW',LRESULT,[w.HWND,w.UINT,w.WPARAM,w.LPARAM])
api(u,'RegisterClassW',w.ATOM,[c.POINTER(WC)])
api(u,'CreateWindowExW',w.HWND,[w.DWORD,w.LPCWSTR,w.LPCWSTR,w.DWORD,c.c_int,c.c_int,c.c_int,c.c_int,w.HWND,w.HMENU,w.HINSTANCE,c.c_void_p])
api(k,'GetModuleHandleW',w.HMODULE,[w.LPCWSTR])
api(u,'ShowWindow',w.BOOL,[w.HWND,c.c_int]);api(u,'SetForegroundWindow',w.BOOL,[w.HWND])
api(u,'GetWindowRect',w.BOOL,[w.HWND,c.POINTER(w.RECT)]);api(u,'GetClassNameW',c.c_int,[w.HWND,w.LPWSTR,c.c_int]);
api(u,'GetForegroundWindow',w.HWND,[]);api(u,'DestroyWindow',w.BOOL,[w.HWND])
api(u,'GetMessageW',w.BOOL,[c.POINTER(w.MSG),w.HWND,w.UINT,w.UINT]);api(u,'DispatchMessageW',LRESULT,[c.POINTER(w.MSG)])
api(u,'PostMessageW',w.BOOL,[w.HWND,w.UINT,w.WPARAM,w.LPARAM])
api(u,'SetCapture',w.HWND,[w.HWND]);api(u,'ReleaseCapture',w.BOOL,[])
api(u,'WindowFromPoint',w.HWND,[w.POINT]);api(u,'GetAncestor',w.HWND,[w.HWND,w.UINT])
api(u,'GetCursorPos',w.BOOL,[c.POINTER(w.POINT)]);api(u,'SetCursorPos',w.BOOL,[c.c_int,c.c_int])
api(u,'GetLastInputInfo',w.BOOL,[c.POINTER(LAST)]);api(k,'GetTickCount',w.DWORD,[])
api(u,'SendInput',w.UINT,[w.UINT,c.POINTER(INPUT),c.c_int])
api(u,'SetWindowLongPtrW',c.c_ssize_t,[w.HWND,c.c_int,c.c_ssize_t])
api(u,'SetWindowPos',w.BOOL,[w.HWND,w.HWND,c.c_int,c.c_int,c.c_int,c.c_int,w.UINT])
api(u,'GetDC',w.HDC,[w.HWND]);api(u,'ReleaseDC',c.c_int,[w.HWND,w.HDC])
api(g,'CreateSolidBrush',w.HBRUSH,[w.DWORD]);api(g,'GetPixel',w.DWORD,[w.HDC,c.c_int,c.c_int])
api(g,'DeleteObject',w.BOOL,[w.HANDLE]);api(g,'CreateCompatibleDC',w.HDC,[w.HDC])
api(g,'SelectObject',w.HANDLE,[w.HDC,w.HANDLE]);api(g,'DeleteDC',w.BOOL,[w.HDC])
api(g,'CreateDIBSection',w.HBITMAP,[w.HDC,c.POINTER(BI),w.UINT,c.POINTER(c.c_void_p),w.HANDLE,w.DWORD])
api(g,'BitBlt',w.BOOL,[w.HDC,c.c_int,c.c_int,c.c_int,c.c_int,w.HDC,c.c_int,c.c_int,w.DWORD])

report={'kind':'controlled native fixtures, not final user acceptance','checks':[],'input_scope':'test-owned windows and the G0 feeder only','screenshots':'own fixture client area only'}
def check(name,ok,detail=None):
 report['checks'].append({'name':name,'passed':bool(ok),'detail':detail})
 if not ok: raise AssertionError(name+': '+str(detail))
def state():
 for _ in range(20):
  try:return json.loads(STATE.read_text())
  except (OSError,json.JSONDecodeError):time.sleep(.1)
 raise RuntimeError('No diagnostic state')
def wait_until(pred,timeout=4):
 end=time.monotonic()+timeout
 while time.monotonic()<end:
  s=state()
  if pred(s):return s
  time.sleep(.1)
 raise AssertionError('Timed out: '+str(state()))
def rgb(p):
 dc=u.GetDC(0)
 try:
  value=g.GetPixel(dc,round(p[0]),round(p[1]));return [value&255,(value>>8)&255,(value>>16)&255]
 finally:u.ReleaseDC(0,dc)
def chunk(t,data):return struct.pack('!I',len(data))+t+data+struct.pack('!I',zlib.crc32(t+data)&0xffffffff)
def screenshot_fixture(box,path):
 x,y,width,height=map(int,box);dc=u.GetDC(0);mem=g.CreateCompatibleDC(dc);bits=c.c_void_p()
 bi=BI(c.sizeof(BI),width,-height,1,32,0,width*height*4,0,0,0,0)
 bitmap=g.CreateDIBSection(dc,c.byref(bi),0,c.byref(bits),None,0);old=g.SelectObject(mem,bitmap)
 try:
  if not g.BitBlt(mem,0,0,width,height,dc,x,y,0x40cc0020):raise OSError('Capture failed')
  raw=c.string_at(bits,width*height*4);rows=bytearray()
  for row in range(height):
   rows.append(0)
   line=raw[row*width*4:(row+1)*width*4]
   for col in range(width):
    b,gr,r,a=line[col*4:col*4+4];rows.extend((r,gr,b))
  png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b'')
  path.write_bytes(png)
 finally:g.SelectObject(mem,old);g.DeleteObject(bitmap);g.DeleteDC(mem);u.ReleaseDC(0,dc)

handles=[];counts={};ready=threading.Event();error=[];boxes=[]
@WNDPROC
def proc(h,msg,wp,lp):
 try:
  if msg==0x201:counts['down']=counts.get('down',0)+1;u.SetCapture(h);return 0
  if msg==0x202:counts['up']=counts.get('up',0)+1;u.ReleaseCapture();return 0
  if msg==0x200 and wp&1:counts['drag']=counts.get('drag',0)+1;return 0
  if msg==0x20a:counts['wheel']=counts.get('wheel',0)+1;return 0
  if msg==0x8010:u.ShowWindow(h,3);return 0
  if msg==0x8011:
   u.ShowWindow(h,9);u.SetWindowLongPtrW(h,-16,0x90000000);u.SetWindowPos(h,None,0,0,display_w,display_h,0x20);return 0
  if msg==0x8012:
   u.SetWindowLongPtrW(h,-16,0x10cf0000);u.SetWindowPos(h,None,*boxes[0],0x20);return 0
  if msg==0x10:u.DestroyWindow(h);return 0
 except Exception as ex:error.append(str(ex))
 return u.DefWindowProcW(h,msg,wp,lp)
def fixture_thread():
 try:
  instance=k.GetModuleHandleW(None);brush=g.CreateSolidBrush(0x003d332b)
  wc=WC(0,proc,0,0,instance,None,None,brush,None,'AquariumG0NativeFixture')
  if not u.RegisterClassW(c.byref(wc)):raise c.WinError(c.get_last_error())
  for i,b in enumerate(boxes):
   h=u.CreateWindowExW(0,wc.name,'Aquarium G0 controlled fixture '+str(i),0x10cf0000,*b,None,None,instance,None)
   if not h:raise c.WinError(c.get_last_error())
   handles.append(h)
  ready.set();msg=w.MSG()
  while u.GetMessageW(c.byref(msg),None,0,0)>0:u.TranslateMessage(c.byref(msg));u.DispatchMessageW(c.byref(msg))
 except Exception as ex:error.append(str(ex));ready.set()

def target_root(p):return u.GetAncestor(u.WindowFromPoint(w.POINT(round(p[0]),round(p[1]))),2)
def safe_move(p,allowed):
 if u.GetForegroundWindow() not in handles+[state()['feederHandle'],initial_foreground]:raise RuntimeError('User foreground changed; input aborted')
 if target_root(p) not in allowed:raise RuntimeError('Input target is not owned by this test; input aborted')
 u.SetCursorPos(round(p[0]),round(p[1]));time.sleep(.10)
def send(flags,data=0):
 packet=INPUT(0,IU(mi=MI(0,0,data,flags,0,0)))
 if u.SendInput(1,c.byref(packet),c.sizeof(INPUT))!=1:raise c.WinError(c.get_last_error())
def click(p,allowed):safe_move(p,allowed);send(2);time.sleep(.10);send(4);time.sleep(.25)

initial_foreground=u.GetForegroundWindow()
app=None;saved_cursor=w.POINT();u.GetCursorPos(c.byref(saved_cursor));pointer_moved=False
try:
 last=LAST(c.sizeof(LAST),0);u.GetLastInputInfo(c.byref(last));idle=((k.GetTickCount()-last.tick)&0xffffffff)/1000
 if idle<2:raise RuntimeError('Desktop recently active; rerun only while idle')
 if STATE.exists():STATE.unlink()
 exe=ROOT/'src/Aquarium.Windows/bin/Release/net10.0-windows/Aquarium.Windows.exe'
 app=subprocess.Popen([str(exe),'--g0','--feed','--diagnostics',str(STATE),'--probe-seconds','25'],cwd=ROOT)
 time.sleep(2);s=wait_until(lambda s:bool(s['markers']))
 check('process entered interactive session',s['session']>0,{'session':s['session'],'display':s['display'],'scale':s['transform']['Scale']})
 check('passive overlay is layered, noactivate and transparent',(s['overlayExtendedStyle']&0x08080020)==0x08080020)
 scale=s['transform']['Scale'];display_w=round(s['display']['Width']);display_h=round(s['display']['Height'])
 rear,middle,front=s['markers']
 def point(r,dx,dy):return ((r['X']+dx)*scale,(r['Y']+dy)*scale)
 boxes=[tuple(round(v*scale) for v in [rear['X']-50,rear['Y']-65,420,330]),tuple(round(v*scale) for v in [middle['X']-25,middle['Y']-45,98,120])]
 thread=threading.Thread(target=fixture_thread,daemon=True);thread.start();ready.wait(3)
 check('two native fixture windows created',len(handles)==2,error)
 A,B=handles;u.SetWindowPos(A,None,0,0,0,0,0x13);u.SetWindowPos(B,None,0,0,0,0,0x13);time.sleep(.4)
 # Windows may reject background activation; a verified, test-owned click establishes the intended foreground.
 pointer_moved=True;click((boxes[1][0]+35,boxes[1][1]+65),[B]);time.sleep(.7);s=wait_until(lambda s:s['overlayVisible'])
 check('fixture B is actually foremost after controlled click',u.GetForegroundWindow()==B)
 check('passive habitat did not activate its own process',not s['foregroundIsAquarium'],{'fixture_foreground':u.GetForegroundWindow() in handles})
 f=point(front,5,35);mleft=point(middle,5,35);mright=point(middle,115,35);r=point(rear,5,35)
 report['fixture_setup']={'boxes':boxes,'foreground':u.GetForegroundWindow(),'handles':handles,'snapshot':s}
 for hh in handles:
  rr=w.RECT();u.GetWindowRect(hh,c.byref(rr));report['fixture_setup'].setdefault('actual_bounds',[]).append([rr.left,rr.top,rr.right,rr.bottom])
 report['fixture_setup']['sample_roots']=[target_root(v) for v in [f,mleft,mright,r]]
 if any(v not in handles for v in report['fixture_setup']['sample_roots']):
  report['blocked']='A foreign window covers the controlled test region. No input sent; obtain an unobstructed local desktop for the native gate.'
  raise RuntimeError(report['blocked'])
 check('middle clipped where foremost window covers it',rgb(mleft)!=[82,198,175],rgb(mleft))
 check('middle drawn above rear window',rgb(mright)==[82,198,175],rgb(mright))
 check('front drawn above ordinary windows',rgb(f)==[223,129,166],rgb(f))
 check('rear clipped by work window',rgb(r)!=[238,181,96],rgb(r))
 # Both sample points are solid opaque marker pixels. Hit testing must skip the overlay.
 check('opaque marker routes hit test to fixture',target_root(f)==A)
 empty=(boxes[0][0]+15,boxes[0][1]+boxes[0][3]-25)
 check('transparent area routes hit test to fixture',target_root(empty)==A)
 # Capture only the area fully covered by our two fixture windows, not the user's desktop.
 x,y,bw,bh=boxes[0]
 screenshot_fixture((x+10,y+40,bw-20,bh-50),OUT/'fixture-composition.png')
 pointer_moved=True;old_down=counts.get('down',0);click(f,[A]);check('real injected click delivered through opaque overlay',counts.get('down',0)==old_down+1,dict(counts))
 old_wheel=counts.get('wheel',0);safe_move(empty,[A]);send(0x800,120);time.sleep(.2);check('wheel delivered through transparent overlay',counts.get('wheel',0)==old_wheel+1,dict(counts))
 safe_move(f,[A]);send(2);time.sleep(.1);u.SetCursorPos(round(f[0]+20),round(f[1]+12));time.sleep(.2);send(4);time.sleep(.2)
 check('fixture receives drag through passive overlay',counts.get('drag',0)>=1,dict(counts))
 u.SetForegroundWindow(B);time.sleep(.5);check('middle returns when B raised',rgb(mright)==[82,198,175])
 u.SetForegroundWindow(A);time.sleep(.5);check('middle occlusion follows changed order',rgb(mright)!=[82,198,175])
 s=wait_until(lambda s:not s.get('feederFalling',False),timeout=6);fp=s['feederPosition'];feed=(round((fp['X']+40)*scale),round((fp['Y']+55)*scale))
 safe_move(feed,[s['feederHandle']]);send(2);time.sleep(.35)
 s=state();check('feeder owns native capture after deliberate pickup',s['feederMode']=='Held' and s['feederCapture'] and s['nativeCaptureOwned'])
 for n in range(1,5):u.SetCursorPos(round(feed[0]+n*12),round(feed[1]-n*8));time.sleep(.12)
 s=state();check('captured feeder actually moved',s['moveCount']>0 and s['feederPosition']!=fp,{'moves':s['moveCount'],'before':fp,'after':s['feederPosition']})
 send(4);s=wait_until(lambda s:s['feederMode']=='Resting' and not s['feederCapture'])
 check('release clears capture and rests feeder',not s['nativeCaptureOwned'])
 # Move onto a fixture before changing its state. No user window receives input.
 click(empty,[A]);u.PostMessageW(A,0x8010,0,0);time.sleep(.7)
 s=state();check('ordinary maximize does not suppress habitat',s['overlayVisible'],s['suppression'])
 u.PostMessageW(A,0x8011,0,0);time.sleep(.8)
 s=wait_until(lambda s:not s['overlayVisible'])
 check('foreign borderless fullscreen suppresses both surfaces',not s['feederVisible'] and 'Fullscreen' in s['suppression'],s['suppression'])
 frames=s['frames'];time.sleep(.7);check('hidden render count stops',state()['frames']==frames)
 u.PostMessageW(A,0x8012,0,0);time.sleep(.8)
 s=wait_until(lambda s:s['overlayVisible'] and s['feederVisible'])
 check('fullscreen exit restores feeder resting',s['feederMode']=='Resting' and not s['feederCapture'])
 s=wait_until(lambda s:not s.get('feederFalling',False),timeout=6);fp=s['feederPosition'];hit=s.get('feederClosePoint',{'X':151,'Y':14});xp=((fp['X']+hit['X'])*scale,(fp['Y']+hit['Y'])*scale)
 click(xp,[s['feederHandle']]);s=wait_until(lambda s:s['feederMode']=='Closed')
 check('X closes feeder but not habitat',s['overlayVisible'] and not s['feederVisible'])
 second=subprocess.run([str(exe),'--feed'],cwd=ROOT,timeout=5)
 s=wait_until(lambda s:s['feederVisible'])
 check('second launch reuses original process',s['pid']==app.pid and second.returncode==0)
 report['all_automated_checks_passed']=True
except Exception as ex:
 report['error']=str(ex);report['all_automated_checks_passed']=False
 if app and STATE.exists():report['failure_state']=state()
finally:
 # Release only test-generated input, restore the pointer, and remove only test-owned windows.
 if pointer_moved:send(4);u.SetCursorPos(saved_cursor.x,saved_cursor.y)
 for h in handles:u.PostMessageW(h,0x10,0,0)
 report['fixture_input_counts']=counts
 if app:
  try:app.wait(timeout=45);report['auto_exit_code']=app.returncode;report['final_state']=state()
  except subprocess.TimeoutExpired:report['auto_exit_pending']=True
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=True))

sys.exit(0 if report.get("all_automated_checks_passed") else 2 if report.get("blocked") else 1)
