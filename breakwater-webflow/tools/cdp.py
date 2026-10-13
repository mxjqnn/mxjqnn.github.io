# Headless Chrome driver used to test the reference pages: python3 cdp.py <outdir> <url> <width> <height> '<json steps>' [load wait]
# Steps: {"js": "..."} evaluates (result collected), {"wait": s}, {"shot": "name"} saves <outdir>/name.png, {"mouse": [x, y]} moves the pointer, {"cdp": "Method", "params": {...}} sends any CDP command (e.g. Emulation.setFocusEmulationEnabled so :focus works headless).
import asyncio, json, base64, subprocess, time, urllib.request, sys
import websockets
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
S=sys.argv[1]; url=sys.argv[2]; w=int(sys.argv[3]); h=int(sys.argv[4]); steps=json.loads(sys.argv[5])
proc=subprocess.Popen([CH,"--headless=new","--disable-gpu","--remote-debugging-port=9333","--user-data-dir="+S+"/prof",f"--window-size={w},{h}","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(150):
        try: targets=json.load(urllib.request.urlopen("http://localhost:9333/json")); break
        except Exception: time.sleep(0.2)
    else: raise SystemExit("Chrome did not open its debug port in 30s")
    ws_url=[t for t in targets if t["type"]=="page"][0]["webSocketDebuggerUrl"]
    async def main():
        async with websockets.connect(ws_url,max_size=50_000_000) as ws:
            n=[0]
            async def send(m,p=None):
                n[0]+=1; i=n[0]; await ws.send(json.dumps({"id":i,"method":m,"params":p or {}}))
                while True:
                    r=json.loads(await ws.recv())
                    if r.get("id")==i: return r.get("result",{})
            await send("Emulation.setDeviceMetricsOverride",{"width":w,"height":h,"deviceScaleFactor":float(__import__("os").environ.get("DPR","1")),"mobile":False})
            await send("Page.enable"); await send("Runtime.enable")
            await send("Page.navigate",{"url":url}); await asyncio.sleep(float(sys.argv[6]) if len(sys.argv)>6 else 2.5)
            out=[]
            for st in steps:
                if "js" in st:
                    r=await send("Runtime.evaluate",{"expression":st["js"],"awaitPromise":True,"returnByValue":True})
                    out.append(r.get("result",{}).get("value"))
                if "cdp" in st: await send(st["cdp"], st.get("params"))
                if "mouse" in st: await send("Input.dispatchMouseEvent",{"type":"mouseMoved","x":st["mouse"][0],"y":st["mouse"][1]})
                if "wait" in st: await asyncio.sleep(st["wait"])
                if "shot" in st:
                    r=await send("Page.captureScreenshot",{"format":"png"})
                    open(f"{S}/{st['shot']}.png","wb").write(base64.b64decode(r["data"]))
            print(json.dumps(out,indent=1))
    asyncio.run(main())
finally:
    proc.terminate()
