using System;
using System.Runtime.InteropServices;
using System.Text;
using Aquarium.Core;

namespace Aquarium.Windows.Platform;

internal static class NativeMethods
{
    internal const int GwlExStyle=-20, GwlStyle=-16;
    internal const long ExTransparent=0x20, ExToolWindow=0x80, ExLayered=0x80000, ExNoActivate=0x08000000;
    internal const uint NoActivate=0x10, NoZOrder=0x4;
    internal const uint WmMouseActivate=0x21, WmDpiChanged=0x02e0, WmDisplayChange=0x7e;
    internal static readonly nint Topmost=new(-1);
    [StructLayout(LayoutKind.Sequential)] internal struct Rect { public int Left,Top,Right,Bottom; public readonly Rect2 ToRect()=>new(Left,Top,Right-Left,Bottom-Top); }
    [StructLayout(LayoutKind.Sequential)] internal struct Point { public int X,Y; public readonly Point2 ToPoint()=>new(X,Y); }
    [StructLayout(LayoutKind.Sequential)] internal struct MonitorInfo { public int Size; public Rect Monitor,Work; public uint Flags; }
    internal delegate bool EnumCallback(nint h,nint l);
    internal delegate void WinEventCallback(nint hook,uint ev,nint hwnd,int objectId,int childId,uint thread,uint time);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool EnumWindows(EnumCallback cb,nint data);
    [DllImport("user32.dll")] internal static extern nint GetTopWindow(nint h);
    [DllImport("user32.dll")] internal static extern nint GetWindow(nint h,uint command);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool IsWindow(nint h);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool IsWindowVisible(nint h);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool IsIconic(nint h);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool IsZoomed(nint h);
    [DllImport("user32.dll")] internal static extern uint GetWindowThreadProcessId(nint h,out uint pid);
    [DllImport("user32.dll",CharSet=CharSet.Unicode)] internal static extern int GetClassName(nint h,StringBuilder name,int size);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool GetWindowRect(nint h,out Rect r);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool GetClientRect(nint h,out Rect r);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool ClientToScreen(nint h,ref Point p);
    [DllImport("user32.dll")] internal static extern nint GetForegroundWindow();
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool GetCursorPos(out Point p);
    [DllImport("user32.dll")] internal static extern short GetAsyncKeyState(int vKey);
    [DllImport("user32.dll")] internal static extern nint WindowFromPoint(Point p);
    [DllImport("user32.dll")] internal static extern nint GetAncestor(nint h,uint flags);
    [DllImport("user32.dll",EntryPoint="GetWindowLongPtrW")] internal static extern nint GetWindowLongPtr(nint h,int index);
    [DllImport("user32.dll",EntryPoint="SetWindowLongPtrW",SetLastError=true)] internal static extern nint SetWindowLongPtr(nint h,int index,nint value);
    [DllImport("user32.dll",SetLastError=true)] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool SetWindowPos(nint h,nint after,int x,int y,int cx,int cy,uint flags);
    [DllImport("user32.dll")] internal static extern nint MonitorFromPoint(Point point,uint flags);
    [DllImport("user32.dll",CharSet=CharSet.Unicode)] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool GetMonitorInfo(nint m,ref MonitorInfo info);
    [DllImport("shcore.dll")] internal static extern int GetDpiForMonitor(nint m,int kind,out uint x,out uint y);
    [DllImport("dwmapi.dll",EntryPoint="DwmGetWindowAttribute")] internal static extern int DwmRect(nint h,int attr,out Rect rect,int size);
    [DllImport("dwmapi.dll",EntryPoint="DwmGetWindowAttribute")] internal static extern int DwmInt(nint h,int attr,out int value,int size);
    [DllImport("shell32.dll")] internal static extern int SHQueryUserNotificationState(out int state);
    [DllImport("user32.dll")] internal static extern nint SetWinEventHook(uint min,uint max,nint module,WinEventCallback callback,uint pid,uint thread,uint flags);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool UnhookWinEvent(nint hook);
    [DllImport("user32.dll")] internal static extern nint GetCapture();
    [DllImport("user32.dll")] internal static extern nint OpenInputDesktop(uint flags,[MarshalAs(UnmanagedType.Bool)] bool inherit,uint access);
    [DllImport("user32.dll",CharSet=CharSet.Unicode)] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool GetUserObjectInformation(nint h,int index,StringBuilder text,int length,out int needed);
    [DllImport("user32.dll")] [return:MarshalAs(UnmanagedType.Bool)] internal static extern bool CloseDesktop(nint h);
    internal static string ClassName(nint h) { var s=new StringBuilder(256); GetClassName(h,s,s.Capacity); return s.ToString(); }
    internal static bool IsOwn(nint h) { GetWindowThreadProcessId(h,out var pid); return pid==(uint)Environment.ProcessId; }
    internal static bool TryBounds(nint h,out Rect2 r)
    {
        if(DwmRect(h,9,out var native,Marshal.SizeOf<Rect>())!=0 && !GetWindowRect(h,out native)) { r=default; return false; }
        r=native.ToRect(); return r.Valid;
    }
    internal static bool TryClient(nint h,out Rect2 r)
    {
        if(!GetClientRect(h,out var local)) {r=default;return false;}
        var p=new Point(); if(!ClientToScreen(h,ref p)){r=default;return false;}
        r=new(p.X,p.Y,local.Right,local.Bottom);return r.Valid;
    }
    internal static bool InputDesktopAvailable()
    {
        var h=OpenInputDesktop(0,false,1); if(h==0)return false;
        try {var name=new StringBuilder(256);return GetUserObjectInformation(h,2,name,512,out _) && name.ToString()=="Default";}
        finally{CloseDesktop(h);}
    }
}
