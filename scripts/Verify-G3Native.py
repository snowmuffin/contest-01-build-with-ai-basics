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

# G3 extends the same bounded, test-owned native harness used by G0.
OUT=Path(os.environ.get('AQUARIUM_TEST_OUTPUT',str(ROOT/'artifacts/g3/native')));OUT.mkdir(parents=True,exist_ok=True);STATE=OUT/'state.json'
report={'kind':'G3 live-host lifecycle checks','checks':[],
        'scope':'Actual WPF host + owned Win32 fixtures; selected native notifications are explicitly simulated.'}
api(u,'GetWindowThreadProcessId',w.DWORD,[w.HWND,c.POINTER(w.DWORD)])
api(u,'IsWindowVisible',w.BOOL,[w.HWND]);api(u,'IsWindow',w.BOOL,[w.HWND])
api(u,'RegisterWindowMessageW',w.UINT,[w.LPCWSTR])
ENUM=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
api(u,'EnumWindows',w.BOOL,[ENUM,w.LPARAM])
initial_foreground=u.GetForegroundWindow()
app=None;pointer_moved=False;saved_cursor=w.POINT();u.GetCursorPos(c.byref(saved_cursor))

def pidof(h):
 value=w.DWORD();u.GetWindowThreadProcessId(h,c.byref(value));return value.value

def classof(h):
 b=c.create_unicode_buffer(256);u.GetClassNameW(h,b,256);return b.value

def own_windows(pid):
 result=[]
 @ENUM
 def cb(h,l):
  if pidof(h)==pid:result.append(h)
  return True
 u.EnumWindows(cb,0);return result

def safe_move(p,allowed):
 if pidof(u.GetForegroundWindow()) not in [os.getpid(),app.pid] and u.GetForegroundWindow()!=initial_foreground:
  raise RuntimeError('User foreground changed; aborting controlled input')
 if target_root(p) not in allowed:raise RuntimeError('Target is not test-owned; aborting controlled input')
 u.SetCursorPos(round(p[0]),round(p[1]));time.sleep(.10)

def fixture_click():
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


def tray_action(label):
 global pointer_moved
 pointer_moved=True
 # A test-only notification callback opens the actual NotifyIcon menu. Production has no test command endpoint.
 candidates=[h for h in own_windows(app.pid) if classof(h).startswith('WindowsForms10.Window') and not u.IsWindowVisible(h)]
 if not candidates:raise RuntimeError('NotifyIcon native window not found')
 for h in candidates:u.PostMessageW(h,0x800,0,0x205)
 s=wait_until(lambda s:bool(s.get('trayMenu')),timeout=4)
 item=next(x for x in s['trayMenu']['items'] if x['text']==label)
 r=item['bounds'];point=(r['X']+r['Width']/2,r['Y']+r['Height']/2)
 click(point,[s['trayMenu']['handle']])
 return candidates

def pick_up():
 global pointer_moved
 s=wait_until(lambda s:s['feederVisible']);p=s['feederPosition'];sc=s['transform']['Scale']
 at=((p['X']+40)*sc,(p['Y']+55)*sc)
 pointer_moved=True;safe_move(at,[s['feederHandle']]);send(2)
 return wait_until(lambda s:s['feederMode']=='Held' and s['nativeCaptureOwned']),at

def open_feeder_over_fixture(exe):
 # Open only after the pointer is on the owned work window, rather than under
 # a protected shell surface left beneath the user's pre-test pointer.
 candidates=[(int(display_w*f),int(max(140,display_h*.25))) for f in [.45,.6,.3]]
 point=next((p for p in candidates if target_root(p)==handles[0]),None)
 if point is None:raise RuntimeError('No safe fixture point to open the feeder')
 safe_move(point,[handles[0]]);time.sleep(.2)
 started=subprocess.run([str(exe),'--feed'],cwd=ROOT,timeout=6)
 if started.returncode!=0:raise RuntimeError('Feeder launcher failed')
 return wait_until(lambda s:s['feederVisible'] and s['feederMode']=='Resting')


