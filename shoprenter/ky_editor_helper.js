window.ky={sleep:ms=>new Promise(r=>setTimeout(r,ms)),BASE:'https://stratoswebdesign.github.io/kontyos/shoprenter/',log:[],
groups(){return [...document.querySelectorAll('.template-list-group')]},
group(n){return this.groups().find(g=>{const h=g.firstElementChild;return h&&h.textContent.trim()===n})},
async openFolder(n){const g=this.group(n);if(!g)throw 'nofolder '+n;if(!g.classList.contains('template-list-group-opened')){g.firstElementChild.click();await this.sleep(800)}return this.group(n)},
cm(){return document.querySelector('.CodeMirror').CodeMirror},
activeName(){const a=document.querySelector('li.theme-editor-tab-list-item.active, .nav-link.active, .active[class*=tab]');return a?a.textContent.trim():''},
async open(f,file){const g=await this.openFolder(f);const a=[...g.querySelectorAll('a.template-list-file')].find(a=>a.textContent.trim()===file);if(!a)throw 'nofile '+f+'/'+file;a.click();for(let i=0;i<40;i++){await this.sleep(250);if(document.querySelector('.CodeMirror')&&this.activeName()===file)break}await this.sleep(900);return this.activeName()+' len'+this.cm().getValue().length},
san(s){return s.replace(/=/g,'≡').replace(/%/g,'％').replace(/&/g,'＆').replace(/;/g,'；')},
lines(a,b){const L=this.cm().getValue().split('\n');return this.san(L.slice(a,b).map((l,i)=>(i+a)+':'+l.trim()).join(' ¶ '))},
grep(re){const L=this.cm().getValue().split('\n');return this.san(L.map((l,i)=>i+':'+l.trim()).filter(l=>re.test(l)).join(' ¶ '))},
assertSandbox(){if(location.host!=='kontyos.sandbox.shoprenter.hu')throw 'NOT SANDBOX '+location.host},
setInput(inp,v){const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;s.call(inp,v);inp.dispatchEvent(new Event('input',{bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}))},
modal(){const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Fájl létrehozása'&&b.offsetParent);if(!b)return null;let p=b;while(p&&!p.querySelector('input'))p=p.parentElement;return p},
async fetchText(p){const r=await fetch(this.BASE+p+'?t='+Date.now(),{cache:'no-store'});if(!r.ok)throw 'fetch '+r.status+' '+p;return r.text()},
toast(){return [...document.querySelectorAll('body *')].filter(e=>e.children.length===0&&/mentése|sikeres|hiba/i.test(e.textContent)&&e.offsetParent).map(e=>e.textContent.trim()).join('|')},
saveBtn(){return [...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Mentés')},
put(text){const cm=this.cm();cm.focus();cm.execCommand('selectAll');cm.replaceSelection(text,'end','+input');window.scrollTo(0,0);document.scrollingElement.scrollTop=0},
async create(f,name,content){this.assertSandbox();const g=await this.openFolder(f);if([...g.querySelectorAll('a.template-list-file')].some(a=>a.textContent.trim()===name+'.tpl'))return 'EXISTS '+name;g.querySelector('a.create-new-template-file').click();let m=null;for(let i=0;i<20&&!m;i++){await this.sleep(200);m=this.modal()}if(!m)return 'NOMODAL';this.setInput(m.querySelector('input'),name);await this.sleep(200);[...m.querySelectorAll('button')].find(b=>b.textContent.trim()==='Fájl létrehozása').click();for(let i=0;i<40;i++){await this.sleep(250);if(this.activeName()===name+'.tpl')break}await this.sleep(600);if(this.activeName()!==name+'.tpl')return 'NOT OPENED '+name+' active:'+this.activeName();this.put(content);await this.sleep(400);window.scrollTo(0,0);return 'created '+name+' len'+this.cm().getValue().length+' btn:'+(/disabled/.test(this.saveBtn().className)?'DIS':'en')},
async prep(name){for(let i=0;i<25&&this.toast();i++)await this.sleep(300);const c=await this.fetchText('snippets/'+name+'.tpl');const r=await this.create('snippets',name,c);this.cur={name,len:c.length,r};window.scrollTo(0,0);return r},
async verify(){let t='';for(let i=0;i<20;i++){await this.sleep(300);t=this.toast();if(t)break}const ok=/sikeres/i.test(t);this.log.push(this.cur.name+':'+(ok?'OK':'FAIL['+t+']'));window.scrollTo(0,0);return this.cur.name+' '+(ok?'OK':'FAIL '+t+' / '+this.cur.r)}};
ky.reput=async function(n){this.assertSandbox();await this.open('snippets',n+'.tpl');const cur=this.cm().getValue();const c=await this.fetchText('snippets/'+n+'.tpl');this.cur={name:n};if(cur===c){this.cur.same=true;return n+' SAME'}this.put(c);for(let i=0;i<25&&/disabled/.test(this.saveBtn().className);i++)await this.sleep(200);window.scrollTo(0,0);return n+' '+(/disabled/.test(this.saveBtn().className)?'DIS':'en')};
ky.verify2=async function(){if(this.cur&&this.cur.same)return this.cur.name+' SAME';return this.verify()};
'helpers ok';
