// usage: node logo.js [out.png]
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:512,height:512}});
await p.goto('file://'+__dirname+'/logo.html');await p.screenshot({path:process.argv[2]||'clearing-price-logo.png'});await b.close();})();
