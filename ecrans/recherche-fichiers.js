(() => {
  const panel = document.createElement('details');
  panel.style.cssText = 'position:fixed;right:16px;top:12px;z-index:10000;background:#202a30;color:#fff;border:1px solid #87999f;border-radius:8px;padding:10px;max-width:min(380px,90vw);font:14px system-ui;box-shadow:0 3px 16px #0006';
  const summary = document.createElement('summary'); summary.textContent = 'Fichiers de recherche'; panel.append(summary);
  const note = document.createElement('p'); note.textContent = 'Partagés entre les deux joueurs · 20 Mo par fichier · sources à vérifier.'; panel.append(note);
  const label = document.createElement('label'); label.textContent = 'Ajouter des fichiers ';
  const input = document.createElement('input'); input.type = 'file'; input.multiple = true; input.style.maxWidth = '100%'; label.append(input); panel.append(label);
  const status = document.createElement('p'); status.setAttribute('role', 'status'); panel.append(status);
  const refresh = document.createElement('button'); refresh.textContent = 'Actualiser'; panel.append(refresh);
  const list = document.createElement('ul'); list.style.cssText = 'max-height:40vh;overflow:auto;padding-left:20px'; panel.append(list);
  document.body.append(panel);
  async function reload() {
    const response = await fetch('/recherche-fichiers'); const data = await response.json();
    if (!response.ok) throw new Error(data.erreur);
    list.replaceChildren();
    for (const f of data.fichiers) {
      const li = document.createElement('li'); const a = document.createElement('a');
      a.textContent = f.nom; a.href = '/recherche-fichiers/' + f.id; a.style.color = '#a8e5ff'; a.download = f.nom;
      li.append(a, document.createTextNode(` — ${Math.ceil(f.taille / 1024)} Ko · ${f.auteur} · à vérifier`)); list.append(li);
    }
    if (!data.fichiers.length) list.textContent = 'Aucun fichier déposé.';
  }
  refresh.onclick = () => reload().catch(e => { status.textContent = e.message; });
  panel.addEventListener('toggle', () => { if (panel.open) refresh.onclick(); });
  input.onchange = async () => {
    input.disabled = true; let count = 0;
    try {
      for (const file of input.files) {
        if (file.size > 20 * 1024 * 1024) throw new Error(file.name + ' dépasse 20 Mo.');
        status.textContent = 'Envoi de ' + file.name + '…';
        const response = await fetch('/recherche-fichiers', { method: 'POST', headers: { 'X-Recherche-Upload': '1', 'X-Fichier-Nom': encodeURIComponent(file.name), 'Content-Type': 'application/octet-stream' }, body: file });
        const data = await response.json(); if (!response.ok) throw new Error(data.erreur); count++;
      }
      status.textContent = count + ' fichier(s) enregistré(s).';
    } catch (e) { status.textContent = count + ' enregistré(s). ' + e.message; }
    finally { input.disabled = false; input.value = ''; await reload().catch(e => { status.textContent += ' ' + e.message; }); }
  };
})();
