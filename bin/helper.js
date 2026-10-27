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

const DIVIDER = '='.repeat(60);

function validSubjects() {
  return Object.keys(SUBJECTS).sort();
}

function resolveSubject(raw) {
  if (!raw) return null;
  const rawStr = String(raw).trim().toLowerCase();
  for (const s of Object.keys(SUBJECTS)) {
    if (s.toLowerCase() === rawStr) return s;
  }
  if (['subject1', 'sub1', 's1'].includes(rawStr)) {
    if (SUBJECTS['aoa']) return 'aoa';
  }
  if (['subject2', 'sub2', 's2'].includes(rawStr)) {
    if (SUBJECTS['coa']) return 'coa';
  }
  if (['subject3', 'sub3', 's3'].includes(rawStr)) {
    if (SUBJECTS['fsjp']) return 'fsjp';
  }
  return null;
}

function validTopics(subject) {
  const s = resolveSubject(subject);
  if (!s || !SUBJECTS[s]) return [];
  const keys = Object.keys(SUBJECTS[s]).filter(k => /^\d+$/.test(k));
  return keys.sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
}

function resolveTopic(subject, raw) {
  const s = resolveSubject(subject);
  if (!s || !SUBJECTS[s]) return null;
  const topics = SUBJECTS[s];
  const rawStr = String(raw).trim().toLowerCase();

  if (topics[rawStr]) return rawStr;

  // Normalize: 'exp1', 'exp01', 'exp 1', 'experiment 1', 'topic 1'
  const cleaned = rawStr.replace(/^(exp|experiment|topic)[\s_\-]*/i, '');
  if (topics[cleaned]) return cleaned;

  const cleanedNum = cleaned.replace(/^0+/, '') || '0';
  if (topics[cleanedNum]) return cleanedNum;

  return null;
}

function normalizeArgs(args) {
  // If arguments are ['aoa', 'exp', '1'] -> ['aoa', 'exp1']
  if (args.length >= 3 && ['exp', 'experiment', 'topic'].includes(args[1].toLowerCase())) {
    return [args[0], `exp${args[2]}`, ...args.slice(3)];
  }
  return args;
}

