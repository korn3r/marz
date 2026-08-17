cd `dirname $0`/app/dashboard
npm run build --if-present -- --outDir build --assetsDir statics
cp ./build/index.html ./build/404.html
