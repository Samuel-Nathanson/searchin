const { promises: fs } = require("fs")
const path = require("path")

async function copyDir(src, dest) {
  await fs.mkdir(dest, { recursive: true });
  let entries = await fs.readdir(src, { withFileTypes: true });

  for (let entry of entries) {
    let srcPath = path.join(src, entry.name);
    let destPath = path.join(dest, entry.name);

    entry.isDirectory() ?
      await copyDir(srcPath, destPath) :
      await fs.copyFile(srcPath, destPath);
  }
}

const srcDir = "./src"
const buildDir = "./build"

// To copy a folder :qor file  
copyDir(srcDir, buildDir, function (err) {
  if (err) {
    console.error(err);
  }
});