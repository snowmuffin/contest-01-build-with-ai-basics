"""Local recording helper for the EXISTING real-input feeding verification.
It records the actual desktop host over an opaque test-owned work window, never
substitutes a browser/fake aquarium, and never uploads or writes narration.
Requires an unlocked idle Windows desktop, FFmpeg, and no running aquarium.
The resulting local rehearsal needs frame-by-frame privacy/content review before use.
"""
from __future__ import annotations
import ctypes as c
from ctypes import wintypes as w
import json, os, shutil, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/pre-submit/demo'
OUT.mkdir(parents=True,exist_ok=True)

def main()->None:
    u=c.WinDLL('user32',use_last_error=True)
    u.GetForegroundWindow.restype=w.HWND
    u.OpenInputDesktop.argtypes=[w.DWORD,w.BOOL,w.DWORD];u.OpenInputDesktop.restype=w.HANDLE
    u.CloseDesktop.argtypes=[w.HANDLE]
    desktop=u.OpenInputDesktop(0,False,1)
    if not desktop or not u.GetForegroundWindow():
        if desktop:u.CloseDesktop(desktop)
        raise RuntimeError('No accessible interactive input desktop. Reconnect/unlock normally; do not weaken security.')
    u.CloseDesktop(desktop)
    ffmpeg=shutil.which('ffmpeg');ffprobe=shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:raise RuntimeError('FFmpeg and ffprobe must already be installed; no automatic install.')
    existing=subprocess.check_output(['powershell.exe','-NoProfile','-Command',"@(Get-Process Aquarium.Windows -ErrorAction SilentlyContinue).Count"],text=True).strip()
    if existing!='0':raise RuntimeError('Exit the existing aquarium via its tray before recording the candidate itself.')
    os.environ['AQUARIUM_TEST_OUTPUT']=str(OUT/'native')
    source=(ROOT/'scripts/Verify-FeedingNative.py').read_text(encoding='utf-8')
    anchor=" check('actual native fixture is foreground',u.GetForegroundWindow()==A)"
    if source.count(anchor)!=1:raise RuntimeError('Verification source changed; inspect recorder hook instead of guessing.')
    video=OUT/('feeding-rehearsal-'+str(time.time_ns())+'.mp4')
    recorder=None;stream=None
    def begin(scope):
        nonlocal recorder,stream
        s=scope['state']();scale=s['transform']['Scale'];fish=s['fish'][0]['position']
        width=min(1280,int(s['display']['Width'])-120);height=min(720,int(s['display']['Height'])-200)
        width-=width%2;height-=height%2
        x=max(50,min(int(fish['X']*scale)-180,int(s['display']['Width'])-width-50))
        y=max(110,min(int(fish['Y']*scale)-260,int(s['display']['Height'])-height-90))
        # Conservative full-window intersection check; never record through an unrelated foreground window.
        api=scope['api'];api(scope['u'],'GetTopWindow',w.HWND,[w.HWND]);api(scope['u'],'GetWindow',w.HWND,[w.HWND,w.UINT]);api(scope['u'],'IsWindowVisible',w.BOOL,[w.HWND])
        api(scope['u'],'GetWindowThreadProcessId',w.DWORD,[w.HWND,c.POINTER(w.DWORD)])
        api(scope['d'],'DwmGetWindowAttribute',c.c_long,[w.HWND,c.c_uint,c.c_void_p,c.c_uint])
        current=scope['u'].GetTopWindow(None);visited=set();saw_fixture=False
        while current:
            if current in visited or len(visited)>4096:raise RuntimeError('Unstable window order; capture aborted')
            visited.add(current)
            if current==scope['A']:saw_fixture=True;break
            pid=w.DWORD();scope['u'].GetWindowThreadProcessId(current,c.byref(pid));cloaked=c.c_int()
            scope['d'].DwmGetWindowAttribute(current,14,c.byref(cloaked),4)
            if scope['u'].IsWindowVisible(current) and not cloaked.value and pid.value not in [os.getpid(),scope['app'].pid]:
                r=w.RECT();scope['u'].GetWindowRect(current,c.byref(r))
                if r.left<x+width and r.right>x and r.top<y+height and r.bottom>y:
                    raise RuntimeError('An unrelated window overlaps the capture rectangle; recording aborted')
            current=scope['u'].GetWindow(current,2)
        if not saw_fixture:raise RuntimeError('Opaque fixture not found under capture region')
        stream=(OUT/'ffmpeg.log').open('wb')
        recorder=subprocess.Popen([ffmpeg,'-hide_banner','-loglevel','warning','-f','gdigrab','-framerate','20',
            '-offset_x',str(x),'-offset_y',str(y),'-video_size',f'{width}x{height}','-draw_mouse','1','-i','desktop',
            '-t','40','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE,stdout=stream,stderr=stream)
        scope['report']['recording']={'file':str(video.relative_to(ROOT)),'capture_rectangle':[x,y,width,height],
            'kind':'actual application and test-owned work window','narration':'none','privacy_review':'pending','public_upload':False}
        time.sleep(.8)
    def end_recording():
        if recorder and recorder.poll() is None:
            try:recorder.communicate(b'q\n',timeout=15)
            except subprocess.TimeoutExpired:recorder.terminate();recorder.wait(timeout=5)
    source=source.replace(anchor,anchor+'\n _recording_begin(globals())',1)
    cleanup='finally:\n if pointer_moved:send(4);u.SetCursorPos(saved_cursor.x,saved_cursor.y)'
    if source.count(cleanup)!=1:raise RuntimeError('Native cleanup hook changed; abort recording')
    # Finish the movie before the opaque fixture is destroyed, including failed test paths.
    source=source.replace(cleanup,'finally:\n _recording_end()\n if pointer_moved:send(4);u.SetCursorPos(saved_cursor.x,saved_cursor.y)',1)
    scope={'__file__':str(ROOT/'scripts/Verify-FeedingNative.py'),'__name__':'__main__','_recording_begin':begin,'_recording_end':end_recording}
    result=0
    try:
        exec(compile(source,'recording_existing_native_verification','exec'),scope)
    except SystemExit as status:
        result=int(status.code or 0)
    finally:
        if recorder:
            if recorder.poll() is None:
                try:recorder.communicate(b'q\n',timeout=15)
                except subprocess.TimeoutExpired:recorder.terminate();recorder.wait(timeout=5)
            if stream:stream.close()
    if result:raise RuntimeError('Feeding verification failed; recording is not accepted evidence')
    if not video.exists():raise RuntimeError('No recording created')
    probe=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_format','-show_streams','-of','json',str(video)]))
    (OUT/'recording-receipt.json').write_text(json.dumps({'path':str(video.relative_to(ROOT)),'media':probe,'review':'pending','uploaded':False},indent=2),encoding='utf-8')
    print(json.dumps({'local_video':str(video),'bytes':video.stat().st_size,'review_required':True,'uploaded':False}))

if __name__=='__main__':
    try:main()
    except Exception as error:
        (OUT/'recording-status.json').write_text(json.dumps({'status':'blocked-or-failed','reason':str(error),'video_accepted':False,'uploaded':False},indent=2),encoding='utf-8')
        raise
