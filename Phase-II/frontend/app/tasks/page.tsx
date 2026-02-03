'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TaskItem from '@/components/TaskItem';
import TaskForm from '@/components/TaskForm';
import ChatInterface from '@/components/ChatInterface';
import { apiClient } from '@/lib/api';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const extractUserIdFromToken = () => {
    const token = localStorage.getItem('authToken');
    if (!token) return null;

    try {
      // Split the JWT token (header.payload.signature)
      const parts = token.split('.');
      if (parts.length !== 3) return null;

      // Decode the payload (second part)
      const payload = JSON.parse(atob(parts[1]));
      return payload.sub || 'default_user'; // 'sub' is the subject/user ID
    } catch (e) {
      console.error('Error decoding token:', e);
      return 'default_user';
    }
  };

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      router.push('/login');
    } else {
      fetchTasks();
    }
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getTasks();
      setTasks(data);
    } catch (err: any) {
      setError('Failed to load tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (newTask: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    try {
      const data = await apiClient.createTask(newTask);
      setTasks([...tasks, data]);
    } catch (err: any) {
      setError('Failed to add task');
      console.error(err);
    }
  };

  const handleUpdateTask = async (updatedTask: Task) => {
    try {
      const data = await apiClient.updateTask(updatedTask.id, {
        title: updatedTask.title,
        description: updatedTask.description,
        completed: updatedTask.completed,
      });
      setTasks(tasks.map(task => task.id === data.id ? data : task));
    } catch (err: any) {
      setError('Failed to update task');
      console.error(err);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const data = await apiClient.toggleTaskCompletion(taskId);
      setTasks(tasks.map(task => task.id === taskId ? data : task));
    } catch (err: any) {
      setError('Failed to update task status');
      console.error(err);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await apiClient.deleteTask(taskId);
        setTasks(tasks.filter(task => task.id !== taskId));
      } catch (err: any) {
        setError('Failed to delete task');
        console.error(err);
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo App</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="ml-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left column - Traditional task management */}
          <div className="space-y-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Add New Task</h2>
              <TaskForm onSubmit={handleAddTask} />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Tasks</h2>

              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
                  <span className="block sm:inline">{error}</span>
                </div>
              )}

              {tasks.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-500">No tasks yet. Add a new task to get started!</p>
                </div>
              ) : (
                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                  <ul className="divide-y divide-gray-200">
                    {tasks.map((task) => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        onUpdate={handleUpdateTask}
                        onToggleComplete={handleToggleComplete}
                        onDelete={handleDeleteTask}
                      />
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Right column - AI Chat Interface */}
          <div>
            <ChatInterface userId={extractUserIdFromToken() || 'default_user'} />
          </div>
        </div>
      </div>
    </div>
  );
}