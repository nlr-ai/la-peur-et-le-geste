# -*- coding: utf-8 -*-
"""Lancer un processus qui survit a son lanceur — le worker d'un CAST.

LE CAST MOURAIT AVEC SON LANCEUR (7.10). Un billet-reveil part le plus souvent
d'une commande que le MJ lance dans SA session (agy) : quand la commande rend
la main, l'outil tue tout ce qu'elle a fait naitre, worker detache compris,
avant sa premiere ligne. Mesure : requetes restees dans
.agents-runtime/requests/ (Gerardys, Orwyle, Steffon), journaux a zero octet,
aucun reveil abouti. Les drapeaux de detachement n'y changent rien (sortir du
job est refuse : WinError 5), parce que l'arbre des processus suffit a nous
retrouver.

Donc sous Windows on ne lance pas le worker : on demande a WINDOWS de le
lancer (WMI, Win32_Process.Create). Il nait enfant du service WMI, hors de
tout arbre qu'on puisse tuer. Il n'herite ni de notre environnement ni de nos
flux : l'environnement voyage dans la requete, et le worker ouvre lui-meme son
journal (runtime_worker.py, 3e argument). Si WMI echoue, on retombe sur un
Popen detache — jamais pire qu'avant.
"""
import os
import subprocess

_SANS_FENETRE = 0x08000000
_NOUVEAU_GROUPE = 0x00000200
_DETACHED_PROCESS = 0x00000008


def _ligne(argv):
    return subprocess.list2cmdline(argv)


def _par_wmi(argv, cwd):
    """PID du processus cree par WMI, ou None."""
    def q(s):
        return "'" + s.replace("'", "''") + "'"
    # ShowWindow=0 : sans lui, chaque worker ouvre une console VISIBLE sur le
    # bureau de l'utilisateur (vu le 7.10 : des fenetres « tour 1 : dire — »).
    script = ("$s = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly "
              "-Property @{ShowWindow=[UInt16]0}; "
              "$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create "
              "-Arguments @{CommandLine=%s; CurrentDirectory=%s; "
              "ProcessStartupInformation=$s}; "
              "if ($r.ReturnValue -eq 0) { $r.ProcessId } else { exit 1 }"
              % (q(_ligne(argv)), q(cwd)))
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                           capture_output=True, timeout=60, creationflags=_SANS_FENETRE)
    except (OSError, subprocess.SubprocessError):
        return None
    sortie = r.stdout.decode("utf-8", "replace").strip()
    return int(sortie) if r.returncode == 0 and sortie.isdigit() else None


def lancer_hors_arbre(argv, cwd, log, env):
    """Lance argv hors de l'arbre de l'appelant ; rend son PID (ou None)."""
    if os.name == "nt":
        pid = _par_wmi(argv, cwd)
        if pid:
            return pid
    with open(log, "ab") as f:
        kw = ({"creationflags": _SANS_FENETRE | _NOUVEAU_GROUPE | _DETACHED_PROCESS}
              if os.name == "nt" else {"start_new_session": True})
        return subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                stdout=f, stderr=subprocess.STDOUT, **kw).pid
