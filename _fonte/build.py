import json, os, html, re, shutil
# Gera o site do TNP. Fonte: _fonte/ (artigos.json, site.css, site.js). Saida: raiz do repositorio.
# Uso (WSL): cd /mnt/c/Projetos/tnp-site && python3 _fonte/build.py
B=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(B)
os.makedirs(os.path.join(OUT,'assets'),exist_ok=True)
arts=json.load(open(os.path.join(B,'artigos.json'),encoding='utf-8'))
DOM='https://tecnologianapratica.com.br'
SYM='<svg viewBox="0 0 340 200" aria-hidden="true"><path d="M30 44 L76 101 L30 158" fill="none" stroke="currentColor" stroke-width="27" stroke-linecap="round" stroke-linejoin="round"/><rect x="214" y="30" width="103" height="142" rx="51.5" fill="none" stroke="currentColor" stroke-width="27"/><rect x="98" y="163" width="91" height="22" rx="4" fill="#44E07A"/></svg>'
SOL='<svg class="ic-sol" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5.3 5.3l1.7 1.7M17 17l1.7 1.7M5.3 18.7 7 17M17 7l1.7-1.7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><svg class="ic-lua" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
def head(title,desc,path,og='/assets/og.jpg',tipo='website'):
    t=html.escape(title); d=html.escape(desc)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{DOM}{path}">
