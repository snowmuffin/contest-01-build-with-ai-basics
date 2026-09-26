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

# Isolated-profile Edge test. No existing user tab/profile is opened or controlled.
import winreg
OUT=Path(os.environ.get('AQUARIUM_TEST_OUTPUT',str(ROOT/'artifacts/g3/browser')));OUT.mkdir(parents=True,exist_ok=True);STATE=OUT/'state.json'
report={'kind':'Actual Edge F11 test with a new workspace-local profile','checks':[]}
api(u,'GetWindowThreadProcessId',w.DWORD,[w.HWND,c.POINTER(w.DWORD)])
api(u,'IsWindowVisible',w.BOOL,[w.HWND]);api(u,'IsWindow',w.BOOL,[w.HWND]);api(u,'IsZoomed',w.BOOL,[w.HWND])
ENUM=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM);api(u,'EnumWindows',w.BOOL,[ENUM,w.LPARAM])
app=None;browser=None;owned=[];browser_pids=[];saved=w.POINT();u.GetCursorPos(c.byref(saved));moved=False
class KI(c.Structure):
 _fields_=[('vk',w.WORD),('scan',w.WORD),('flags',w.DWORD),('time',w.DWORD),('extra',c.c_size_t)]
def pidof(h):
 p=w.DWORD();u.GetWindowThreadProcessId(h,c.byref(p));return p.value
def f11(h):
 if u.GetForegroundWindow()!=h or pidof(h) not in browser_pids:raise RuntimeError('F11 target is not the isolated browser')
 for flags in [0,2]:
  key=KI(0x7a,0,flags,0,0);packet=INPUT();packet.type=1;c.memmove(c.addressof(packet.u),c.byref(key),c.sizeof(key))
  if u.SendInput(1,c.byref(packet),c.sizeof(packet))!=1:raise c.WinError(c.get_last_error())
  time.sleep(.05)
try:
 last=LAST(c.sizeof(LAST),0);u.GetLastInputInfo(c.byref(last))
 if ((k.GetTickCount()-last.tick)&0xffffffff)/1000<2:raise RuntimeError('Active user input; browser test paused')
 with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe') as key:
  edge=winreg.QueryValue(key,None)
 profile=OUT/'edge-profile';page=OUT/'fixture.html'
 page.write_text('<!doctype html><meta charset="utf-8"><title>Aquarium G3 isolated test</title><style>body{background:#223746;color:#eef6f8;font:30px sans-serif;padding:50px;min-height:400vh}</style><h1>Aquarium G3 native browser test</h1><p>Temporary isolated profile. This local page has no external resources.</p>',encoding='utf-8')
 if STATE.exists():STATE.unlink()
 exe=Path(os.environ.get('AQUARIUM_TEST_EXE',str(ROOT/'src/Aquarium.Windows/bin/Release/net10.0-windows/Aquarium.Windows.exe'))).resolve()
 if not exe.is_relative_to(ROOT) or not exe.is_file():raise RuntimeError('Expected project-owned test binary')
 app=subprocess.Popen([str(exe),'--feed','--diagnostics',str(STATE),'--probe-seconds','30'],cwd=ROOT)
 wait_until(lambda s:s['alive'] and s['overlayVisible'],5)
 browser=subprocess.Popen([edge,'--user-data-dir='+str(profile),'--no-first-run','--no-default-browser-check','--disable-background-networking','--new-window',page.as_uri()])
 time.sleep(3)
 # Only return identifiers of processes with OUR unique profile directory in their command line.
 escaped=str(profile).replace("'","''")
 command="$p=@(Get-CimInstance Win32_Process -Filter \"Name='msedge.exe'\" | Where-Object {$_.CommandLine -and $_.CommandLine.Contains('"+escaped+"')} | ForEach-Object {$_.ProcessId}); ConvertTo-Json -Compress -InputObject $p"
 result=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True,timeout=10)
 browser_pids=json.loads(result.stdout);browser_pids=browser_pids if isinstance(browser_pids,list) else [browser_pids]
 @ENUM
 def cb(h,l):
  if pidof(h) in browser_pids and u.IsWindowVisible(h):
   name=c.create_unicode_buffer(256);u.GetClassNameW(h,name,256)
   if name.value.startswith('Chrome_WidgetWin'):owned.append(h)
  return True
 u.EnumWindows(cb,0)
 metadata=[]
 for candidate in owned:
  bounds=w.RECT();u.GetWindowRect(candidate,c.byref(bounds));metadata.append({'handle':candidate,'pid':pidof(candidate),'bounds':[bounds.left,bounds.top,bounds.right,bounds.bottom]})
 report['owned_browser_windows']=metadata
 check('isolated-profile Edge window identified',len(owned)>0,{'count':len(owned),'process_count':len(browser_pids)})
 owned.sort(key=lambda handle:next((m['bounds'][2]-m['bounds'][0])*(m['bounds'][3]-m['bounds'][1]) for m in metadata if m['handle']==handle),reverse=True)
 h=owned[0];u.ShowWindow(h,3);u.SetForegroundWindow(h);time.sleep(.5)
 if u.GetForegroundWindow()!=h:
  r=w.RECT();u.GetWindowRect(h,c.byref(r))
  candidates=[(x,y) for y in range(max(180,r.top+180),r.bottom-40,48)
                     for x in range(max(40,r.left+40),r.right-40,48)]
  pt=next((pt for pt in candidates if target_root(pt)==h),None)
  if pt is None:raise RuntimeError('No exposed test-owned browser point; no foreign input sent')
  moved=True;u.SetCursorPos(*pt);send(2);time.sleep(.05);send(4);time.sleep(.3)
 check('only test-owned browser gets F11 input',u.GetForegroundWindow()==h)
 s=wait_until(lambda s:s['overlayVisible']);check('normal maximized Edge keeps habitat visible',u.IsZoomed(h) and 'Fullscreen' not in s['suppression'])
 f11(h);s=wait_until(lambda s:'Fullscreen' in s['suppression'] and not s['overlayVisible'],5)
 check('actual Edge F11 hides fish and feeder',not s['feederVisible'])
 frames=s['frames'];sim=s['simulationTime'];time.sleep(.9);s=state()
 check('Edge fullscreen freezes world and rendering',s['frames']==frames and s['simulationTime']==sim)
 f11(h);s=wait_until(lambda s:s['overlayVisible'] and s['feederVisible'],5)
 check('leaving Edge F11 restores resting feeder',s['feederMode']=='Resting' and not s['nativeCaptureOwned'])
 check('no unsolicited food after fullscreen cycle',s['emitted']==0)
 report['all_automated_checks_passed']=True
except Exception as ex:
 report['error']=str(ex);report['all_automated_checks_passed']=False
 if STATE.exists():report['failure_state']=state()
finally:
 for h in owned:
  if pidof(h) in browser_pids:u.PostMessageW(h,0x10,0,0)
 if moved:send(4);u.SetCursorPos(saved.x,saved.y)
 if browser:
  try:browser.wait(timeout=5)
  except subprocess.TimeoutExpired:report['isolated_profile_process_exit_pending']=True
 if app:
  try:app.wait(timeout=35);report['app_exit_code']=app.returncode
  except subprocess.TimeoutExpired:report['app_exit_pending']=True
 report['browser_launcher_exit_code']=browser.poll() if browser else None
 report['real_session']= 'RDP' if u.GetSystemMetrics(0x1000) else 'local-console'
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k!='failure_state'},ensure_ascii=True))
sys.exit(0 if report.get('all_automated_checks_passed') else 1)
