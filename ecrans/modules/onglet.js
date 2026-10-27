// LE SIÈGE DE CET ONGLET, et non celui du navigateur (7.10).
//
// Le serveur reconnaît le siège par `?jeton=` ou, à défaut, par le cookie
// `jeton` — et ce cookie vaut pour TOUT le navigateur. Deux onglets ouverts
// sur deux sièges (la reine, Otto) : le dernier chargé réécrit le cookie, et
// l'autre onglet, qui sonde /scene toutes les deux secondes sans jeton, reçoit
// le fil de l'autre siège. Son curseur ne colle plus, rien n'arrive, et il
// faut recharger pour revoir son propre fil.
//
// Un onglet ouvert avec `?jeton=` dans son adresse garde donc CE jeton et le
// joint à chacune de ses requêtes. Sans jeton dans l'adresse, rien ne change :
// le cookie décide, comme avant (bascule de siège, changement de monde).
(function () {
  const jeton = new URLSearchParams(location.search).get("jeton");
  if (!jeton) return;

  function avecJeton(url) {
    try {
      const u = new URL(url, location.href);
      if (u.origin !== location.origin || u.searchParams.has("jeton")) return url;
      u.searchParams.set("jeton", jeton);
      return u.pathname + u.search + u.hash;
    } catch (e) { return url; }
  }

  const fetchOrigine = window.fetch.bind(window);
  window.fetch = function (entree, init) {
    if (typeof entree === "string" || entree instanceof URL) {
      return fetchOrigine(avecJeton(String(entree)), init);
    }
    if (entree instanceof Request) {
      return fetchOrigine(new Request(avecJeton(entree.url), entree), init);
    }
    return fetchOrigine(entree, init);
  };

  if (navigator.sendBeacon) {
    const balise = navigator.sendBeacon.bind(navigator);
    navigator.sendBeacon = (url, donnees) => balise(avecJeton(String(url)), donnees);
  }
})();
