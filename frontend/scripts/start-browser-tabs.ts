const { spawn, exec } = require('child_process');
const http = require('http');

// Start Angular dev server using npx so we use the local CLI
const ngServe = spawn('npx', ['ng', 'serve'], { stdio: 'inherit', shell: true });

const urlBase = 'http://localhost:4200';
const urls = [`${urlBase}/robot`, `${urlBase}/map`];

function checkServer(): void {
  http.get(urlBase, (res: { statusCode: number; }) => {
    if (res.statusCode && res.statusCode >= 200 && res.statusCode < 400) {
      // Open two tabs in Windows default browser
      const openCmd = urls.map(u => `start "" "${u}"`).join(' && ');
      exec(openCmd, (err: any) => {
        if (err) console.error('Failed to open browser tabs:', err);
      });
    } else {
      setTimeout(checkServer, 800);
    }
  }).on('error', () => setTimeout(checkServer, 800));
}

checkServer();

// Forward exit signals to the ng serve process
function forward(): () => void {
  return () => {
    try { ngServe.kill(); } catch (e) { /* ignore */ }
    process.exit();
  };
}

process.on('SIGINT', forward());
process.on('SIGTERM', forward());
