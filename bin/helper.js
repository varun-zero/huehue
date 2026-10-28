#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

// Load data
const dataPath = path.join(__dirname, '..', 'data.json');
let SUBJECTS = {};
try {
  SUBJECTS = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
} catch (err) {
  console.error(`[error] Could not load data from ${dataPath}: ${err.message}`);
  process.exit(1);
}

const DEFAULT_SUBJECT = 'fsjp';
const DIVIDER = '='.repeat(60);

function validSubjects() {
  return Object.keys(SUBJECTS).sort();
}

function resolveSubject(raw) {
  if (!raw) return DEFAULT_SUBJECT;
  const rawStr = String(raw).trim().toLowerCase();
  for (const s of Object.keys(SUBJECTS)) {
    if (s.toLowerCase() === rawStr) return s;
  }
  if (['subject3', 'sub3', 's3', 'java', 'fullstack', 'fsjp'].includes(rawStr)) {
    return 'fsjp';
  }
  return null;
}

function validTopics(subject = DEFAULT_SUBJECT) {
  const s = resolveSubject(subject);
  if (!s || !SUBJECTS[s]) return [];
  const keys = Object.keys(SUBJECTS[s]).filter(k => /^\d+$/.test(k));
  return keys.sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
}

function resolveTopic(subject, raw) {
  const s = resolveSubject(subject) || DEFAULT_SUBJECT;
  if (!s || !SUBJECTS[s]) return null;
  const topics = SUBJECTS[s];
  const rawStr = String(raw).trim().toLowerCase();

  if (topics[rawStr]) return rawStr;

  const cleaned = rawStr.replace(/^(exp|experiment|topic|q)[\s_\-]*/i, '');
  if (topics[cleaned]) return cleaned;

  const cleanedNum = cleaned.replace(/^0+/, '') || '0';
  if (topics[cleanedNum]) return cleanedNum;

  return null;
}

function normalizeArgs(args) {
  if (args.length >= 3 && ['exp', 'experiment', 'topic', 'q'].includes(args[1].toLowerCase())) {
    return [args[0], `exp${args[2]}`, ...args.slice(3)];
  }
  if (args.length >= 2 && ['exp', 'experiment', 'topic', 'q'].includes(args[0].toLowerCase())) {
    return [`exp${args[1]}`, ...args.slice(2)];
  }
  return args;
}

function getTopic(subject, topicNum) {
  const s = resolveSubject(subject) || DEFAULT_SUBJECT;
  if (!SUBJECTS[s]) {
    console.error(`[error] Unknown subject: '${subject}'`);
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }
  const t = resolveTopic(s, topicNum);
  if (!t) {
    console.error(`[error] Unknown experiment identifier: '${topicNum}' for subject '${s}'`);
    const validItems = validTopics(s).map(k => `exp${k}`);
    console.error(`        Valid experiments: ${validItems.join(', ')} (or 1..${validItems.length})`);
    process.exit(1);
  }
  return { subject: s, topicNum: t, data: SUBJECTS[s][t] };
}

function copyToClipboard(text) {
  const platform = process.platform;
  try {
    if (platform === 'win32') {
      const proc = spawnSync('clip', { input: Buffer.from(text, 'utf16le') });
      return proc.status === 0;
    } else if (platform === 'darwin') {
      const proc = spawnSync('pbcopy', { input: text });
      return proc.status === 0;
    } else {
      for (const cmd of ['xclip', 'xsel']) {
        const args = (cmd === 'xclip') ? ['-selection', 'clipboard'] : ['--clipboard', '--input'];
        const proc = spawnSync(cmd, args, { input: text });
        if (proc.status === 0) return true;
      }
    }
  } catch (err) {
    // ignore
  }
  return false;
}

function topicFiles(topicData) {
  if (Array.isArray(topicData.files) && topicData.files.length > 0) {
    return topicData.files;
  }
  return [{
    name: topicData.filename || '',
    language: topicData.language || 'java',
    code: topicData.code || ''
  }];
}

function resolveFile(files, raw) {
  if (raw === null || raw === undefined) return null;
  const text = String(raw).trim();
  if (text.toLowerCase() === 'all') return -1;
  if (/^\d+$/.test(text)) {
    const num = parseInt(text, 10);
    if (num >= 1 && num <= files.length) return num - 1;
    return null;
  }
  const lower = text.toLowerCase();
  for (let i = 0; i < files.length; i++) {
    const name = String(files[i].name || '');
    if (name.toLowerCase() === lower || path.basename(name).toLowerCase() === lower) {
      return i;
    }
  }
  return null;
}

