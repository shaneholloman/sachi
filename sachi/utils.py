import re
from typing import cast

import regex as alt_re

FAKE_SLASH = "／"

FS_SPECIAL_CHARS = re.compile(r"[/\\:*\"?<>|]")

# https://github.com/filebot/data/blob/57a846e346838461e17f0674a7d2732d95413d91/media-sources.txt
SOURCES_RE = {
    "BluRay": re.compile(
        r"\b(Blu.?Ray|BDRip|BRip|BR.?Rip|BDMV|BD|BDR|BD25|BD50|BD5|BD9|3D.?BluRay|3DBD|BDRemux|BDRX)\b"
    ),
    "CAM": re.compile(r"\b(CAM|CAMRip|CAM.?Rip)\b"),
    "DVD-R": re.compile(r"\b(DVD.?R|DVD.?Full|Full.?Rip|DVD|DVD.?[59])\b"),
    "DVDRip": re.compile(r"\b(DVD.?Rip|DVD.?Mux)\b"),
    "HDDVD": re.compile(r"\b(HDDVD)\b"),
    "HDTV": re.compile(r"\b(HDTV|DVB|DVBRip|DTVRip|HDTVRip)\b"),
    "LaserRip": re.compile(r"\b(LaserRip|Laserdisc)\b"),
    "MicroHD": re.compile(r"\b(Micro.?HD)\b"),
    "R5": re.compile(r"\b(R5|R5.?LINE)\b"),
    "SCREENER": re.compile(
        r"\b(SCREENER|SCR|DVDSCR|DVDSCREENER|BDSCR|BR.?Scr|BR.?Screener)\b"
    ),
    "SDTV": re.compile(r"\b(SDTV|PDTV|DSR|DSRip|SATRip|DTHRip|TVRip)\b"),
    "TELECINE": re.compile(r"\b(TELECINE|TC|HDTC)\b"),
    "TELESYNC": re.compile(r"\b(TELESYNC|TS|HDTS|PDVD|PTVD|PreDVDRip)\b"),
    "UnknownRip": re.compile(r"\b(UnknownRip|URip)\b"),
    "VCD": re.compile(r"\b(VCD)\b"),
    "VHS": re.compile(r"\b(VHS|VHSRip)\b"),
    "WEB-DL": cast(re, alt_re).compile(
        r"\b((?:(?:ABC|ATVP|AMC|AMZN|BBC|CBS|CC|CR|CRAV|CW|DCU|DSNP|DSNY|Disney[+]|DisneyPlus|FBWatch|FREE|FOX|HBO|MAX|HMAX|HULU|iP|iT|LIFE|MA|MTV|NBC|NICK|NF|Netflix|RED|TF1|STZ|STAN|PCOK|PMTP)[ .-])?(?:WEB.?DL|WEB.?DLRip|WEB.?Cap|WEB.?Rip|HC|HD.?Rip|VODR|VODRip|PPV|PPVRip|iTunesHD|ithd|AmazonHD|NetflixHD|NetflixUHD|(?<=\d{3,4}[p].)WEB|WEB(?=.[hx]\d{3})))\b"
    ),
    "WorkPrint": re.compile(r"\b(WORKPRINT|WP)\b"),
}
