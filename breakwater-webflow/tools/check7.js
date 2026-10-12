(function(){ try {
  function base(el){var s=document.createElement("span");s.style.cssText="display:inline-block;width:0;height:0;vertical-align:baseline";el.appendChild(s);var b=s.getBoundingClientRect().bottom;s.remove();return b}
  var out={W:innerWidth};
  var wl=document.querySelectorAll('.wwd-title .line'), sr=document.querySelector('.slot-wwd').getBoundingClientRect();
  out.shopBaselineMinusPhotoBottom=(base(wl[4])-sr.bottom).toFixed(2);
  var notch=parseFloat(document.querySelector('.slot-wwd').style.getPropertyValue('--notch'));
  out.notchPct=notch; out.orientedBaselineMinusStep=(base(wl[2])-(sr.top+sr.height*notch/100)).toFixed(2);
  out.titleTop=document.querySelector('.wwd-title').style.getPropertyValue('--wt');
  var p1=document.querySelector('.wwd-hero .p1').getBoundingClientRect(), wt=document.querySelector('.wwd-title').getBoundingClientRect(); out.titleBottomToP1=(p1.top-wt.bottom).toFixed(1);
  var sl=document.querySelectorAll('.start-title .line'), ss=document.querySelector('.slot-start').getBoundingClientRect(); out.startBaselineMinusPhotoBottom=(base(sl[sl.length-1])-ss.bottom).toFixed(2);
  var srows=document.querySelector('.srows').getBoundingClientRect(); out.photoBottomToRows=(srows.top-ss.bottom).toFixed(1);
  out.sizes={ppara:getComputedStyle(document.querySelector('.ppara')).fontSize, agendaBody:getComputedStyle(document.querySelector('.agenda-body')).fontSize, meta:getComputedStyle(document.querySelector('.agenda-meta')).fontSize, sdesc:getComputedStyle(document.querySelector('.sdesc')).fontSize, faq:getComputedStyle(document.querySelector('.faq-rich')).fontSize, ptitle:getComputedStyle(document.querySelector('.ptitle')).fontSize};
  var items=[...document.querySelectorAll('.faq-item')]; out.faqBorders=items.map(i=>getComputedStyle(i).borderTopWidth+'/'+getComputedStyle(i).borderBottomWidth); out.listBottom=getComputedStyle(document.querySelector('.faq-list')).borderBottomWidth;
  var pt=document.querySelector('.prong-tabs').getBoundingClientRect(), ptl=document.querySelector('.ptitle.on')||document.querySelector('.ptitle'); var pr=ptl.getBoundingClientRect(); out.tabsPanel=[Math.round(pt.height), Math.round(pr.bottom-pt.top)];
  return JSON.stringify(out);
} catch(e){ return 'ERR '+e; } })()
