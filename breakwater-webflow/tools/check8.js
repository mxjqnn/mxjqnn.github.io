(function(){ try {
  var q=function(s){return document.querySelector(s)}, r=function(s){return q(s).getBoundingClientRect()};
  var out={W:innerWidth, docW:document.documentElement.clientWidth};
  var hero=r('.slot-wwd'), start=r('.slot-start');
  out.heroLeft=hero.left.toFixed(1); out.heroRight=(innerWidth-hero.right).toFixed(1); out.heroH=hero.height.toFixed(0);
  out.startLeft=start.left.toFixed(1); out.startRight=(innerWidth-start.right).toFixed(1);
  var p1=r('.wwd-hero .p1'); out.p1Left=p1.left.toFixed(1);
  var pt=r('.prong-title'), pin=r('.prong-pin'), pic=r('.prong-slot .pic');
  out.titleToPhoto=(pic.top-pt.bottom).toFixed(1); out.pinH=pin.height.toFixed(0); out.vh=innerHeight; out.picH=pic.height.toFixed(0);
  var ptl=q('.ptitle.on')||q('.ptitle'); out.ptitleSize=getComputedStyle(ptl).fontSize; out.ptitleToParas=(r('.prong-paras').top-ptl.getBoundingClientRect().bottom).toFixed(1);
  out.pinBottomPad=(pin.bottom-r('.prong-paras').bottom).toFixed(1);
  out.agenda={body:getComputedStyle(q('.agenda-body')).fontSize, meta:getComputedStyle(q('.agenda-meta')).fontSize};
  var row=q('.srow'); var n=r('.srow .snum'), t=r('.srow .srow-title'), d=r('.srow .sdesc');
  out.srow={numLeft:n.left.toFixed(0), titleLeft:t.left.toFixed(0), numBottomToTitle:(t.top-n.bottom).toFixed(1), titleToDesc:(d.top-t.bottom).toFixed(1), arrow:getComputedStyle(q('.sarrow')).display};
  return JSON.stringify(out);
} catch(e){ return 'ERR '+e; } })()