try:
 last=LAST(c.sizeof(LAST),0);u.GetLastInputInfo(c.byref(last))
 if ((k.GetTickCount()-last.tick)&0xffffffff)/1000<2:raise RuntimeError('Desktop is active; rerun while idle')
 if STATE.exists():STATE.unlink()
 exe=Path(os.environ.get('AQUARIUM_TEST_EXE',str(ROOT/'src/Aquarium.Windows/bin/Release/net10.0-windows/Aquarium.Windows.exe'))).resolve()
 if not exe.is_relative_to(ROOT) or not exe.is_file():raise RuntimeError('Test executable must be an existing project artifact')
 app=subprocess.Popen([str(exe),'--diagnostics',str(STATE),'--probe-seconds','65'],cwd=ROOT)
 s=wait_until(lambda s:s.get('alive') and len(s.get('fish') or [])==5,6)
 check('actual feeding host is running',s['foodImplemented'] and s['pid']==app.pid)
 display_w=round(s['display']['Width']);display_h=round(s['display']['Height'])
 boxes=[(0,80,display_w,display_h-160)]
 threading.Thread(target=fixture_thread,daemon=True).start();ready.wait(3)
 check('controlled real work window created',len(handles)==1,error);A=handles[0]
 pointer_moved=True;fixture_click();time.sleep(.3)
 check('work fixture foreground established',u.GetForegroundWindow()==A)
 s=open_feeder_over_fixture(exe)
 tray_ids=tray_action('Hide');s=wait_until(lambda s:s['manualHidden'] and not s['overlayVisible'])
 check('actual tray Hide removes both surfaces',not s['feederVisible'])
 sim=s['simulationTime'];frames=s['frames'];time.sleep(.8);s=state()
 check('manual Hide freezes drawing and simulation',s['frames']==frames and s['simulationTime']==sim,{'frame_before':frames,'frame_after':s['frames'],'time_before':sim,'time_after':s['simulationTime']})
 second=subprocess.run([str(exe),'--feed'],cwd=ROOT,timeout=6);s=state()
 check('feeder launch cannot override manual Hide',second.returncode==0 and s['manualHidden'] and not s['overlayVisible'])
 fixture_click();u.PostMessageW(A,0x8011,0,0);s=wait_until(lambda s:'Fullscreen' in s['suppression'])
 check('fullscreen protection coexists with manual Hide',s['manualHidden'] and not s['overlayVisible'])
 u.PostMessageW(A,0x8012,0,0);s=wait_until(lambda s:'Fullscreen' not in s['suppression'])
 check('fullscreen exit does not undo manual Hide',s['manualHidden'] and not s['overlayVisible'])
 tray_action('Show again');s=wait_until(lambda s:s['overlayVisible'] and s['feederVisible'])
 check('tray Show restores only a resting feeder',s['feederMode']=='Resting' and not s['nativeCaptureOwned'])
 s,at=pick_up();emitted=s['emitted'];u.PostMessageW(s['feederHandle'],0x001f,0,0)
 s=wait_until(lambda s:s['feederMode']=='Resting' and not s['nativeCaptureOwned']);send(4)
 check('WM_CANCELMODE releases captured feeder',not s['feederCapture'] and s['emitted']==emitted)
 s,at=pick_up();u.SetForegroundWindow(A);time.sleep(.25)
 check('external work window gains focus for interruption test',u.GetForegroundWindow()==A)
 s=wait_until(lambda s:s['feederMode']=='Resting');send(4)
 check('deactivation cancels held input',not s['nativeCaptureOwned'])
 s,at=pick_up();before=s['emitted']
 # A real foreign fullscreen transition occurs while the left button is still down.
 u.SetForegroundWindow(A);u.PostMessageW(A,0x8011,0,0)
 s=wait_until(lambda s:'Fullscreen' in s['suppression'] and not s['overlayVisible']);send(4)
 check('fullscreen during holding clears capture and tool',s['feederMode']=='Resting' and not s['feederVisible'] and not s['nativeCaptureOwned'])
 sim=s['simulationTime'];frames=s['frames'];time.sleep(.8);s=state()
 check('fullscreen stops simulation, redraw and emission',s['simulationTime']==sim and s['frames']==frames and s['emitted']==before)
 u.PostMessageW(A,0x8012,0,0);s=wait_until(lambda s:s['overlayVisible'] and s['feederVisible'])
 check('fullscreen recovery cannot resume old hold',s['feederMode']=='Resting' and s['emitted']==before)
 s,at=pick_up();u.PostMessageW(s['overlayHandle'],0x007e,32,display_w|(display_h<<16))
 s=wait_until(lambda s:s['feederMode']=='Resting' and not s['nativeCaptureOwned']);send(4)
 check('simulated display-change notification cancels drag',not s['feederCapture'])
 s=wait_until(lambda s:s['overlayVisible']);p=s['feederPosition'];scale=s['transform']['Scale']
 check('display-change recovery leaves feeder inside primary display',p['X']>=0 and p['Y']>=0 and p['X']+164<=display_w/scale+1 and p['Y']+112<=display_h/scale+1)
 prior_handle=s['feederHandle'];prior_holds=s['holdCount']
 children=[subprocess.Popen([str(exe),'--feed'],cwd=ROOT) for _ in range(10)]
 codes=[p.wait(timeout=8) for p in children];s=state()
 check('ten rapid launches all receive handled-command acknowledgements',codes==[0]*10,codes)
 check('rapid launches preserve resident, feeder and no automatic pickup',s['pid']==app.pid and s['feederHandle']==prior_handle and s['holdCount']==prior_holds and s['feederMode']=='Resting')
 # Test the framework recovery message on our own icon, without restarting Explorer.
 msg=u.RegisterWindowMessageW('TaskbarCreated')
 for h in tray_ids:u.PostMessageW(h,msg,0,0)
 time.sleep(.3);tray_action('Hide');s=wait_until(lambda s:s['manualHidden'])
 check('simulated TaskbarCreated keeps tray menu usable',s['trayVisible'])
 tray_action('Show again');s=wait_until(lambda s:s['overlayVisible'])
 check('restoration after tray recovery keeps ordinary input',s['feederMode']=='Resting' and not s['nativeCaptureOwned'])
 fixture_click();u.PostMessageW(A,0x8010,0,0);time.sleep(.5);s=state()
 check('ordinary maximize remains distinct from fullscreen',s['overlayVisible'] and 'Fullscreen' not in s['suppression'])
 tray_action('Exit');code=app.wait(timeout=5);s=state()
 check('actual tray Exit terminates the resident normally',code==0 and not s['alive'])
 check('exit stops timer, tray, hooks and capture',not s['timerRunning'] and not s['trayVisible'] and s['eventHooks']==0 and not s['nativeCaptureOwned'])
 check('exit destroys both native windows',not u.IsWindow(s['overlayHandle']) and not u.IsWindow(s['feederHandle']))
 report['all_automated_checks_passed']=True
except Exception as ex:
 report['error']=str(ex);report['all_automated_checks_passed']=False
 if STATE.exists():report['failure_state']=state()
finally:
 if pointer_moved:send(4);u.SetCursorPos(saved_cursor.x,saved_cursor.y)
 for h in handles:u.PostMessageW(h,0x10,0,0)
 if app:
  try:app.wait(timeout=70);report['exit_code']=app.returncode
  except subprocess.TimeoutExpired:report['auto_exit_pending']=True
 if STATE.exists():report['final_state']=state()
 report['environment']={'remote_session':bool(u.GetSystemMetrics(0x1000)),'real_resolution_change_performed':False,'real_session_disconnect_performed':False,'explorer_restarted':False}
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 (OUT/('report-'+str(time.time_ns())+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k not in ['failure_state','final_state']},ensure_ascii=True))
sys.exit(0 if report.get('all_automated_checks_passed') else 1)
