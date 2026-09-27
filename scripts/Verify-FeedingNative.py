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
OUT=Path(os.environ.get('AQUARIUM_TEST_OUTPUT',str(ROOT/'artifacts/feeding/native')));OUT.mkdir(parents=True,exist_ok=True)
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

report={'kind':'actual feeding against test-owned native windows, not learner acceptance','checks':[],'input_scope':'test-owned windows and the G0 feeder only','screenshots':'own fixture client area only'}
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
  wc=WC(0,proc,0,0,instance,None,None,brush,None,'AquariumFeedingNativeFixture')
  if not u.RegisterClassW(c.byref(wc)):raise c.WinError(c.get_last_error())
  for i,b in enumerate(boxes):
   h=u.CreateWindowExW(0,wc.name,'Aquarium feeding controlled fixture '+str(i),0x10cf0000,*b,None,None,instance,None)
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


def activate_fixture():
 # Stage only our temporary fixture. Restore an ordinary (non-topmost) window
 # before evaluating the aquarium; never resize/minimize the user's windows.
 bounds=w.RECT();u.GetWindowRect(handles[0],c.byref(bounds))
 candidates=[(x,y) for y in range(bounds.top+40,bounds.bottom-12,40)
                    for x in range(bounds.left+14,bounds.right-12,40)]
 point=next((p for p in candidates if target_root(p)==handles[0]),None)
 temporary_topmost=False
 try:
  if point is None:
   if not u.SetWindowPos(handles[0],-1,0,0,0,0,0x13):raise RuntimeError('Fixture staging failed')
   temporary_topmost=True;time.sleep(.2)
   point=next((p for p in candidates if target_root(p)==handles[0]),None)
  if point is None:raise RuntimeError('No exposed fixture point; no foreign input sent')
  click(point,[handles[0]])
 finally:
  if temporary_topmost:
   u.SetWindowPos(handles[0],-2,0,0,0,0,0x13);time.sleep(.25)
 if u.GetForegroundWindow()!=handles[0]:raise RuntimeError('Fixture did not become foreground')


def pick_up(lift=0):
 s=wait_until(lambda s:s['feederVisible'] and s['feederMode']=='Resting' and not s.get('feederFalling',False),timeout=6)
 fp=s['feederPosition'];sc=s['transform']['Scale'];hit=s.get('feederBodyPoint',{'X':40,'Y':55})
 at=(round((fp['X']+hit['X'])*sc),round((fp['Y']+hit['Y'])*sc))
 safe_move(at,[s['feederHandle']]);send(2)
 s=wait_until(lambda s:s['feederMode']=='Held' and s['nativeCaptureOwned'])
 if lift:
  at=(at[0],max(round(100*sc),at[1]-round(lift*sc)))
  if u.GetForegroundWindow()!=s['feederHandle']:raise RuntimeError('Foreground changed before lifting feeder')
  u.SetCursorPos(*at);time.sleep(.3);s=state()
 return s,at


initial_foreground=u.GetForegroundWindow()
app=None;saved_cursor=w.POINT();u.GetCursorPos(c.byref(saved_cursor));pointer_moved=False

def open_feeder_over_fixture(exe):
 # Open only after the pointer is on the owned work window, rather than under
 # a protected shell surface left beneath the user's pre-test pointer.
 candidates=[(int(display_w*f),int(max(140,display_h*.25))) for f in [.45,.6,.3]]
 point=next((p for p in candidates if target_root(p)==handles[0]),None)
 if point is None:raise RuntimeError('No safe fixture point to open the feeder')
 safe_move(point,[handles[0]]);time.sleep(.2)
 started=subprocess.run([str(exe),'--feed'],cwd=ROOT,timeout=6)
 if started.returncode!=0:raise RuntimeError('Feeder launcher failed')
 opened=wait_until(lambda s:s['feederVisible'] and s['feederMode']=='Resting')
 landed=wait_until(lambda s:not s.get('feederFalling',False),timeout=6)
 if 'feederFalling' in opened:
  check('unheld feeder falls and lands above the taskbar',landed['feederPosition']['Y']>opened['feederPosition']['Y'] and abs(landed['feederPosition']['Y']+landed['feederSize']['Height']-landed['workArea']['Bottom'])<1,{'opened':opened['feederPosition'],'landed':landed['feederPosition']})
  check('falling neither captures input nor emits food',not landed['nativeCaptureOwned'] and landed['emitted']==opened['emitted'])
 return landed


