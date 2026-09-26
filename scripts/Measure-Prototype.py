"""Finite resource check of the real packaged aquarium, using owned native fixtures.
Requires an idle interactive Windows desktop; no screen capture or third-party input.
Sample ordinary, held feeding and hidden states; a failed phase never becomes a pass.
No runtime dependency is added to the application.
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

# Short, explicitly non-isolated performance sample. Not a sustained/battery benchmark.
OUT=Path(os.environ.get('AQUARIUM_TEST_OUTPUT',str(ROOT/'artifacts/g4/performance'))).resolve();
if not OUT.is_relative_to(ROOT/'artifacts'):raise RuntimeError('Measurement output must stay under project artifacts')
OUT.mkdir(parents=True,exist_ok=True);STATE=OUT/'state.json'
duration=float(os.environ.get('AQUARIUM_SAMPLE_SECONDS','5'))
requested_duration=duration
if not 5<=duration<=150:raise RuntimeError('Choose 5 to 150 seconds per phase')
if (OUT/'report.json').exists():raise RuntimeError('Use a new output directory; do not overwrite prior evidence')
report={'kind':'finite same-host Release process sample','checks':[],'samples':[],'requested_phase_seconds':duration}
api(k,'OpenProcess',w.HANDLE,[w.DWORD,w.BOOL,w.DWORD]);api(k,'CloseHandle',w.BOOL,[w.HANDLE])
api(k,'GetProcessTimes',w.BOOL,[w.HANDLE,c.POINTER(w.FILETIME),c.POINTER(w.FILETIME),c.POINTER(w.FILETIME),c.POINTER(w.FILETIME)])
api(k,'GetSystemTimes',w.BOOL,[c.POINTER(w.FILETIME),c.POINTER(w.FILETIME),c.POINTER(w.FILETIME)])
class MEM(c.Structure):
 _fields_=[('cb',w.DWORD),('faults',w.DWORD)]+[(name,c.c_size_t) for name in ['peak_ws','working_set','peak_pool','pool','peak_nonpaged','nonpaged','pagefile','peak_pagefile','private']]
ps=c.WinDLL('psapi');api(ps,'GetProcessMemoryInfo',w.BOOL,[w.HANDLE,c.POINTER(MEM),w.DWORD])
process_handle=None

def ticks(ft):return (ft.dwHighDateTime<<32)|ft.dwLowDateTime

def take(phase):
 idle=w.FILETIME();kernel=w.FILETIME();user=w.FILETIME();k.GetSystemTimes(c.byref(idle),c.byref(kernel),c.byref(user))
 sample={'phase':phase,'wall':time.monotonic(),'system_idle_ticks':ticks(idle),'system_total_ticks':ticks(kernel)+ticks(user)}
 if process_handle:
  created=w.FILETIME();exited=w.FILETIME();p_kernel=w.FILETIME();p_user=w.FILETIME()
  if not k.GetProcessTimes(process_handle,c.byref(created),c.byref(exited),c.byref(p_kernel),c.byref(p_user)):raise c.WinError(c.get_last_error())
  mem=MEM();mem.cb=c.sizeof(MEM)
  if not ps.GetProcessMemoryInfo(process_handle,c.byref(mem),mem.cb):raise c.WinError(c.get_last_error())
  s=state();sample.update(cpu_seconds=(ticks(p_kernel)+ticks(p_user))/1e7,working_set=mem.working_set,private_bytes=mem.private,frames=s['frames'],simulation=s['simulationTime'],food=len(s.get('food') or []),emitted=s['emitted'],consumed=s['consumed'],visible=s['overlayVisible'],render_metrics=s.get('renderMetrics'),expired=s['expired'],fish_ids=sorted(x['id'] for x in s['fish']),display=s['display'],transform=s['transform'])
 report['samples'].append(sample)

def sample_phase(name,duration=5,move=None):
 progress={'phase':name,'pid':app.pid if app else None,'requested_seconds':duration}
 temp=OUT/'phase.json.tmp';temp.write_text(json.dumps(progress),encoding='utf-8');temp.replace(OUT/'phase.json')
 start=time.monotonic();last_sample=-1;i=0
 while time.monotonic()-start<duration:
  if move:move(i);i+=1
  if time.monotonic()-last_sample>=.25:take(name);last_sample=time.monotonic()
  time.sleep(.05)
 take(name)

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
 if ((k.GetTickCount()-last.tick)&0xffffffff)/1000<2:raise RuntimeError('Desktop recently active; do not start synthetic input')
 existing=subprocess.check_output(['powershell.exe','-NoProfile','-Command',"@(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue).Count"],text=True).strip()
 if existing!='0':raise RuntimeError('Close the existing aquarium normally before measuring a new package')
 sample_phase('no-aquarium baseline',4)
 exe=Path(os.environ.get('AQUARIUM_TEST_EXE',str(ROOT/'artifacts/g4/extracted-r2/DesktopAquarium/app/Aquarium.Windows.exe'))).resolve()
 if not exe.is_relative_to(ROOT) or not exe.is_file():raise RuntimeError('Measurement executable must be an existing project artifact')
 if STATE.exists():STATE.unlink()
 app=subprocess.Popen([str(exe),'--diagnostics',str(STATE),'--probe-seconds',str(min(600,int(duration*3+60)))],cwd=ROOT)
 s=wait_until(lambda s:s.get('alive') and len(s.get('fish') or [])==5,6)
 process_handle=k.OpenProcess(0x410,False,app.pid)
 if not process_handle:raise c.WinError(c.get_last_error())
 display_w=round(s['display']['Width']);display_h=round(s['display']['Height'])
 boxes=[(0,80,display_w,display_h-160)]
 threading.Thread(target=fixture_thread,daemon=True).start();ready.wait(3)
 if len(handles)!=1:raise RuntimeError('No controlled performance window')
 A=handles[0];pointer_moved=True;fixture_click();time.sleep(.7)
 s=open_feeder_over_fixture(exe)
 sample_phase('ordinary habitat',duration)
 s,at=pick_up()
 def shake(i):
  if u.GetForegroundWindow()!=s['feederHandle']:raise RuntimeError('User foreground changed; stopping benchmark input')
  u.SetCursorPos(round(at[0]+(55 if i%2 else -55)),round(at[1]))
 sample_phase('held shaking / feeding',duration,shake)
 send(4);wait_until(lambda s:s['feederMode']=='Resting')
 time.sleep(.6);fixture_click();api(u,'AllowSetForegroundWindow',w.BOOL,[w.DWORD])(app.pid);tray_action('Hide');wait_until(lambda s:s['manualHidden'] and not s['overlayVisible'])
 sample_phase('manual hidden',duration)
 measured=[x for x in report['samples'] if 'cpu_seconds' in x]
 for phase in ['ordinary habitat','held shaking / feeding','manual hidden']:
  items=[x for x in measured if x['phase']==phase]
  check(phase+' completed requested interval',len(items)>1 and items[-1]['wall']-items[0]['wall']>=requested_duration*.98)
 check('same five fish identities across all samples',all(x['fish_ids']==measured[0]['fish_ids'] and len(x['fish_ids'])==5 for x in measured))
 check('food cap and conservation hold across all samples',all(0<=x['food']<=64 and x['emitted']==x['consumed']+x['expired']+x['food'] for x in measured))
 hidden=[x for x in measured if x['phase']=='manual hidden']
 check('hidden interval stops rendering simulation and emission',all(not x['visible'] and x['frames']==hidden[0]['frames'] and x['simulation']==hidden[0]['simulation'] and x['emitted']==hidden[0]['emitted'] for x in hidden))
 fixture_click();u.AllowSetForegroundWindow(app.pid);tray_action('Show again');wait_until(lambda s:s['overlayVisible'])
 check('restored after sample without held input',state()['feederMode']=='Resting')
 fixture_click();u.AllowSetForegroundWindow(app.pid);tray_action('Exit');app.wait(timeout=5)
 check('measured package exited normally',app.returncode==0)
 report['passed']=True
except Exception as ex:
 report['passed']=False;report['error']=str(ex)
finally:
 if process_handle:k.CloseHandle(process_handle)
 if pointer_moved:send(4);u.SetCursorPos(saved_cursor.x,saved_cursor.y)
 for h in handles:u.PostMessageW(h,0x10,0,0)
 if app:
  try:app.wait(timeout=55)
  except subprocess.TimeoutExpired:report['exit_pending']=True
 summary=[]
 for name in dict.fromkeys(s['phase'] for s in report['samples']):
  items=[s for s in report['samples'] if s['phase']==name]
  if len(items)<2:continue
  a,b=items[0],items[-1];duration=b['wall']-a['wall'];total=b['system_total_ticks']-a['system_total_ticks']
  row={'phase':name,'seconds':round(duration,2),'whole_system_cpu_percent':round(100*(1-(b['system_idle_ticks']-a['system_idle_ticks'])/total),3) if total else None}
  if 'cpu_seconds' in a:
   row.update(process_cpu_percent_of_all_logical_processors=round((b['cpu_seconds']-a['cpu_seconds'])/duration/os.cpu_count()*100,4),working_set_mib_end=round(b['working_set']/1048576,2),private_mib_start=round(a['private_bytes']/1048576,2),private_mib_end=round(b['private_bytes']/1048576,2),observed_render_fps=round((b['frames']-a['frames'])/duration,2),max_food=max(s['food'] for s in items),emitted_during=b['emitted']-a['emitted'],consumed_during=b['consumed']-a['consumed'])
  summary.append(row)
 report.update(summary=summary,logical_processors=os.cpu_count(),remote_session=bool(u.GetSystemMetrics(0x1000)),diagnostics_enabled=True,gpu_measured=False,per_frame_latency_measured=False,callback_metrics_available=any(x.get('render_metrics') for x in report['samples']),sustained_run=bool(report.get('passed')) and requested_duration>=60)
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k!='samples'},ensure_ascii=True))
sys.exit(0 if report.get('passed') else 1)
