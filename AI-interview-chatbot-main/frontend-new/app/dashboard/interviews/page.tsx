'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card } from '@tremor/react'
import { 
  Calendar,
  Clock,
  Video,
  FileText,
  MoreVertical,
  Plus
} from 'lucide-react'

const interviews = [
  {
    id: 1,
    position: 'Senior Frontend Developer',
    candidate: 'Sarah Johnson',
    date: '2023-12-10T14:00:00',
    duration: '1 hour',
    type: 'Technical Interview',
    status: 'scheduled',
  },
  {
    id: 2,
    position: 'Product Manager',
    candidate: 'Michael Chen',
    date: '2023-12-10T15:30:00',
    duration: '45 minutes',
    type: 'First Round',
    status: 'scheduled',
  },
  {
    id: 3,
    position: 'UX Designer',
    candidate: 'Emily Brown',
    date: '2023-12-11T10:00:00',
    duration: '1 hour',
    type: 'Portfolio Review',
    status: 'scheduled',
  },
]

export default function InterviewsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Interviews</h1>
        <button className="inline-flex items-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90">
          <Plus className="mr-2 h-4 w-4" />
          Schedule Interview
        </button>
      </div>

      <Card>
        <div className="flex items-center justify-between border-b pb-4">
          <div className="flex space-x-4">
            <select className="rounded-lg border bg-white px-4 py-2 text-sm dark:bg-gray-800">
              <option>All Types</option>
              <option>Technical</option>
              <option>Behavioral</option>
              <option>System Design</option>
            </select>
            <select className="rounded-lg border bg-white px-4 py-2 text-sm dark:bg-gray-800">
              <option>All Status</option>
              <option>Scheduled</option>
              <option>Completed</option>
              <option>Cancelled</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <input
              type="search"
              placeholder="Search interviews..."
              className="rounded-lg border px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>

        <div className="mt-4 space-y-4">
          {interviews.map((interview, index) => (
            <motion.div
              key={interview.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="relative rounded-lg border p-4 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <h3 className="font-medium">{interview.position}</h3>
                  <p className="text-sm text-gray-500">{interview.candidate}</p>
                </div>
                <button className="rounded-full p-2 hover:bg-gray-100 dark:hover:bg-gray-700">
                  <MoreVertical className="h-5 w-5 text-gray-500" />
                </button>
              </div>
              <div className="mt-4 flex items-center space-x-6">
                <div className="flex items-center text-sm text-gray-500">
                  <Calendar className="mr-2 h-4 w-4" />
                  {new Date(interview.date).toLocaleDateString()}
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <Clock className="mr-2 h-4 w-4" />
                  {interview.duration}
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <FileText className="mr-2 h-4 w-4" />
                  {interview.type}
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between">
                <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:bg-green-800/30 dark:text-green-500">
                  {interview.status}
                </span>
                <div className="flex space-x-2">
                  <button className="inline-flex items-center rounded-lg border px-3 py-1 text-sm hover:bg-gray-50 dark:hover:bg-gray-800">
                    View Details
                  </button>
                  <button className="inline-flex items-center rounded-lg bg-primary px-3 py-1 text-sm text-white hover:bg-primary/90">
                    <Video className="mr-2 h-4 w-4" />
                    Join Call
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </Card>
    </div>
  )
} 