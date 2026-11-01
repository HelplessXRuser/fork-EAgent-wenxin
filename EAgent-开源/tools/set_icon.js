#!/usr/bin/env node
/*
 * 替换 PE 文件图标（所有图标组 × 多尺寸）
 * 用法: node set_icon.js <input.exe> <icon.ico> [output.exe]
 * 依赖: npm install resedit
 */
const fs = require('fs');
const ResEdit = require('resedit');

const [inExe, icoPath, outExe] = process.argv.slice(2);
if (!inExe || !icoPath) {
  console.log('usage: node set_icon.js <input.exe> <icon.ico> [output.exe]');
  process.exit(2);
}
const dst = outExe || inExe;

const exe = ResEdit.NtExecutable.from(fs.readFileSync(inExe), { ignoreCert: true });
const res = ResEdit.NtExecutableResource.from(exe);
const groups = ResEdit.Resource.IconGroupEntry.fromEntries(res.entries);
if (!groups.length) throw new Error('no icon group found');
const ico = ResEdit.Data.IconFile.from(fs.readFileSync(icoPath));

for (const g of groups) {
  ResEdit.Resource.IconGroupEntry.replaceIconsForResource(
    res.entries, g.id, g.lang, ico.icons.map(i => i.data)
  );
}
res.outputResource(exe);
fs.writeFileSync(dst, Buffer.from(exe.generate()));
console.log(`icon replaced: ${groups.length} group(s) x ${ico.icons.length} size(s) -> ${dst}`);
