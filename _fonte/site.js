(function(){
  var root=document.documentElement, b=document.getElementById('tema');
  if(b) b.addEventListener('click',function(){
    var cur=root.getAttribute('data-theme');
    var dark=cur? cur==='dark' : !window.matchMedia('(prefers-color-scheme: light)').matches;
    var novo=dark?'light':'dark'; root.setAttribute('data-theme',novo);
    try{localStorage.setItem('tnp-tema',novo);}catch(x){}
  });
  var fil=document.querySelector('.filters');
  if(fil){
    var chips=fil.querySelectorAll('.chip'), posts=document.querySelectorAll('#lista .post');
    function render(q){
      posts.forEach(function(p){p.hidden=!(q==='todos'||p.dataset.q===q);});
      chips.forEach(function(c){c.setAttribute('aria-pressed',c.dataset.q===q?'true':'false');});
    }
    chips.forEach(function(c){c.addEventListener('click',function(){render(c.dataset.q);});});
    render('todos');
  }
  var f=document.getElementById('contato');
  if(f){
    var t0=Date.now(), st=document.getElementById('c-status'), btn=document.getElementById('c-btn');
    var URL_CONTATO='https://tecnlogianapratica.app.n8n.cloud/webhook/tnp-contato';
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var d={}; new FormData(f).forEach(function(v,k){d[k]=String(v).trim();}); d.t=Date.now()-t0;
      st.className='status mono';
      if(!d.nome||!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)||(d.mensagem||'').length<6){
        st.textContent='Preencha nome, um e-mail válido e a mensagem.'; st.classList.add('err'); return;
      }
      btn.disabled=true; st.textContent='Enviando...';
      fetch(URL_CONTATO,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
        .then(function(r){return r.json().catch(function(){return {};}).then(function(j){return {ok:r.ok&&j.ok!==false};});})
        .then(function(r){
          if(r.ok){f.reset(); st.textContent='Mensagem enviada. O Bruno responde por e-mail.'; st.classList.add('ok');}
          else{st.textContent='Não deu para enviar agora. Tente de novo em instantes.'; st.classList.add('err');}
        })
        .catch(function(){st.textContent='Sem conexão com o servidor. Tente de novo em instantes.'; st.classList.add('err');})
        .then(function(){btn.disabled=false;});
    });
  }
})();
