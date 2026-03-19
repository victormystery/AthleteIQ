/**
 * Database seeding script.
 * Run with: npm run seed (from the server directory)
 *
 * Seeds:
 * 1. Career pathways (11 pathways)
 * 2. Admin user (if not already present)
 */

import 'dotenv/config'
import mongoose from 'mongoose'
import { env } from '../config/env.js'
import { CareerPathway, User } from '../models/index.js'
import { careerPathwaysSeedData } from '../data/career_pathways.js'

async function seed() {
  console.log('🌱 AthleteIQ Seed Script Starting...\n')

  try {
    await mongoose.connect(env.mongoUri)
    console.log('✅ Connected to MongoDB:', env.mongoUri)

    // ── 1. Seed Career Pathways ────────────────────────────────────────────
    console.log('\n📋 Seeding career pathways...')

    let created = 0
    let skipped = 0

    for (const pathway of careerPathwaysSeedData) {
      const exists = await CareerPathway.findOne({ slug: pathway.slug })
      if (exists) {
        console.log(`  ⏭  Skipped (exists): ${pathway.title}`)
        skipped++
      } else {
        await CareerPathway.create(pathway)
        console.log(`  ✅ Created: ${pathway.title}`)
        created++
      }
    }

    console.log(`\n  Career pathways: ${created} created, ${skipped} skipped`)

    // ── 2. Seed Admin User ─────────────────────────────────────────────────
    console.log('\n👤 Seeding admin user...')

    const adminEmail = 'admin@athleteiq.com'
    const existingAdmin = await User.findOne({ email: adminEmail })

    if (existingAdmin) {
      console.log(`  ⏭  Admin user already exists: ${adminEmail}`)
    } else {
      await User.create({
        name: 'AthleteIQ Admin',
        email: adminEmail,
        password: 'Admin@AthleteIQ2026!',
        role: 'admin'
      })
      console.log(`  ✅ Admin user created: ${adminEmail}`)
      console.log('  🔑 Default password: Admin@AthleteIQ2026!')
      console.log('  ⚠️  IMPORTANT: Change this password after first login!')
    }

    // ── Summary ────────────────────────────────────────────────────────────
    console.log('\n🎉 Seeding complete!\n')
    console.log('📊 Database Summary:')
    console.log(`  • Career Pathways: ${await CareerPathway.countDocuments()}`)
    console.log(`  • Users: ${await User.countDocuments()}`)
    console.log('\n🚀 You can now start the server with: npm run dev')
  } catch (err) {
    console.error('\n❌ Seeding failed:', err)
    process.exit(1)
  } finally {
    await mongoose.disconnect()
    console.log('\n🔌 Disconnected from MongoDB')
  }
}

seed()
