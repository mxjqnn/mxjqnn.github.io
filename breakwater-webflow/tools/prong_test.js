(function(){ try {
  var st=document.querySelector('.prong-stage'), r=st.getBoundingClientRect(), top=r.top+scrollY, range=st.offsetHeight-innerHeight;
  window.__p = {top:top, range:range};
  return JSON.stringify(window.__p);
} catch(e){ return 'ERR '+e; } })()
