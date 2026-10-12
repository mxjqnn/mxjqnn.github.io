(function(){ try {
  function base(el){var s=document.createElement("span");s.style.cssText="display:inline-block;width:0;height:0;vertical-align:baseline";el.appendChild(s);var b=s.getBoundingClientRect().bottom;s.remove();return b}
  var q=s=>document.querySelector(s), r=s=>q(s).getBoundingClientRect();
  var L=[...document.querySelectorAll('.wwa-title .line')], sr=r('.slot-studio');
  var txt=l=>{var h=l.querySelector('.hl'); if(h) return h.getBoundingClientRect(); var rg=document.createRange(); rg.selectNodeContents(l); return rg.getBoundingClientRect();};
  var t=L.map(txt);
  var nx=parseFloat(q('.slot-studio').style.getPropertyValue('--nx'))/100*sr.width+sr.left, ny=parseFloat(q('.slot-studio').style.getPropertyValue('--ny'))/100*sr.height+sr.top;
  var gapTop=t[3].top-ny, gapRight=nx-t[3].right, gapAbovePE=t[4].top-sr.bottom;
  return JSON.stringify({rightEdges:[t[0].right,t[1].right,t[2].right].map(x=>x.toFixed(1)), imgLeftMinusAIright:(sr.left-t[2].right).toFixed(1),
    stepBottomMinusAIbaseline:(ny-base(L[2])).toFixed(2), imgBottomMinusKMbaseline:(sr.bottom-base(L[3])).toFixed(2),
    gaps:[gapTop.toFixed(1),gapRight.toFixed(1),gapAbovePE.toFixed(1)], fillTouch:[(t[3].top-t[2].bottom).toFixed(1),(t[4].top-t[3].bottom).toFixed(1)],
    peRight:t[4].right.toFixed(1), imgRight:sr.right.toFixed(1), intro:getComputedStyle(q('.pgroup-intro')).transform});
} catch(e){ return 'ERR '+e; } })()
