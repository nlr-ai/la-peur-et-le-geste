const assert = require('node:assert/strict');
const { projeter } = require('./domaine/contacts-indirects');
const personnes = new Map(['joueur','ami','cible','autre'].map(id => [id,{id,nom:id}]));
const directs = new Set(['joueur','ami']);
const liens = [{source_id:'ami',cible_id:'joueur',confiance:80},{source_id:'ami',cible_id:'cible',confiance:70}];
assert.equal(projeter('joueur',directs,[],personnes,liens).get('ami')[0].id,'cible');
// Chaque direction est indépendante : une confiance inverse ne suffit pas.
assert.equal(projeter('joueur',directs,[],personnes,[{source_id:'joueur',cible_id:'ami',confiance:100},liens[1]]).size,0);
assert.equal(projeter('joueur',directs,[{source_id:'ami',cible_id:'joueur',opinion:-60}],personnes,liens).size,0);
assert.equal(projeter('joueur',directs,[{source_id:'ami',cible_id:'cible',opinion:-60}],personnes,liens).size,0);
assert.equal(projeter('joueur',new Set([...directs,'cible']),[],personnes,liens).size,0);
assert.equal(projeter('joueur',directs,[],personnes,[liens[0],{source_id:'ami',cible_id:'autre',confiance:10}]).size,0);
// Pas de propagation à un troisième degré, ni de secrets dans la projection.
personnes.get('cible').secret='cache';
const resultat=projeter('joueur',directs,[],personnes,[...liens,{source_id:'cible',cible_id:'autre',confiance:100}]);
assert.deepEqual(resultat.get('ami').map(c=>c.id),['cible']);
assert.equal(resultat.get('ami')[0].secret,undefined);
console.log('Contacts indirects : directions, seuils, variations et confidentialité vérifiés.');
