#!/usr/bin/env python3
import csv, random, os
hooks = [
"Cloudways or Kinsta? Fast answer",
"GeneratePress or Astra? Choose fast",
"RankMath or Yoast? Pick right",
"Umami or Plausible? Privacy wins",
"WP Rocket or free cache?",
"Fix slow WordPress in 10 minutes",
"Stop CLS in two steps",
"Hit LCP under 2.5s today",
"Delay JS safely, instantly",
"Compress images without ugly blur",
"Best hosting for photographers 2025",
"Best stack under €20/mo",
"Best image optimizer for WP",
"Best analytics without cookies",
]
bullets = ["GeneratePress, no builder","ShortPixel WebP/AVIF","Delay non-critical JS","Preload key requests","System font stack","CDN + edge cache","Backups & staging","Granular scaling","Lower entry price","Privacy-first tracking"]
tags = ["#wordpress #pagespeed","#seo #webdev","#lcp #cwv","#photography #hosting","#analytics #privacy"]
rows = [["id","hook","b1","b2","b3","cta","hashtags"]]
n=1
for h in hooks:
    for _ in range(4):
        b = random.sample(bullets,3)
        rows.append([f"b2_{n}",h,b[0],b[1],b[2],"See my stack + settings. Link in bio.",random.choice(tags)])
        n+=1
rows = rows[:51]
os.makedirs("data", exist_ok=True)
with open("data/video_scripts_batch2.csv","w",newline="",encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
print("Wrote data/video_scripts_batch2.csv with",len(rows)-1,"rows")
