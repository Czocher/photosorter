# PhotoSorter

Fedora KDE5 automatic photo sorting utility meant for faster camera handling.

Add it as a KDE Device Notifier action using:

```
photosorter.py '%f'
```

It will load the photos from your camer/SD-card, group them by consecutive dates
and copy them to a local directory under `~/Pictures/PhotoSorter` (or fail if it doesn't exist ;)).
