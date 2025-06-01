'use client'

import React from 'react'
import { motion } from 'framer-motion'
import {
  AreaChart,
  BarChart,
  Card,
  Title,
  Text
} from '@tremor/react'
import { 
  Calendar,
  Users,
  TrendingUp,
  Clock
} from 'lucide-react'

const chartdata = [
  {
    date: '2023-01',
    'Total Interviews': 45,
    'Successful Hires': 20,
  },
  {
    date: '2023-02',
    'Total Interviews': 52,
    'Successful Hires': 24,
  },
  {
    date: '2023-03',
    'Total Interviews': 48,
    'Successful Hires': 22,
  },
  // Add more data points as needed
]

const performanceData = [
  {
    category: 'Technical Skills',
    score: 85,
  },
  {
    category: 'Communication',
    score: 92,
  },
  {
    category: 'Problem Solving',
    score: 78,
  },
  {
    category: 'Cultural Fit',
    score: 88,
  },
]

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Analytics</h1>
        <div className="flex space-x-2">
          <select className="rounded-lg border bg-white px-4 py-2 text-sm dark:bg-gray-800">
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>Last year</option>
          </select>
          <button className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90">
            Export Report
          </button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card>
            <Title>Interview Trends</Title>
            <Text>Total interviews vs successful hires</Text>
            <AreaChart
              className="mt-4 h-72"
              data={chartdata}
              index="date"
              categories={['Total Interviews', 'Successful Hires']}
              colors={['blue', 'green']}
            />
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <Title>Performance Metrics</Title>
            <Text>Average scores across different categories</Text>
            <BarChart
              className="mt-4 h-72"
              data={performanceData}
              index="category"
              categories={['score']}
              colors={['purple']}
            />
          </Card>
        </motion.div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          {
            title: 'Interview Success Rate',
            value: '68%',
            change: '+5.2%',
            icon: TrendingUp,
          },
          {
            title: 'Average Time to Hire',
            value: '18 days',
            change: '-2.3 days',
            icon: Clock,
          },
          {
            title: 'Active Candidates',
            value: '245',
            change: '+12',
            icon: Users,
          },
          {
            title: 'Scheduled Interviews',
            value: '38',
            change: '+5',
            icon: Calendar,
          },
        ].map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card>
              <div className="flex items-center justify-between">
                <div>
                  <Text>{stat.title}</Text>
                  <div className="mt-2 text-2xl font-bold">{stat.value}</div>
                  <div className="mt-1 text-sm text-green-600">{stat.change}</div>
                </div>
                <stat.icon className="h-8 w-8 text-gray-400" />
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  )
} 