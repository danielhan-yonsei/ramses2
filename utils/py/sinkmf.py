#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from plot_backend import set_backend
import argparse
import ramses as ram

parser = argparse.ArgumentParser(description="Compare the sink mass functions of several runs")
parser.add_argument("nout", help="enter output number")
parser.add_argument("paths", nargs="+", help="run directories containing output_*")
parser.add_argument("--labels", nargs="+", help="legend labels, one per run")
parser.add_argument("--nbin", help="number of bins per dex")
parser.add_argument("--out", help="output a png image")
args = parser.parse_args()
no_display = set_backend()

nout = args.nout
labels = args.labels if args.labels else args.paths
if len(labels) != len(args.paths):
    print("Need one label per run")
    exit()
if args.nbin==None:
    nbin=4
else:
    nbin=int(args.nbin)

# Sink masses in Msol for each run
masses = []
for path in args.paths:
    print("Reading output number ",nout," in ",path)
    s=ram.rd_part(nout,path=path+"/",prefix='sink')
    i=ram.rd_info(nout,path=path+"/")
    unit_m = i.unit_d * i.unit_l**3 / 2e33
    masses.append(s.mass[s.mass > 0] * unit_m)

# Common logarithmic bins
lmin = np.floor(np.log10(min([np.min(m) for m in masses]))*nbin)/nbin
lmax = np.ceil(np.log10(max([np.max(m) for m in masses]))*nbin)/nbin
bins = np.linspace(lmin, lmax, int(round((lmax-lmin)*nbin))+1)
bin_size = bins[1]-bins[0]
centers = 0.5*(bins[:-1]+bins[1:])

hists = [np.histogram(np.log10(m), bins=bins)[0] for m in masses]

# Summary and table, first run as reference
print()
for label, m in zip(labels, masses):
    print("%-12s N=%7d  Mtot=%10.4e Msol  M50=%10.4e  M90=%10.4e  Mmax=%10.4e" %
          (label, len(m), np.sum(m), np.percentile(m,50), np.percentile(m,90), np.max(m)))
print()
print("log10 M    " + "".join(["%12s" % l for l in labels]) +
      "".join(["%12s" % ("ratio "+str(k+1)) for k in range(1,len(labels))]))
for ib in range(len(centers)):
    line = "%6.2f     " % centers[ib] + "".join(["%12d" % h[ib] for h in hists])
    for h in hists[1:]:
        if hists[0][ib] > 0:
            line += "%12.3f" % (h[ib]/hists[0][ib])
        else:
            line += "%12s" % "-"
    print(line)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(6,10))

for label, m, h in zip(labels, masses, hists):
    # Differential mass function
    ax1.step(centers, h/bin_size, where='mid', label=label)
    # Cumulative number above M
    ms = np.sort(m)[::-1]
    ax2.plot(np.log10(ms), np.arange(1,len(ms)+1), label=label)
    # Cumulative mass in sinks above M
    ax3.plot(np.log10(ms), np.cumsum(ms), label=label)

ax1.set_yscale("log")
ax1.set_ylabel(r'dN/dlog$_{10}$M')
ax1.legend()
ax2.set_yscale("log")
ax2.set_ylabel(r'N(>M)')
ax3.set_yscale("log")
ax3.set_ylabel(r'M$_{\rm sink}$(>M) [Msol]')
ax3.set_xlabel(r'log$_{10}$ M$_{\rm sink}$ [Msol]')
plt.tight_layout()

if args.out:
    plt.savefig(args.out)

if not no_display:
    plt.show()