try:
 last=LAST(c.sizeof(LAST),0);u.GetLastInputInfo(c.byref(last));idle=((k.GetTickCount()-last.tick)&0xffffffff)/1000
 if idle<2:raise RuntimeError('Desktop recently active; rerun only while idle')
 if STATE.exists():STATE.unlink()
 exe=Path(os.environ.get('AQUARIUM_TEST_EXE',str(ROOT/'src/Aquarium.Windows/bin/Release/net10.0-windows/Aquarium.Windows.exe'))).resolve()
 if not exe.is_relative_to(ROOT) or not exe.is_file():raise RuntimeError('Test executable must be an existing project artifact')
 app=subprocess.Popen([str(exe),'--diagnostics',str(STATE),'--probe-seconds','45'],cwd=ROOT)
 time.sleep(1.5);s=wait_until(lambda s:s.get('foodImplemented') and len(s.get('fish') or [])==5)
 check('actual world has five fish, no G0 markers substituted',s['stage'].startswith('G1/G2') and s['foodImplemented'])
 scale=s['transform']['Scale'];display_w=round(s['display']['Width']);display_h=round(s['display']['Height'])
 boxes=[(20,30,display_w-40,display_h-100),(40,60,210,130)]
 threading.Thread(target=fixture_thread,daemon=True).start();ready.wait(3)
 check('native test background created',len(handles)==2,error)
 A,B=handles
 u.SetWindowPos(A,None,0,0,0,0,0x13);time.sleep(.3)
 pointer_moved=True;activate_fixture();time.sleep(.5)
 check('actual native fixture is foreground',u.GetForegroundWindow()==A)
 s=open_feeder_over_fixture(exe)
 check('feeder opens resting without food',s['feederMode']=='Resting' and s['emitted']==0)
 if 'feederBodyPoint' in s:
  fp=s['feederPosition'];corner=(round((fp['X']+2)*scale),round((fp['Y']+15)*scale))
  check('transparent feeder padding exposes the work fixture',target_root(corner)==A and rgb(corner)==[43,51,61],rgb(corner))
  old_down=counts.get('down',0);click(corner,[A])
  check('transparent padding passes real clicks to the work fixture',counts.get('down',0)>old_down and state()['holdCount']==0)
  hit=s['feederBodyPoint'];body_pixel=(round((fp['X']+hit['X'])*scale),round((fp['Y']+hit['Y'])*scale))
  check('canister body remains opaque and interactive',target_root(body_pixel)==s['feederHandle'] and rgb(body_pixel)==[91,80,62],rgb(body_pixel))

 # Native input goes to the tool only, not to a simulated world entry point.
 s,body=pick_up();first=s['fish'][0];fp=s['feederPosition'];fh=s['feederHandle']
 point=lambda x,y:(round((x)*scale),round((y)*scale))
 goal=(min(display_w/scale-220,max(80,first['position']['X']+100)),max(80,first['position']['Y']-150))
 delta=((goal[0]-fp['X'])*scale,(goal[1]-fp['Y'])*scale)
 for i in range(1,10):
  if u.GetForegroundWindow()!=fh:raise RuntimeError('Foreground changed during controlled feeder drag')
  u.SetCursorPos(round(body[0]+delta[0]*i/9),round(body[1]+delta[1]*i/9));time.sleep(.04)
 send(4);s=wait_until(lambda s:s['feederMode']=='Resting')
 check('one-way relocation does not dispense',s['emitted']==0,s['emitted'])
 s,body=pick_up(lift=240)
 if 'feederBodyPoint' in s:
  fp=s['feederPosition'];x=round(fp['X']*scale)-16;y=round(fp['Y']*scale)-16;sw=round(80*scale)+32;sh=round(112*scale)+32
  if all(target_root(p)==A for p in [(x,y),(x+sw-1,y),(x,y+sh-1),(x+sw-1,y+sh-1)]):
   screenshot_fixture((x,y,sw,sh),OUT/'feeder-object.png')
 for i in range(18):
  if u.GetForegroundWindow()!=fh:raise RuntimeError('Foreground changed during shake; aborting')
  u.SetCursorPos(body[0]+(60 if i%2 else -60),body[1]);time.sleep(.05)
 s=wait_until(lambda s:s['emitted']>0)
 check('physical held drag emits actual pellets',s['shakes']>0 and len(s['food'])>0,{'shakes':s['shakes'],'emitted':s['emitted'],'pellets':len(s['food'])})
 send(4);s=wait_until(lambda s:s['feederMode']=='Resting' and not s['nativeCaptureOwned']);emitted=s['emitted']
 check('release leaves emitted pellets available',len(s['food'])>0)
 ids=sorted(f['id'] for f in s['fish']);seen_meals=[];deadline=time.monotonic()+10;first_after_emit=s
 while time.monotonic()<deadline:
  s=state();seen_meals.extend(s.get('meals') or [])
  if s['consumed']>0:break
  time.sleep(.08)
 check('fish visibly approaches and consumes live input food',s['consumed']>0,{'consumed':s['consumed'],'emitted':s['emitted'],'simulation_time':s['simulationTime']})
 check('feeding does not create replacement fish',sorted(f['id'] for f in s['fish'])==ids)
 check('normal cursor never emits after release',s['emitted']==emitted)
 check('recorded meals are visible foreground contact',bool(seen_meals) and all(m['Visible'] and m['Band']==2 for m in seen_meals),{'observed_meals':len(seen_meals)})
 check('pellet accounting is consistent',s['emitted']==s['consumed']+s['expired']+len(s['food']))
 # Retain only a crop fully covered by our own opaque background; not user desktop contents.
 f=next((f for f in s['fish'] if f['activity']=='Eat'),s['fish'][0]);fx,fy=point(f['position']['X'],f['position']['Y'])
 x=max(boxes[0][0]+16,min(display_w-700,fx-180));y=max(boxes[0][1]+50,min(display_h-500,fy-180))
 safe_rect=(int(x),int(y),660,410)
 if all(target_root(p)==A for p in [(x+5,y+5),(x+650,y+5),(x+5,y+400),(x+650,y+400)]):
  screenshot_fixture(safe_rect,OUT/'feeding-live.png');report['screenshot']='feeding-live.png (test-owned background only)'
 report['feeding_state']=s
 # Close and re-open through real process activation, still without a direct emission command.
 s=wait_until(lambda s:not s.get('feederFalling',False),timeout=6);fp=s['feederPosition'];hit=s.get('feederClosePoint',{'X':151,'Y':14})
 click(point(fp['X']+hit['X'],fp['Y']+hit['Y']),[fh]);s=wait_until(lambda s:s['feederMode']=='Closed')
 check('X closes only the tool while fish continue',s['overlayVisible'] and len(s['fish'])==5)
 second=subprocess.run([str(exe),'--feed'],cwd=ROOT,timeout=5);s=wait_until(lambda s:s['feederVisible'])
 check('repeat executable activation reuses resident and feeder',second.returncode==0 and s['pid']==app.pid and s['feederHandle']==fh and s['feederMode']=='Resting')
 # Repeat the real input loop with a maximized ordinary work window.
 activate_fixture();u.PostMessageW(A,0x8010,0,0);time.sleep(.7)
 s=wait_until(lambda s:s['overlayVisible'] and s['feederVisible'])
 check('maximized ordinary window still permits live aquarium',s['suppression']=='None')
 before=s['consumed'];s,body=pick_up(lift=240)
 before_emitted=state()['emitted']
 for i in range(16):
  if u.GetForegroundWindow()!=fh:raise RuntimeError('Foreground changed; aborting second shake')
  u.SetCursorPos(body[0]+(60 if i%2 else -60),body[1]);time.sleep(.05)
 send(4);s=wait_until(lambda s:s['feederMode']=='Resting' and s['emitted']>before_emitted)
 s=wait_until(lambda s:s['consumed']>before,timeout=11)
 check('visible consumption also works over maximized window',s['consumed']>before,{'consumed_after':s['consumed'],'consumed_before':before,'total_emitted':s['emitted']})
 check('same five identities after maximized-window feeding',sorted(f['id'] for f in s['fish'])==ids)
 report['maximized_feeding_state']=s
 # Exercise the actual .lnk, not merely a direct executable invocation.
 shortcut=Path(os.environ.get('AQUARIUM_TEST_SHORTCUT',str(ROOT/'artifacts/feeding/shortcuts/Feed Fish.lnk')))
 if not shortcut.is_file():raise RuntimeError('Create the controlled-folder shortcut before running this harness')
 old_report=s['report'];os.startfile(str(shortcut));s=wait_until(lambda s:s['report']>old_report and s['lastEvent']=='open-feeder')
 check('actual feeder shortcut reuses the same resident',s['pid']==app.pid and s['feederHandle']==fh)
 report['all_automated_checks_passed']=True
except Exception as ex:
 report['error']=str(ex);report['all_automated_checks_passed']=False
 if app and STATE.exists():report['failure_state']=state()
finally:
 if pointer_moved:send(4);u.SetCursorPos(saved_cursor.x,saved_cursor.y)
 for h in handles:u.PostMessageW(h,0x10,0,0)
 if app:
  try:app.wait(timeout=45);report['auto_exit_code']=app.returncode
  except subprocess.TimeoutExpired:report['auto_exit_pending']=True
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 (OUT/('report-'+str(time.time_ns())+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({'checks':report['checks'],'passed':report.get('all_automated_checks_passed'),'error':report.get('error'),'screenshot':report.get('screenshot'),'state':report.get('failure_state') or {'consumed':report.get('feeding_state',{}).get('consumed')}},ensure_ascii=True))
sys.exit(0 if report.get('all_automated_checks_passed') else 1)
