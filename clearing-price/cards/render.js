// usage: node render.js data.json outprefix
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const d=fs.readFileSync(process.argv[2],'utf8');const out=process.argv[3];
const b=await chromium.launch();
for(const [size,w,h] of [['tall',1080,1350],['wide',1200,627]]){
 const pg=await b.newPage({viewport:{width:w,height:h}});
 await pg.goto('file://'+path.resolve(__dirname,'card.html')+'?size='+size+'&d='+encodeURIComponent(d));
 await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(50);await pg.screenshot({path:`${out}-${size}.png`});}
await b.close();})();
