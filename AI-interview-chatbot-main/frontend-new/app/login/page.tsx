'use client'

import React from 'react'
import { signIn } from 'next-auth/react'
import { motion } from 'framer-motion'
import { Github, Mail } from 'lucide-react'

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mx-auto w-full max-w-md space-y-6 p-6"
      >
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold">Welcome back</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Sign in to your account to continue
          </p>
        </div>
        <div className="space-y-4">
          <button
            onClick={() => signIn('google', { callbackUrl: '/dashboard' })}
            className="flex w-full items-center justify-center space-x-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            <Mail className="h-5 w-5" />
            <span>Continue with Google</span>
          </button>
          <button
            onClick={() => signIn('github', { callbackUrl: '/dashboard' })}
            className="flex w-full items-center justify-center space-x-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            <Github className="h-5 w-5" />
            <span>Continue with GitHub</span>
          </button>
        </div>
        <p className="text-center text-sm text-gray-500 dark:text-gray-400">
          By continuing, you agree to our{' '}
          <a href="/terms" className="underline hover:text-gray-900 dark:hover:text-gray-100">
            Terms of Service
          </a>{' '}
          and{' '}
          <a href="/privacy" className="underline hover:text-gray-900 dark:hover:text-gray-100">
            Privacy Policy
          </a>
        </p>
      </motion.div>
    </div>
  )
} 