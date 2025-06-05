"use client";

import React, { useState } from "react";
import {
  CheckCircle2,
  Circle,
  CircleAlert,
  CircleDotDashed,
  CircleX,
  Play,
  Pause,
  RotateCcw,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../lib/utils";

// Type definitions
interface Subtask {
  id: string;
  title: string;
  description: string;
  status: "pending" | "in_progress" | "completed" | "failed" | "paused";
  priority: "low" | "medium" | "high" | "urgent";
  agent?: string;
  estimated_duration?: number;
  dependencies?: string[];
}

interface AgentPlan {
  id: string;
  title: string;
  description: string;
  status: "pending" | "in_progress" | "completed" | "failed";
  subtasks: Subtask[];
  progress_percentage: number;
  estimated_total_duration?: number;
}

interface AgentPlanProps {
  plan: AgentPlan;
  onRunSubtask?: (planId: string, subtaskId: string) => void;
  onPauseSubtask?: (planId: string, subtaskId: string) => void;
  onReassignSubtask?: (planId: string, subtaskId: string, newAgent: string) => void;
}

function getStatusIcon(status: string) {
  switch (status) {
    case "completed":
      return <CheckCircle2 className="w-5 h-5 text-green-500" />;
    case "in_progress":
      return <CircleDotDashed className="w-5 h-5 text-blue-500 animate-spin" />;
    case "failed":
      return <CircleX className="w-5 h-5 text-red-500" />;
    case "paused":
      return <CircleAlert className="w-5 h-5 text-yellow-500" />;
    default:
      return <Circle className="w-5 h-5 text-gray-400" />;
  }
}

function getStatusColor(status: string) {
  switch (status) {
    case "completed":
      return "text-green-500 bg-green-500/10 border-green-500/20";
    case "in_progress":
      return "text-blue-500 bg-blue-500/10 border-blue-500/20";
    case "failed":
      return "text-red-500 bg-red-500/10 border-red-500/20";
    case "paused":
      return "text-yellow-500 bg-yellow-500/10 border-yellow-500/20";
    default:
      return "text-gray-400 bg-gray-500/10 border-gray-500/20";
  }
}

function getPriorityColor(priority: string) {
  switch (priority) {
    case "urgent":
      return "bg-red-500/20 text-red-300 border-red-500/30";
    case "high":
      return "bg-orange-500/20 text-orange-300 border-orange-500/30";
    case "medium":
      return "bg-blue-500/20 text-blue-300 border-blue-500/30";
    case "low":
      return "bg-gray-500/20 text-gray-300 border-gray-500/30";
    default:
      return "bg-gray-500/20 text-gray-300 border-gray-500/30";
  }
}

function SubtaskActions({ 
  planId, 
  subtask, 
  onRun, 
  onPause, 
  onReassign 
}: { 
  planId: string; 
  subtask: Subtask;
  onRun?: (planId: string, subtaskId: string) => void;
  onPause?: (planId: string, subtaskId: string) => void;
  onReassign?: (planId: string, subtaskId: string, agent: string) => void;
}) {
  const [showReassign, setShowReassign] = useState(false);
  const [newAgent, setNewAgent] = useState("");

  const agents = [
    "research_specialist",
    "devops_specialist", 
    "scout_commander",
    "model_coordinator",
    "tool_curator",
    "integration_architect",
    "live_api_specialist"
  ];

  return (
    <div className="flex flex-wrap gap-2 mt-3">
      {/* Run Button */}
      <button
        className={cn(
          "flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium transition-all",
          "bg-green-500/20 hover:bg-green-500/30 text-green-300 border border-green-500/30",
          (subtask.status === "completed" || subtask.status === "in_progress") && 
          "opacity-50 cursor-not-allowed"
        )}
        disabled={subtask.status === "completed" || subtask.status === "in_progress"}
        onClick={() => onRun?.(planId, subtask.id)}
      >
        <Play className="w-3 h-3" />
        Run
      </button>

      {/* Pause Button */}
      <button
        className={cn(
          "flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium transition-all",
          "bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-300 border border-yellow-500/30",
          subtask.status !== "in_progress" && "opacity-50 cursor-not-allowed"
        )}
        disabled={subtask.status !== "in_progress"}
        onClick={() => onPause?.(planId, subtask.id)}
      >
        <Pause className="w-3 h-3" />
        Pause
      </button>

      {/* Reassign Button */}
      <button
        className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium transition-all bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 border border-purple-500/30"
        onClick={() => setShowReassign(!showReassign)}
      >
        <RotateCcw className="w-3 h-3" />
        Reassign
      </button>

      {/* Reassign Dropdown */}
      <AnimatePresence>
        {showReassign && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="flex items-center gap-2"
          >
            <select
              className="px-2 py-1 rounded text-xs bg-gray-800 border border-gray-600 text-white"
              value={newAgent}
              onChange={(e) => setNewAgent(e.target.value)}
            >
              <option value="">Select Agent</option>
              {agents.map(agent => (
                <option key={agent} value={agent}>
                  {agent.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
            <button
              className="px-2 py-1 rounded text-xs bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50"
              onClick={() => {
                if (newAgent) {
                  onReassign?.(planId, subtask.id, newAgent);
                  setShowReassign(false);
                  setNewAgent("");
                }
              }}
              disabled={!newAgent}
            >
              Assign
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export const AgentPlan: React.FC<AgentPlanProps> = ({
  plan,
  onRunSubtask,
  onPauseSubtask,
  onReassignSubtask
}) => {
  const [expandedSubtasks, setExpandedSubtasks] = useState<Set<string>>(new Set());

  const toggleSubtask = (subtaskId: string) => {
    const newExpanded = new Set(expandedSubtasks);
    if (newExpanded.has(subtaskId)) {
      newExpanded.delete(subtaskId);
    } else {
      newExpanded.add(subtaskId);
    }
    setExpandedSubtasks(newExpanded);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-900/50 backdrop-blur-xl border border-gray-700/50 rounded-xl p-6 space-y-6"
    >
      {/* Plan Header */}
      <div className="space-y-4">
        <div className="flex items-start justify-between">
          <div className="space-y-2">
            <h3 className="text-xl font-semibold text-white">{plan.title}</h3>
            <p className="text-gray-300 text-sm">{plan.description}</p>
          </div>
          <div className={cn(
            "px-3 py-1 rounded-lg text-xs font-medium border",
            getStatusColor(plan.status)
          )}>
            {plan.status.replace('_', ' ').toUpperCase()}
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Progress</span>
            <span className="text-purple-300">{Math.round(plan.progress_percentage)}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${plan.progress_percentage}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      </div>

      {/* Subtasks */}
      <div className="space-y-3">
        <h4 className="text-lg font-medium text-white flex items-center gap-2">
          <span>📋</span>
          Subtasks ({plan.subtasks.length})
        </h4>
        
        <div className="space-y-2">
          {plan.subtasks.map((subtask, index) => (
            <motion.div
              key={subtask.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-gray-800/50 border border-gray-600/30 rounded-lg p-4 space-y-3"
            >
              <div 
                className="flex items-start gap-3 cursor-pointer"
                onClick={() => toggleSubtask(subtask.id)}
              >
                {getStatusIcon(subtask.status)}
                <div className="flex-1 space-y-2">
                  <div className="flex items-center justify-between">
                    <h5 className="font-medium text-white">{subtask.title}</h5>
                    <div className="flex items-center gap-2">
                      {subtask.agent && (
                        <span className="px-2 py-1 rounded text-xs bg-blue-500/20 text-blue-300 border border-blue-500/30">
                          {subtask.agent.replace('_', ' ')}
                        </span>
                      )}
                      <span className={cn(
                        "px-2 py-1 rounded text-xs border",
                        getPriorityColor(subtask.priority)
                      )}>
                        {subtask.priority}
                      </span>
                    </div>
                  </div>
                  
                  <AnimatePresence>
                    {expandedSubtasks.has(subtask.id) && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="space-y-3"
                      >
                        <p className="text-gray-300 text-sm">{subtask.description}</p>
                        
                        {subtask.estimated_duration && (
                          <div className="text-xs text-gray-400">
                            Estimated duration: {subtask.estimated_duration} minutes
                          </div>
                        )}

                        <SubtaskActions
                          planId={plan.id}
                          subtask={subtask}
                          onRun={onRunSubtask}
                          onPause={onPauseSubtask}
                          onReassign={onReassignSubtask}
                        />
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Plan Summary */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-700/50">
        <div className="text-sm text-gray-400">
          {plan.subtasks.filter(s => s.status === "completed").length} of {plan.subtasks.length} completed
        </div>
        {plan.estimated_total_duration && (
          <div className="text-sm text-gray-400">
            Total estimated: {Math.round(plan.estimated_total_duration / 60)}h {plan.estimated_total_duration % 60}m
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default AgentPlan;