// Commands
function cmdList(args) {
  const subject = args.length > 0 ? args[0] : DEFAULT_SUBJECT;
  const s = resolveSubject(subject);
  if (!s || !SUBJECTS[s]) {
    console.error(`[error] Unknown subject: '${subject}'`);
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }

  console.log(DIVIDER);
  console.log(`  Experiments in '${s}' (Full Stack Java Programming)`);
  console.log(DIVIDER);
  for (const num of validTopics(s)) {
    const topic = SUBJECTS[s][num];
    const prefix = `Exp ${String(num).padStart(2, '0')}`;
    const files = topicFiles(topic);
    const suffix = files.length > 1 ? ` (${files.length} files)` : '';
    console.log(`  [${prefix}]  ${topic.title}${suffix}`);
  }
  console.log(DIVIDER);
}

function cmdShow(args) {
  args = normalizeArgs(args);
  if (!args.length) {
    console.error('[error] Usage: helper [show] <exp_num> [file|all]');
    console.error('               helper [show] fsjp <exp_num> [file|all]');
    process.exit(1);
  }

  let rawSub = DEFAULT_SUBJECT;
  let rawTopic = args[0];
  let fileArg = null;

  if (args.length === 1) {
    rawSub = DEFAULT_SUBJECT;
    rawTopic = args[0];
  } else if (resolveSubject(args[0])) {
    rawSub = args[0];
    rawTopic = args[1];
    fileArg = args[2] || null;
  } else {
    rawSub = DEFAULT_SUBJECT;
    rawTopic = args[0];
    fileArg = args[1] || null;
  }

  const { subject, topicNum, data } = getTopic(rawSub, rawTopic);
  const files = topicFiles(data);

  if (files.length > 1) {
    let selector = fileArg;
    if (selector === null) {
      // If no file selector specified, show index
      console.log(`[Exp ${String(topicNum).padStart(2, '0')}] ${data.title}`);
      console.log(`${files.length} files:\n`);
      files.forEach((f, idx) => {
        const lineCount = (f.code || '').trim().split('\n').length;
        console.log(`  ${idx + 1}. ${(f.name || `file${idx + 1}`).padEnd(30)} ${(f.language || '').toUpperCase().padEnd(10)} ${lineCount} lines`);
      });
      console.log(`\nPass '1'..'${files.length}' or 'all' to print contents.`);
      return;
    }

    const chosen = resolveFile(files, selector);
    if (chosen === null) {
      console.error(`[error] Unknown file '${selector}' for experiment ${topicNum}.`);
      process.exit(1);
    }

    if (chosen === -1) {
      files.forEach((f, idx) => {
        if (idx > 0) console.log();
        console.log(`===== ${idx + 1}. ${f.name || `file${idx + 1}`} =====`);
        console.log((f.code || '').trim());
      });
    } else {
      console.log((files[chosen].code || '').trim());
    }
    return;
  }

  const code = (files[0].code || '').trim();
  if (code) {
    console.log(code);
  } else {
    console.log('// (no code yet)');
  }
}

function cmdWrite(args) {
  args = normalizeArgs(args);
  if (!args.length) {
    console.error('[error] Usage: helper write [subject] <exp_num> [filename|folder]');
    process.exit(1);
  }

  let rawSub = DEFAULT_SUBJECT;
  let rawTopic = args[0];
  let destArg = null;

  if (args.length === 1) {
    rawSub = DEFAULT_SUBJECT;
    rawTopic = args[0];
  } else if (resolveSubject(args[0])) {
    rawSub = args[0];
    rawTopic = args[1];
    destArg = args[2] || null;
  } else {
    rawSub = DEFAULT_SUBJECT;
    rawTopic = args[0];
    destArg = args[1] || null;
  }

  const { subject, topicNum, data } = getTopic(rawSub, rawTopic);
  const files = topicFiles(data);

  if (files.length > 1) {
    const folder = destArg || `${subject}_exp_${topicNum}`;
    fs.mkdirSync(folder, { recursive: true });
    files.forEach(f => {
      const target = path.join(folder, f.name || 'file.txt');
      fs.writeFileSync(target, (f.code || '').trim() + '\n', 'utf-8');
      console.log(`     ${target}`);
    });
    console.log(`[ok] Wrote ${files.length} files to '${folder}'`);
    return;
  }

  const filename = destArg || files[0].name || `${subject}_exp_${topicNum}.java`;
  try {
    fs.writeFileSync(filename, (files[0].code || '').trim() + '\n', 'utf-8');
    console.log(`[ok] Code written to '${filename}'`);
  } catch (err) {
    console.error(`[error] Could not write file: ${err.message}`);
    process.exit(1);
  }
}

