'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
          <div className="container px-4 md:px-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="flex flex-col items-center space-y-4 text-center"
            >
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                Welcome to Ivy
              </h1>
              <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                Your AI-powered interview assistant. Enhance your hiring process with advanced analytics and real-time insights.
              </p>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="space-x-4"
              >
                <Link
                  href="/login"
                  className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                >
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </motion.div>
            </motion.div>
          </div>
        </section>
        
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
          <div className="container px-4 md:px-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3"
            >
              <FeatureCard
                title="AI-Powered Analysis"
                description="Real-time emotion detection and behavioral analysis during interviews."
              />
              <FeatureCard
                title="Advanced Analytics"
                description="Comprehensive reports and insights to make better hiring decisions."
              />
              <FeatureCard
                title="Smart Scheduling"
                description="Automated interview scheduling with calendar integration."
              />
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  )
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="rounded-lg border bg-card p-6 text-card-foreground shadow-sm"
    >
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-sm text-gray-500 dark:text-gray-400">{description}</p>
    </motion.div>
  )
} 