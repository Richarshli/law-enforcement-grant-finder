const dataUrl = 'data/current/grants.json';
let dataset = {grants:[], sources:[]};
const grantsEl = document.querySelector('#grants');
const categoryEl = document.querySelector('#category');
const statusEl = document.querySelector('#status');
const searchEl = document.querySelector('#search');
const countEl = document.querySelector('#result-count');
const updatedEl = document.querySelector('#last-updated');
const healthEl = document.querySelector('#source-health');

function escapeHtml(value=''){return value.replace(/[&<>'"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}[ch]));}
function render(){
  const q=searchEl.value.toLowerCase().trim();
  const cat=categoryEl.value; const status=statusEl.value;
  const items=dataset.grants.filter(g=>{
    const hay=[g.title,g.agency,g.category,g.summary,...(g.keywords||[])].join(' ').toLowerCase();
    return (!q||hay.includes(q))&&(cat==='all'||g.category===cat)&&(status==='all'||g.status===status);
  });
  countEl.textContent=`${items.length} result${items.length===1?'':'s'}`;
  grantsEl.innerHTML=items.length?items.map(g=>`<article class="card"><span class="badge">${escapeHtml(g.status)}</span><span class="badge">${escapeHtml(g.category)}</span><h3>${escapeHtml(g.title)}</h3><p><strong>Agency:</strong> ${escapeHtml(g.agency)}</p><p>${escapeHtml(g.summary)}</p><p><strong>Deadline:</strong> ${escapeHtml(g.deadline||'See official source')}</p><p><strong>Eligible applicants:</strong> ${escapeHtml(g.eligibility||'See official source')}</p><a href="${g.url}" target="_blank" rel="noopener">View official opportunity</a></article>`).join(''):'<p>No matching grants found.</p>';
}
function renderSources(){healthEl.innerHTML=dataset.sources.map(s=>`<div class="source"><strong>${escapeHtml(s.name)}</strong> — <span class="${s.available?'ok':'warn'}">${s.available?'Available':'Check failed'}</span><br><small>Last checked: ${escapeHtml(s.checked_at||'Not yet checked')}</small></div>`).join('');}
fetch(dataUrl).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();}).then(data=>{
  dataset=data; updatedEl.textContent=`Last updated: ${data.last_updated||'Not yet updated'}`;
  [...new Set(data.grants.map(g=>g.category))].sort().forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;categoryEl.appendChild(o)});
  render();renderSources();
}).catch(err=>{updatedEl.textContent='Update data could not be loaded.';grantsEl.innerHTML=`<p>${escapeHtml(err.message)}</p>`;});
[searchEl,categoryEl,statusEl].forEach(el=>el.addEventListener('input',render));