function cmdCopy(args) {
  args = normalizeArgs(args);
  if (!args.length) {
    console.error('[error] Usage: helper copy [subject] <exp_num> [file|all]');
    process.exit(1);
  }

  let rawSub = DEFAULT_SUBJECT;
  let rawTopic = args[0];
  let fileArg = null;

  if (args.length === 1) {
    rawSub = DEFAULT_SUBJECT;
    rawTopic = args[0];
  } else if (resolveSubject(args[0])) {
    rawSub = args[0];
    rawTopic = args[1];
    fileArg = args[2] || null;
  } else {
    rawSub = DEFAULT_SUBJECT;
    rawTopic = args[0];
    fileArg = args[1] || null;
  }

  const { subject, topicNum, data } = getTopic(rawSub, rawTopic);
  const files = topicFiles(data);

  let textToCopy = '';
  let label = '';

  if (files.length > 1) {
    const selector = fileArg || '1';
    const chosen = resolveFile(files, selector);
    if (chosen === null) {
      console.error(`[error] Unknown file '${selector}' for experiment ${topicNum}.`);
      process.exit(1);
    }
    if (chosen === -1) {
      textToCopy = files.map((f, idx) => `===== ${idx + 1}. ${f.name} =====\n${(f.code || '').trim()}`).join('\n\n');
      label = `${files.length} files`;
    } else {
      textToCopy = (files[chosen].code || '').trim();
      label = files[chosen].name;
    }
  } else {
    textToCopy = (files[0].code || '').trim();
    label = `Exp ${String(topicNum).padStart(2, '0')}`;
  }

  if (!textToCopy) {
    console.log(`[warn] The code block is empty - nothing to copy.`);
    return;
  }

  const success = copyToClipboard(textToCopy + '\n');
  if (success) {
    console.log(`[ok] ${label} copied to clipboard.`);
  } else {
    console.log('[warn] Could not access system clipboard.\n');
    console.log(textToCopy);
  }
}

const USAGE = `\
helper -- Offline CLI study helper tool for Full Stack Java Programming (FSJP)

Usage:
  helper fsjp <exp_num> [file|all]          # Prints ONLY the code directly to terminal!
  helper <exp_num> [file|all]               # Prints ONLY the code directly to terminal!
  helper show  [subject] <exp_num> [file]   # Prints code
  helper list                               # List all experiments
  helper write [subject] <exp_num> [file]   # Save code to file/folder
  helper copy  [subject] <exp_num> [file]   # Copy code directly to clipboard

Examples:
  helper 6                  # Outputs Exp 06 Hierarchical Inheritance
  helper fsjp 6             # Outputs Exp 06 Hierarchical Inheritance
  helper fsjp 8 1           # Outputs Exp 08 file 1 (index.html)
  helper fsjp 8 2           # Outputs Exp 08 file 2 (HelloServlet.java)
  helper fsjp 8 all         # Outputs Exp 08 both files
  helper 6 > Hierarchical.java # Redirect directly to a file
`;

function main() {
  const argv = process.argv.slice(2);

  if (!argv.length || ['-h', '--help', 'help'].includes(argv[0])) {
    console.log(USAGE);
    process.exit(0);
  }

  const first = argv[0].toLowerCase();
  const rest = argv.slice(1);

  if (first === 'list') {
    cmdList(rest);
  } else if (['show', 'code', 'get'].includes(first)) {
    cmdShow(rest);
  } else if (first === 'write') {
    cmdWrite(rest);
  } else if (first === 'copy') {
    cmdCopy(rest);
  } else if (resolveSubject(first)) {
    cmdShow([first, ...rest]);
  } else if (resolveTopic(DEFAULT_SUBJECT, first)) {
    cmdShow([DEFAULT_SUBJECT, first, ...rest]);
  } else {
    console.error(`[error] Unknown command or experiment: '${first}'`);
    console.error('        Valid commands: list, show, write, copy');
    console.log();
    console.log(USAGE);
    process.exit(1);
  }
}

main();
