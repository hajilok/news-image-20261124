// Deterministic offline entrypoint for make.fun news-image-20261124.
// Runs on Node 22 with standard library modules only and zero network access.

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { crc32 } from 'node:zlib';

const MAX_BYTES = 1_048_576; // 1 MiB cap
const MAX_DIMENSION = 1024;  // 1024 x 1024 max pixels

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const JPEG_SOI = Buffer.from([0xff, 0xd8]);

interface ImageMeta {
  format: 'png' | 'jpeg';
  width: number;
  height: number;
  bytes: number;
  sha256: string;
}

function validatePngChunks(buf: Buffer): { width: number; height: number } {
  let offset = 8;
  let width = 0;
  let height = 0;
  let sawIhdr = false;
  let sawIdat = false;
  let sawIend = false;

  while (offset + 12 <= buf.length) {
    const length = buf.readUInt32BE(offset);
    const chunkType = buf.subarray(offset + 4, offset + 8).toString('ascii');
    const dataStart = offset + 8;
    const dataEnd = dataStart + length;
    const crcEnd = dataEnd + 4;

    if (crcEnd > buf.length) {
      throw new Error(`Truncated PNG chunk ${chunkType} at offset ${offset}`);
    }

    const expectedCrc = buf.readUInt32BE(dataEnd);
    const actualCrc = crc32(buf.subarray(offset + 4, dataEnd)) >>> 0;
    if (actualCrc !== expectedCrc) {
      throw new Error(`PNG CRC mismatch in chunk ${chunkType}`);
    }

    if (chunkType === 'IHDR') {
      if (length !== 13) throw new Error('Invalid PNG IHDR length');
      width = buf.readUInt32BE(dataStart);
      height = buf.readUInt32BE(dataStart + 4);
      sawIhdr = true;
    } else if (chunkType === 'IDAT') {
      sawIdat = true;
    } else if (chunkType === 'IEND') {
      sawIend = true;
      if (crcEnd !== buf.length) {
        throw new Error('Trailing bytes after PNG IEND chunk');
      }
      break;
    }

    offset = crcEnd;
  }

  if (!sawIhdr || !sawIdat || !sawIend) {
    throw new Error('Incomplete PNG structure: missing IHDR, IDAT, or IEND');
  }
  return { width, height };
}

function inspectImage(buf: Buffer): ImageMeta {
  if (buf.length === 0 || buf.length > MAX_BYTES) {
    throw new Error(`Invalid image byte size: ${buf.length} (limit ${MAX_BYTES})`);
  }

  const sha256 = createHash('sha256').update(buf).digest('hex');

  if (buf.length >= 24 && buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
    const { width, height } = validatePngChunks(buf);
    return { format: 'png', width, height, bytes: buf.length, sha256 };
  }

  if (buf.length >= 4 && buf.subarray(0, 2).equals(JPEG_SOI)) {
    if (buf[buf.length - 2] !== 0xff || buf[buf.length - 1] !== 0xd9) {
      throw new Error('Truncated JPEG: missing EOI marker');
    }
    let offset = 2;
    while (offset + 4 < buf.length) {
      if (buf[offset] !== 0xff) {
        throw new Error(`Malformed JPEG marker at offset ${offset}`);
      }
      const marker = buf[offset + 1];
      if (marker === 0xd9 || marker === 0xda) break;
      const segLen = buf.readUInt16BE(offset + 2);
      const isSof =
        (marker >= 0xc0 && marker <= 0xc3) ||
        (marker >= 0xc5 && marker <= 0xc7) ||
        (marker >= 0xc9 && marker <= 0xcb) ||
        (marker >= 0xcd && marker <= 0xcf);
      if (isSof && offset + 9 <= buf.length) {
        const height = buf.readUInt16BE(offset + 5);
        const width = buf.readUInt16BE(offset + 7);
        return { format: 'jpeg', width, height, bytes: buf.length, sha256 };
      }
      offset += 2 + segLen;
    }
    throw new Error('JPEG SOF frame dimensions not found');
  }

  throw new Error('Unsupported image format: expected PNG or JPEG bytes');
}

function main(): void {
  const repoRoot = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(repoRoot, 'entry.png');
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const targetPath = join(outputDir, 'entry.png');

  const payload = readFileSync(sourcePath);
  const meta = inspectImage(payload);

  if (meta.width < 1 || meta.height < 1 || meta.width > MAX_DIMENSION || meta.height > MAX_DIMENSION) {
    throw new Error(`Image dimensions ${meta.width}x${meta.height} exceed ${MAX_DIMENSION}x${MAX_DIMENSION}`);
  }

  mkdirSync(outputDir, { recursive: true });
  writeFileSync(targetPath, payload);
}

main();
