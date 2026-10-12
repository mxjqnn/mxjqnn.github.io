# Minifies breakwater.css into tools/styles.min.css and webflow-2-styles-embed.html
import re
s=open('breakwater.css').read()
s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
s=re.sub(r'\s+',' ',s)
for ch in ['{','}',';',',','>']: s=re.sub(r'\s*'+re.escape(ch)+r'\s*',ch,s)
s=re.sub(r':\s+',':',s)
s=s.replace(';}','}').strip()
open('tools/styles.min.css','w').write(s)
# Webflow allows 50,000 characters per Code Embed, so the sheet is split in two at a rule boundary; the embeds sit back to back
cut=s.rfind('}',0,26000)+1
open('tools/styles-a.min.css','w').write(s[:cut]); open('tools/styles-b.min.css','w').write(s[cut:])
print('part A',cut,'part B',len(s)-cut)
open('webflow-2-styles-embed.html','w').write('<!-- Breakwater styles: paste into TWO Code Embeds placed first on the page (Webflow caps an embed at 50,000 characters). Embed 1: -->\n<style>\n'+s[:cut]+'\n</style>\n<!-- Embed 2, directly after embed 1: -->\n<style>\n'+s[cut:]+'\n</style>\n')
print(len(s))