function getTopic(subject, topicNum) {
  const s = resolveSubject(subject);
  if (!s) {
    console.error(`[error] Unknown subject: '${subject}'`);
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }
  const t = resolveTopic(s, topicNum);
  if (!t) {
    const isExperiment = ['aoa', 'coa', 'fsjp'].includes(s);
    const label = isExperiment ? 'experiment' : 'topic';
    console.error(`[error] Unknown ${label} identifier: '${topicNum}' for subject '${s}'`);
    const validItems = validTopics(s).map(k => (isExperiment ? `exp${k}` : k));
    console.error(`        Valid ${label}s: ${validItems.join(', ')} (or 1..${validItems.length})`);
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

// Commands
function cmdList(args) {
  if (args.length === 0) {
    console.log(DIVIDER);
    console.log('  Available Subjects');
    console.log(DIVIDER);
    for (const s of validSubjects()) {
      if (s === 'aoa') {
        console.log(`  * ${s.padEnd(10)} (Analysis of Algorithms -- 10 Experiments)`);
      } else if (s === 'coa') {
        console.log(`  * ${s.padEnd(10)} (Computer Organization & Architecture -- 10 Experiments)`);
      } else if (s === 'fsjp') {
        console.log(`  * ${s.padEnd(10)} (Full Stack Java Programming -- ${validTopics(s).length} Experiments)`);
      } else {
        console.log(`  * ${s}`);
      }
    }
    console.log(DIVIDER);
    return;
  }

  const s = resolveSubject(args[0]);
  if (!s) {
    console.error(`[error] Unknown subject: '${args[0]}'`);
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }

  const isExperiment = ['aoa', 'coa', 'fsjp'].includes(s);
  const label = isExperiment ? 'Experiments' : 'Topics';
  console.log(DIVIDER);
  console.log(`  ${label} in '${s}'`);
  console.log(DIVIDER);
  for (const num of validTopics(s)) {
    const title = SUBJECTS[s][num].title;
    const prefix = isExperiment ? `Exp ${String(num).padStart(2, '0')}` : String(num).padStart(2, ' ');
    const suffix = SUBJECTS[s][num].code_type === 'asm' ? ' [ASM]' : '';
    console.log(`  [${prefix}]  ${title}${suffix}`);
  }
  console.log(DIVIDER);
}

function printAsm(data) {
  const asm = ((data.code_type === 'asm' ? data.code : data.asm) || '').trim();
  if (asm) {
    console.log(asm);
  } else {
    console.log('No assembly program for this experiment.');
  }
}

function cmdShow(args) {
  args = normalizeArgs(args);
  if (args.length < 2) {
    console.error('[error] Usage: helper [show] <subject> <topic_num>');
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }

  const { subject, topicNum, data } = getTopic(args[0], args[1]);
  if (Array.isArray(data.files) && data.files.length > 1) {
    console.error('[error] This experiment has multiple files. Use helper.py:');
    console.error(`        python helper.py show ${subject} ${topicNum}`);
    process.exit(1);
  }
  if (args.length >= 3 && ['asm', 'assembly'].includes(args[2].toLowerCase())) {
    printAsm(data);
    return;
  }
  const code = (data.code || '').trim();
  if (code) {
    // Print ONLY the code - nothing else!
    console.log(code);
  } else {
    console.log('// (no code yet)');
  }
}

function cmdAsm(args) {
  args = normalizeArgs(args);
  if (args.length < 2) {
    console.error('[error] Usage: helper asm <subject> <topic_num>');
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }

  const { data } = getTopic(args[0], args[1]);
  printAsm(data);
}

function cmdWrite(args) {
  args = normalizeArgs(args);
  if (args.length < 2) {
    console.error('[error] Usage: helper write <subject> <topic_num> [filename]');
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }

  const { subject, topicNum, data } = getTopic(args[0], args[1]);
  if (Array.isArray(data.files) && data.files.length > 1) {
    console.error('[error] This experiment has multiple files. Use helper.py:');
    console.error(`        python helper.py write ${subject} ${topicNum}`);
    process.exit(1);
  }
  const isExperiment = ['aoa', 'coa', 'fsjp'].includes(subject);
  const ext = data.language === 'java' ? '.java' : (data.code_type === 'asm' ? '.asm' : '.c');
  let defaultFile;
  if (data.filename) {
    defaultFile = data.filename;
  } else if (isExperiment) {
    defaultFile = `${subject}_exp_${topicNum}${ext}`;
  } else {
    defaultFile = `${subject}_topic_${topicNum}.py`;
  }
  const filename = (args.length >= 3) ? args[2] : defaultFile;

  try {
    fs.writeFileSync(filename, (data.code || '').trim() + '\n', 'utf-8');
    console.log(`[ok] Code written to '${filename}'`);
  } catch (err) {
    console.error(`[error] Could not write file: ${err.message}`);
    process.exit(1);
  }
}

function cmdCopy(args) {
  args = normalizeArgs(args);
  if (args.length < 2) {
    console.error('[error] Usage: helper copy <subject> <topic_num>');
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    process.exit(1);
  }

  const { subject, topicNum, data } = getTopic(args[0], args[1]);
  if (Array.isArray(data.files) && data.files.length > 1) {
    console.error('[error] This experiment has multiple files. Use helper.py:');
    console.error(`        python helper.py copy ${subject} ${topicNum} 1`);
    process.exit(1);
  }
  const copyAsm = args.length >= 3 && ['asm', 'assembly'].includes(args[2].toLowerCase());
  const asmCode = data.code_type === 'asm' ? data.code : data.asm;
  const code = ((copyAsm ? asmCode : data.code) || '').trim();
  const isExperiment = ['aoa', 'coa', 'fsjp'].includes(subject);
  const label = isExperiment ? 'experiment' : 'topic';

  if (!code) {
    console.log(`[warn] The code block for this ${label} is empty - nothing to copy.`);
    return;
  }

  const success = copyToClipboard(code + '\n');
  const displayId = (isExperiment && /^\d+$/.test(topicNum)) ? `Exp ${String(topicNum).padStart(2, '0')}` : topicNum;

  if (success) {
    console.log(`[ok] Code for '${subject}' ${label} ${displayId} copied to clipboard.`);
  } else {
    console.log('[warn] Could not access system clipboard.');
    console.log('       Here is the code:\n');
    console.log(code);
  }
}

const USAGE = `\
helper -- offline CLI study helper tool

Usage:
  helper <subject> <exp_or_topic>          # Prints ONLY the code directly to terminal!
  helper show  <subject> <exp_or_topic>    # Prints ONLY the code
  helper asm   <subject> <exp_or_topic>    # Prints ONLY the assembly code
  helper list                              # List all subjects
  helper list  <subject>                   # List all experiments/topics in subject
  helper write <subject> <exp_or_topic> [file] # Save code directly to file
  helper copy  <subject> <exp_or_topic> [asm]  # Copy code directly to clipboard

Examples:
  helper aoa 1             # Outputs only Exp 01 C code
  helper aoa exp2          # Outputs only Exp 02 C code
  helper aoa exp 3         # Outputs only Exp 03 C code
  helper coa exp1          # Outputs only COA Exp 01 C code
  helper fsjp 1            # Outputs only FSJP Exp 01 Java code
  helper asm coa 3         # Outputs only COA Exp 03 assembly code
  helper aoa 1 > sort.c    # Redirect output directly to a .c file
  helper copy aoa 1        # Copy Exp 01 code to clipboard

COA experiments 3, 4, 8, and 9 are assembly-only. The rest use C.
FSJP experiments are Java. Multi-file FSJP experiments use helper.py.

Available subjects: ${validSubjects().join(', ')}
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
  } else if (first === 'asm') {
    cmdAsm(rest);
  } else if (first === 'write') {
    cmdWrite(rest);
  } else if (first === 'copy') {
    cmdCopy(rest);
  } else if (resolveSubject(first)) {
    // Direct shortcut: helper aoa 1  OR  helper aoa exp 1
    cmdShow([first, ...rest]);
  } else {
    console.error(`[error] Unknown command or subject: '${first}'`);
    console.error('        Valid commands: list, show, asm, write, copy');
    console.error(`        Valid subjects: ${validSubjects().join(', ')}`);
    console.log();
    console.log(USAGE);
    process.exit(1);
  }
}

main();
