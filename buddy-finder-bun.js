#!/usr/bin/env bun
// buddy-finder-bun.js
// Searches for buddy UIDs using Bun.hash (matches real Claude Code)
// Usage: bun buddy-finder-bun.js --species duck --rarity legendary

import { randomBytes } from 'crypto'

const SALT = 'friend-2026-401'
const SPECIES = ['duck', 'goose', 'blob', 'cat', 'dragon', 'octopus', 'owl', 'penguin', 'turtle', 'snail', 'ghost', 'axolotl', 'capybara', 'cactus', 'robot', 'rabbit', 'mushroom', 'chonk']
const RARITIES = ['common', 'uncommon', 'rare', 'epic', 'legendary']
const RARITY_WEIGHTS = { common: 60, uncommon: 25, rare: 10, epic: 4, legendary: 1 }
const RARITY_RANK = { common: 0, uncommon: 1, rare: 2, epic: 3, legendary: 4 }
const EYES = ['·', '✦', '×', '◉', '@', '°']
const HATS = ['none', 'crown', 'tophat', 'propeller', 'halo', 'wizard', 'beanie', 'tinyduck']
const STAT_NAMES = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK']
const RARITY_FLOOR = { common: 5, uncommon: 15, rare: 25, epic: 35, legendary: 50 }

function mulberry32(seed) {
  let a = seed >>> 0
  return function () {
    a |= 0
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function pick(rng, arr) {
  return arr[Math.floor(rng() * arr.length)]
}

function rollRarity(rng) {
  let roll = rng() * 100
  for (const r of RARITIES) {
    roll -= RARITY_WEIGHTS[r]
    if (roll < 0) return r
  }
  return 'common'
}

function rollStats(rng, rarity) {
  const floor = RARITY_FLOOR[rarity]
  const peak = pick(rng, STAT_NAMES)
  let dump = pick(rng, STAT_NAMES)
  while (dump === peak) dump = pick(rng, STAT_NAMES)

  const stats = {}
  for (const name of STAT_NAMES) {
    if (name === peak) {
      stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30))
    } else if (name === dump) {
      stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15))
    } else {
      stats[name] = floor + Math.floor(rng() * 40)
    }
  }
  return stats
}

function rollBuddy(uid) {
  const seed = Number(BigInt(Bun.hash(uid + SALT)) & 0xffffffffn)
  const rng = mulberry32(seed)

  const rarity = rollRarity(rng)
  const species = pick(rng, SPECIES)
  const eye = pick(rng, EYES)
  const hat = rarity === 'common' ? 'none' : pick(rng, HATS)
  const shiny = rng() < 0.01
  const stats = rollStats(rng, rarity)

  return { rarity, species, eye, hat, shiny, stats }
}

function parseArgs() {
  const opts = { max: 500000, count: 1 }
  const args = Bun.argv.slice(2)

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--species': opts.species = args[++i]; break
      case '--rarity': opts.rarity = args[++i]; break
      case '--eye': opts.eye = args[++i]; break
      case '--hat': opts.hat = args[++i]; break
      case '--shiny': opts.shiny = true; break
      case '--max': opts.max = parseInt(args[++i]); break
      case '--count': opts.count = parseInt(args[++i]); break
      case '--help': case '-h':
        console.log(`Usage: bun buddy-finder-bun.js [options]

Options:
  --species <name>   ${SPECIES.join(', ')}
  --rarity <name>    ${RARITIES.join(', ')}
  --eye <char>       ${EYES.join(' ')}
  --hat <name>       ${HATS.join(', ')}
  --shiny            Require shiny
  --max <number>     Max iterations (default: 500000)
  --count <number>   Results to find (default: 1)

Examples:
  bun buddy-finder-bun.js --species duck --rarity legendary
  bun buddy-finder-bun.js --species dragon --shiny`)
        process.exit(0)
    }
  }
  return opts
}

const opts = parseArgs()
const minRarityRank = opts.rarity ? RARITY_RANK[opts.rarity] : -1

console.log(`🔍 Searching with Bun.hash (matches real Claude Code)`)
const filters = []
if (opts.species) filters.push(`species=${opts.species}`)
if (opts.rarity) filters.push(`rarity>=${opts.rarity}`)
if (opts.eye) filters.push(`eye=${opts.eye}`)
if (opts.hat) filters.push(`hat=${opts.hat}`)
if (opts.shiny) filters.push('shiny')
console.log(`Filters: ${filters.join(', ') || 'any'} (max ${opts.max.toLocaleString()})`)
console.log('')

const startTime = Date.now()
let found = 0

for (let i = 0; i < opts.max; i++) {
  const uid = randomBytes(32).toString('hex')
  const buddy = rollBuddy(uid)

  if (opts.species && buddy.species !== opts.species) continue
  if (opts.rarity && RARITY_RANK[buddy.rarity] < minRarityRank) continue
  if (opts.eye && buddy.eye !== opts.eye) continue
  if (opts.hat && buddy.hat !== opts.hat) continue
  if (opts.shiny && !buddy.shiny) continue

  found++
  const shinyLabel = buddy.shiny ? ' ✨' : ''
  console.log(`#${found} [${buddy.rarity.toUpperCase()}] ${buddy.species}${shinyLabel}`)
  console.log(`     eye=${buddy.eye} hat=${buddy.hat}`)
  console.log(`     uid: ${uid}`)
  console.log('')

  if (found >= opts.count) break
}

const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)
if (found === 0) {
  console.log(`❌ No match found in ${opts.max.toLocaleString()} iterations (${elapsed}s)`)
} else {
  console.log(`✅ Found ${found} match(es) in ${elapsed}s`)
}
