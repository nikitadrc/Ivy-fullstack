'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card, Metric, Text } from '@tremor/react'
import { Users, Calendar, Clock, TrendingUp } from 'lucide-react'

const stats = [
  {
    name: 'Total Interviews',
    value: '156',
    icon: Users,
    change: '+12.3%',
    changeType: 'positive',
  },
  {
    name: 'Scheduled Today',
    value: '8',
    icon: Calendar,
    change: '+4.1%',
    changeType: 'positive',
  },
  {
    name: 'Average Duration',
    value: '45m',
    icon: Clock,
    change: '-2.5%',
    changeType: 'negative',
  },
  {
    name: 'Success Rate',
    value: '89%',
    icon: TrendingUp,
    change: '+5.2%',
    changeType: 'positive',
  },
]

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <button className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90">
          New Interview
        </button>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card>
              <div className="flex items-center justify-between">
                <div>
                  <Text>{stat.name}</Text>
                  <Metric>{stat.value}</Metric>
                </div>
                <stat.icon className="h-8 w-8 text-gray-400" />
              </div>
              <div className={`mt-4 flex items-center text-sm ${
                stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
              }`}>
                {stat.change}
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <Card>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Recent Interviews</h2>
            <button className="text-sm text-primary hover:underline">
              View all
            </button>
          </div>
          <div className="space-y-4">
            {[1, 2, 3].map((_, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: i * 0.1 }}
                className="flex items-center justify-between rounded-lg border p-4"
              >
                <div>
                  <p className="font-medium">Frontend Developer</p>
                  <p className="text-sm text-gray-500">John Doe</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium">Today, 2:00 PM</p>
                  <p className="text-sm text-gray-500">45 minutes</p>
                </div>
              </motion.div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Quick Actions</h2>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {[
              { name: 'Schedule Interview', icon: Calendar },
              { name: 'View Analytics', icon: TrendingUp },
              { name: 'Manage Team', icon: Users },
              { name: 'Settings', icon: Clock },
            ].map((action, i) => (
              <motion.button
                key={action.name}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: i * 0.1 }}
                className="flex items-center space-x-2 rounded-lg border p-4 hover:bg-gray-50 dark:hover:bg-gray-800"
              >
                <action.icon className="h-5 w-5 text-gray-400" />
                <span className="text-sm font-medium">{action.name}</span>
              </motion.button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
} 