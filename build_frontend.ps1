Set-Location vue-app
pnpx @tailwindcss/cli -i ./src/main.css -o ./src/output.css
pnpm build
Set-Location ..
if (Test-Path dist) {
    Remove-Item -Path dist -Recurse -Force
}
Copy-Item -Recurse -Force vue-app/dist dist