<meta property="og:type" content="{tipo}">
<meta property="og:site_name" content="Tecnologia na Prática">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{DOM}{path}">
<meta property="og:image" content="{DOM}{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#15302E">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script>try{{var t=localStorage.getItem('tnp-tema');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head>
<body>
'''
def nav(atual):
    itens=[('/','início','home'),('/blog/','blog','blog'),('/materiais/','materiais','materiais'),('/sobre/','sobre','sobre'),('/empresas/','empresas','empresas')]
    a=''.join(f'<a href="{h}"{" aria-current=\"page\"" if k==atual else ""}>{n}</a>' for h,n,k in itens)
    return f'''<header class="top"><div class="wrap">
<a class="brand" href="/" aria-label="Tecnologia na Prática, início">{SYM}<span>TNP</span><span class="sep" aria-hidden="true"></span><span class="nome-marca">Tecnologia na Prática</span></a>
<nav class="menu" aria-label="Seções">{a}</nav>
<button class="theme" id="tema" type="button" aria-label="Trocar entre tema claro e escuro" title="Tema claro ou escuro">{SOL}</button>
</div></header>
<main>
'''
FOOT='''</main>
<footer><div class="wrap">
<div><div class="tag">Simples <span class="hl">assim.</span></div><div class="apoio">Menos hype. Mais prática.</div></div>
<nav class="foot-links mono" aria-label="Rodapé"><a href="/links/">redes</a><a href="/termos.html">termos</a><a href="/privacidade.html">privacidade</a></nav>
</div></footer>
<script src="/assets/site.js" defer></script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "74e68677f70541d39dc59f61ccc2612b"}'></script>
</body>
</html>
'''
def page(path,title,desc,atual,body,**kw):
    p=os.path.join(OUT,path.strip('/'),'index.html') if path.endswith('/') else os.path.join(OUT,path.strip('/'))
    os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf-8').write(head(title,desc,path,**kw)+nav(atual)+body+FOOT)

def card(a):
    return f'''<a class="post" href="/blog/{a['slug']}/"><div class="meta"><span class="q">{html.escape(a['face'])}  {a['quadro']}</span><span>{a['data'][:5]}</span></div><h3>{html.escape(a['titulo'])}</h3><p>{html.escape(a['resumo'])}</p><span class="read">{a['min']} min · ler artigo →</span></a>'''
cards=''.join(card(a) for a in arts)
quadros=[('seg','>_O','Tech Radar'),('ter','O_O','Você Sabia?'),('qua','^_^','Na Prática'),('qui','>_<','Ferramenta da Semana'),('sex','-_-','Resumo TNP'),('sáb','o_O','Pergunta Quente'),('dom','>_O','O Que Vem Por Aí')]
qhtml=''.join(f'<div class="qd"><div class="d">{d}</div><div class="f">{html.escape(f)}</div><div class="n">{n}</div></div>' for d,f,n in quadros)

# HOME
page('/','Tecnologia na Prática · Bruno Lima','Tecnologia de forma simples, em passos que cabem no seu dia. IA, automação e ferramentas traduzidas em o que fazer hoje. Por Bruno Lima, do farol ao CTO.','home',f'''<section class="view"><div class="wrap">
<div class="hero"><div>
<p class="eyebrow">// Tecnologia na Prática · TNP</p>
<h1>Tecnologia de forma simples.<br>Passo a passo que <span class="hl">cabe no seu dia.</span></h1>
<p class="lead">IA, automação, ferramentas e o que muda no trabalho, traduzidos em o que fazer hoje. Sem jargão.</p>
<div class="btns"><a class="btn pri" href="/blog/">Ler o blog →</a><a class="btn" href="/materiais/">Materiais grátis</a></div>
<p class="prompt"><b>&gt;_</b> simples assim.<span class="cursor" aria-hidden="true"></span></p>
</div>
<figure class="perfil"><div class="foto"><img src="/assets/bruno-lima.jpg" alt="Bruno Lima, de óculos, camisa branca e blazer azul-marinho, sobre fundo escuro" width="600" height="1050"><span class="selo mono">&gt;_O TNP</span></div>
<figcaption><strong>Bruno Lima</strong><span class="mono">CTO · do farol ao CTO</span><p>15 anos levando tecnologia para a operação real. Aqui eu conto o que funciona na prática.</p><a href="/sobre/" class="mono">minha história →</a></figcaption></figure>
</div>
<div class="band"><div class="band-head"><h2>Últimas do blog</h2><a href="/blog/">ver tudo →</a></div><div class="posts">{cards}</div></div>
<div class="band"><div class="band-head"><h2>Um quadro por dia</h2><span class="mono faint">grade de 7 dias</span></div><div class="quadros">{qhtml}</div></div>
<div class="band split">
<div class="box"><p class="eyebrow">// para empresas</p><h3>Palestras e consultoria</h3><p>Tecnologia de forma simples para times e lideranças, com a mesma régua do conteúdo: menos hype, mais prática.</p><div class="btns"><a class="btn pri" href="/empresas/">Ver palestras e consultoria →</a></div></div>
<div class="box"><p class="eyebrow">// redes</p><h3>@brunolimatnp em todo lugar</h3><div class="netlinks">
<a href="https://www.instagram.com/brunolimatnp" target="_blank" rel="noopener">Instagram <span>→</span></a>
<a href="https://www.linkedin.com/company/112778648" target="_blank" rel="noopener">LinkedIn · Página TNP <span>→</span></a>
<a href="https://www.youtube.com/@brunolimatnp" target="_blank" rel="noopener">YouTube <span>→</span></a>
<a href="https://www.tiktok.com/@brunolimatnp" target="_blank" rel="noopener">TikTok <span>→</span></a></div></div>
</div></div></section>
''')

# BLOG
chips=''.join(f'<button class="chip" type="button" data-q="{q}">{q}</button>' for q in ['todos']+sorted(set(a['quadro'] for a in arts)))
cards_q=''.join(card(a).replace('<a class="post"',f'<a class="post" data-q="{a["quadro"]}"',1) for a in arts)
page('/blog/','Blog · Tecnologia na Prática','Artigos do TNP: cada post vira um passo a passo, com as fontes e o link para cada rede.','blog',f'''<section class="view"><div class="wrap">
<p class="eyebrow">// blog</p><h1 class="h-page">Cada post, um <span class="hl">passo a passo</span>.</h1>
<p class="sub">Os artigos nascem dos carrosséis aprovados, com as fontes e o link para cada rede.</p>
<div class="filters" role="group" aria-label="Filtrar por quadro">{chips}</div>
<div class="posts" id="lista">{cards_q}</div>
</div></section>
''')

# ARTIGOS
def corpo(a):
    o=[]
    for b in a['corpo']:
        if b[0]=='ul': o.append('<ul>'+''.join(f'<li>{li}</li>' for li in b[1])+'</ul>')
        else: o.append(f'<{b[0]}>{b[1]}</{b[0]}>')
    return '\n'.join(o)
for a in arts:
    sd=os.path.join(OUT,'assets','blog',a['slug']); n=len([f for f in os.listdir(sd) if f.startswith('slide-') and f.endswith('.jpg')]) if os.path.isdir(sd) else 0
    sl=''.join(f'<img class="slide" src="/assets/blog/{a["slug"]}/slide-{i:02d}.jpg" alt="Slide {i} de {n} do carrossel" width="720" height="900" loading="lazy">' for i in range(1,n+1))
    redes=[]
    if a['redes'].get('instagram'): redes.append(f'<a href="{a["redes"]["instagram"]}" target="_blank" rel="noopener">Instagram <span>→</span></a>')
    if a['redes'].get('linkedin'): redes.append(f'<a href="{a["redes"]["linkedin"]}" target="_blank" rel="noopener">LinkedIn <span>→</span></a>')
    mat=f'<div class="box"><h3>Quer o passo a passo em PDF?</h3><p>Baixe o material <b>{a["material"]}</b>.</p><a class="btn pri" href="/materiais/">Ver materiais →</a></div>' if a['palavra'] else ''
    rb=f'<div class="box"><h3>Este post nas redes</h3><div class="netlinks">{"".join(redes)}</div></div>' if redes else ''
    page(f'/blog/{a["slug"]}/',a['titulo']+' · TNP',a['resumo'],'blog',f'''<section class="view"><div class="wrap article">
<article>
<a href="/blog/" class="mono back">← blog</a>
<p class="eyebrow">// {a['quadro']} · {html.escape(a['face'])}</p>
<h1>{html.escape(a['titulo'])}</h1>
<div class="byline"><span>Bruno Lima</span><span>{a['data']}</span><span>{a['min']} min de leitura</span><span>Fonte: {a['fonte']}</span></div>
<div class="slides" aria-label="Slides do carrossel">{sl}</div>
<div class="prose">
{corpo(a)}
<p class="fonte">Fonte: {a['fonte']}</p>
</div>
</article>
<aside class="aside">{mat}{rb}<div class="box"><h3>Fale com o Bruno</h3><p>Palestras e consultoria para o seu time.</p><a class="btn" href="/empresas/">Para empresas →</a></div></aside>
</div></section>
''',tipo='article')

# MATERIAIS
page('/materiais/','Materiais · Tecnologia na Prática','Checklists e guias em PDF que saem dos posts do TNP. Baixe, salve e use hoje.','materiais','''<section class="view"><div class="wrap">
<p class="eyebrow">// materiais</p><h1 class="h-page">O passo a passo <span class="hl">para levar com você.</span></h1>
<p class="sub">Cada material sai de um post e cabe numa página. Baixe, salve e use hoje.</p>
<div class="mats">
<div class="mat"><span class="type">checklist · PDF · 1 página</span><h3>Revise as permissões de IA no seu celular</h3><p>Microfone, câmera, assistentes de voz e o que a IA acessa no trabalho, em 4 passos.</p><div class="btns"><a class="btn pri" href="/materiais/tnp-checklist-permissoes-ia.pdf" download>Baixar PDF</a><a class="mono faint mlink" href="/blog/quando-a-ia-mente/">post de 19/10 →</a></div></div>
<div class="mat"><span class="type">guia · PDF · 2 páginas</span><h3>Começando em tech com IA no meio do caminho</h3><p>As quatro ações do post de 20/10, com exemplos e um plano de 30 dias.</p><div class="btns"><a class="btn pri" href="/materiais/tnp-guia-comecando-em-tech.pdf" download>Baixar PDF</a><a class="mono faint mlink" href="/blog/anthropic-juniores/">post de 20/10 →</a></div></div>
</div></div></section>
''')

# SOBRE
page('/sobre/','Sobre · Do farol ao CTO','A história de Bruno Lima: do panfleto no farol ao cargo de CTO. Por que o TNP existe.','sobre','''<section class="view"><div class="wrap">
<div class="sobre-top"><img src="/assets/bruno-lima.jpg" alt="Bruno Lima" width="600" height="1050"><div>
<p class="eyebrow">// sobre</p><h1 class="h-page">Do farol <span class="hl">ao CTO.</span></h1>
<p class="sub">O TNP mostra tecnologia de forma simples, em passos que você aplica hoje. IA é uma dessas tecnologias, não a única. Para curiosos, profissionais de tech e quem lidera negócios.</p></div></div>
<article class="farol prose"><h2>O farol</h2>
<p>Comecei a trabalhar cedo, como boa parte dos jovens brasileiros. Filho de nordestinos, cresci na periferia da zona leste de São Paulo, num barraquinho de madeira, com uma vontade que nunca passou: ganhar o meu próprio dinheiro e ajudar em casa.</p>
<p>Entreguei panfleto no farol. Carreguei entulho em obra. Fui estagiário em supermercado, balconista de atacado no Brás e auxiliar de ajudante geral, sempre conciliando trabalho e estudo. Já casado, passei por confecção, administrativo e financeiro, até a tecnologia entrar de vez: suporte, sistemas, gerência de projetos, consultoria de implantação, gerência de tecnologia e, hoje, CTO.</p>
<p>São mais de 20 anos de trabalho, e nenhuma dessas etapas foi à toa. Cada uma, curta ou longa, construiu o profissional que eu sou e o homem que me tornei: marido da mulher mais linda do mundo e pai de três lindezas.</p>
<p>Nada disso foi sozinho. Em primeiro lugar, a mão de Deus sempre esteve sobre mim, capacitando e abrindo portas onde não existiam.</p>
<p>O TNP nasce daí: compartilhar o que eu trago na bagagem e abrir uma conversa para a gente crescer junto.</p>
<div class="caminho mono" aria-label="Caminho profissional">panfleto no farol <i>→</i> obra <i>→</i> supermercado <i>→</i> atacado no Brás <i>→</i> confecção <i>→</i> administrativo <i>→</i> financeiro <i>→</i> suporte <i>→</i> sistemas <i>→</i> projetos <i>→</i> implantação <i>→</i> gerência de tecnologia <i>→</i> <b>CTO</b></div>
</article>
<div class="btns cta"><a class="btn pri" href="/empresas/">Falar com o Bruno →</a></div>
</div></section>
''')

# EMPRESAS
page('/empresas/','Palestras e consultoria · TNP','Palestras e consultoria de Bruno Lima: tecnologia de forma simples para times e lideranças. Fale pelo formulário.','empresas','''<section class="view"><div class="wrap">
<p class="eyebrow">// para empresas</p><h1 class="h-page">Tecnologia de forma simples <span class="hl">para o seu time.</span></h1>
<div class="emp-grid">
<div class="box"><p class="eyebrow">palestras</p>
<div class="item"><h3>Tecnologia de forma simples: o que eu posso fazer agora?</h3><p>Um mapa prático das tecnologias que já estão ao alcance do seu time hoje, sem jargão.</p></div>
<div class="item"><h3>IA: o que é, o que come, onde vive?</h3><p>Para quem ouve falar de IA todo dia e quer entender o que ela faz, o que não faz e por onde começar.</p></div></div>
<div class="box"><p class="eyebrow">consultoria · sob consulta</p>
<div class="item"><h3>Diagnóstico de tecnologia</h3><p>Onde a tecnologia ajuda e onde atrapalha a sua operação hoje.</p></div>
<div class="item"><h3>Implantação de automação e IA</h3><p>Do piloto ao uso no dia a dia, com o time junto.</p></div>
<div class="item"><h3>Mentoria para lideranças</h3><p>Decidir sobre tecnologia sem depender de jargão.</p></div></div>
</div>
<form class="contato box" id="contato" novalidate>
<h3>Vamos conversar</h3><p>Conte o que você precisa. A resposta chega por e-mail.</p>
<div class="campos">
<label for="c-nome">Nome<input id="c-nome" name="nome" required autocomplete="name"></label>
<label for="c-email">E-mail<input id="c-email" name="email" type="email" required autocomplete="email"></label>
<label for="c-empresa">Empresa<input id="c-empresa" name="empresa" autocomplete="organization"></label>
<label for="c-assunto">Assunto<select id="c-assunto" name="assunto"><option>Palestra</option><option>Consultoria</option><option>Parceria</option><option>Outro</option></select></label>
<label for="c-msg" class="full">Mensagem<textarea id="c-msg" name="mensagem" rows="5" required></textarea></label>
<input type="text" name="site" id="c-site" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
</div>
<div class="btns"><button class="btn pri" type="submit" id="c-btn">Enviar mensagem</button><span class="status mono" id="c-status" role="status"></span></div>
<p class="nota">Seus dados servem só para responder este contato. Veja a <a href="/privacidade.html">política de privacidade</a>.</p>
</form>
</div></section>
''')

# 404
p404=head('Página não encontrada · TNP','Esta página não existe.','/404.html')+nav('')+'''<section class="view"><div class="wrap nf">
<p class="big mono">o_O</p><h1 class="h-page">Essa página <span class="hl">não existe.</span></h1>
<p class="sub">O link pode estar quebrado ou a página mudou de lugar.</p>
<div class="btns"><a class="btn pri" href="/">Voltar ao início</a><a class="btn" href="/blog/">Ver o blog</a></div>
</div></section>
'''+FOOT
open(os.path.join(OUT,'404.html'),'w',encoding='utf-8').write(p404)

# favicon, robots, sitemap
open(os.path.join(OUT,'favicon.svg'),'w',encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360"><rect width="360" height="360" rx="72" fill="#15302E"/><g transform="translate(10 80)"><path d="M30 44 L76 101 L30 158" fill="none" stroke="#F3EFE6" stroke-width="27" stroke-linecap="round" stroke-linejoin="round"/><rect x="214" y="30" width="103" height="142" rx="51.5" fill="none" stroke="#F3EFE6" stroke-width="27"/><rect x="98" y="163" width="91" height="22" rx="4" fill="#44E07A"/></g></svg>')
open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n')
urls=['/','/blog/','/materiais/','/sobre/','/empresas/','/links/']+[f'/blog/{a["slug"]}/' for a in arts]
open(os.path.join(OUT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{DOM}{u}</loc></url>\n' for u in urls)+'</urlset>\n')
shutil.copy(os.path.join(B,'site.css'),os.path.join(OUT,'assets','site.css'))
shutil.copy(os.path.join(B,'site.js'),os.path.join(OUT,'assets','site.js'))
print('ok', len(arts), 'artigos')
