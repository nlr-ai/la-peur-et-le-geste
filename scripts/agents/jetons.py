# -*- coding: utf-8 -*-
"""JETONS — ce qu'un appel a coute, dans une forme commune aux fournisseurs.

Lu par `compute.enregistrer` sur le resultat normalise de `runtime.appeler`.
"""


def _entier(valeur):
    try:
        return max(0, int(valeur or 0))
    except (TypeError, ValueError):
        return 0


def jetons(resultat):
    """Les jetons d'un appel, dans une forme commune aux trois fournisseurs.

    `entree` ne compte que l'entree fraiche : Codex inclut le cache dans
    `input_tokens`, Claude l'en exclut. Rend None quand le fournisseur n'a
    rien dit — on n'invente pas un zero.
    """
    if not isinstance(resultat, dict):
        return None
    u = resultat.get("usage") or resultat.get("usageMetadata") \
        or (resultat.get("stats") or {}).get("usage") or {}
    if not isinstance(u, dict) or not u:
        return None
    if "promptTokenCount" in u:  # forme Gemini
        cache = _entier(u.get("cachedContentTokenCount"))
        compte = {
            "entree": max(0, _entier(u.get("promptTokenCount")) - cache),
            "cache_lue": cache, "cache_ecrite": 0,
            "sortie": _entier(u.get("candidatesTokenCount")),
            "raisonnement": _entier(u.get("thoughtsTokenCount")),
        }
    elif "cached_input_tokens" in u:  # forme Codex
        cache = _entier(u.get("cached_input_tokens"))
        compte = {
            "entree": max(0, _entier(u.get("input_tokens")) - cache),
            "cache_lue": cache, "cache_ecrite": 0,
            "sortie": _entier(u.get("output_tokens")),
            "raisonnement": _entier(u.get("reasoning_output_tokens")),
        }
    else:  # forme Claude
        compte = {
            "entree": _entier(u.get("input_tokens")),
            "cache_lue": _entier(u.get("cache_read_input_tokens")),
            "cache_ecrite": _entier(u.get("cache_creation_input_tokens")),
            "sortie": _entier(u.get("output_tokens")),
            "raisonnement": 0,
        }
    if not any(compte.values()):
        return None
    cout = resultat.get("total_cost_usd")
    if isinstance(cout, (int, float)) and cout > 0:
        compte["cout_usd"] = float(cout)
    return compte
