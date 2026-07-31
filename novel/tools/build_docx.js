// novel/kyokaisen-mihenshu.txt から星新一賞応募用の縦書きWord文書を作る。
// 使い方: node novel/tools/build_docx.js
'use strict';

const fs = require('fs');
const path = require('path');
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  PageBreak,
  AlignmentType,
  TextDirection,
} = require('docx');

const SRC = path.join(__dirname, '..', 'kyokaisen-mihenshu.txt');
const OUT = path.join(__dirname, '..', 'kyokaisen-mihenshu.docx');

const FONT = 'MS Mincho';
const SECTION_RE = /^[一二三四五六七八九十]+$/;

function main() {
  const raw = fs.readFileSync(SRC, 'utf-8');
  const lines = raw.split('\n');
  const title = lines[0].trim();

  const children = [];

  // 表題
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 400 },
      children: [
        new TextRun({ text: title, font: FONT, size: 32, bold: true }),
      ],
    })
  );

  let firstSection = true;
  for (const raw_line of lines.slice(1)) {
    const line = raw_line.trim();
    if (!line) continue;

    if (SECTION_RE.test(line)) {
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 400, after: 400 },
          pageBreakBefore: !firstSection,
          children: [new TextRun({ text: line, font: FONT, size: 26 })],
        })
      );
      firstSection = false;
      continue;
    }

    children.push(
      new Paragraph({
        spacing: { line: 320 },
        children: [new TextRun({ text: line, font: FONT, size: 21 })],
      })
    );
  }

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: FONT, size: 21 },
        },
      },
    },
    sections: [
      {
        properties: {
          page: {
            size: { width: 11906, height: 16838 }, // A4縦向き(DXA)。縦書きはページ形状を変えずtextDirectionだけで実現する
            margin: { top: 1701, bottom: 1701, left: 1985, right: 1985 },
            textDirection: TextDirection.TOP_TO_BOTTOM_RIGHT_TO_LEFT,
          },
        },
        children,
      },
    ],
  });

  Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync(OUT, buffer);
    console.log('出力:', OUT);
    console.log('段落数:', children.length);
  });
}

main();
