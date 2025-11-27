"use client"
import { Star } from "lucide-react"
import { cls } from "./utils"

export default function ConversationRow({ data, active, onSelect, onTogglePin, showMeta }) {
  // --- CHANGES ARE BELOW ---

  // This helper function handles keyboard accessibility.
  // It allows the user to trigger the onSelect function by pressing Enter or Space.
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      // Prevent the default action (like scrolling the page on spacebar press)
      e.preventDefault();
      onSelect();
    }
  };

  return (
    <div className="group relative">
      {/* 1. Changed <button> to <div> */}
      <div
        onClick={onSelect}
        // 2. Added accessibility attributes and keyboard handler
        role="button"
        tabIndex="0"
        onKeyDown={handleKeyDown}
        // 3. Added 'cursor-pointer' to the className for visual feedback
        className={cls(
          "-mx-1 flex w-[calc(100%+8px)] items-center gap-2 rounded-lg px-2 py-2 text-left cursor-pointer",
          active
            ? "bg-zinc-100 text-zinc-900 dark:bg-zinc-800/60 dark:text-zinc-100"
            : "hover:bg-zinc-100 dark:hover:bg-zinc-800",
        )}
        title={data.title}
      >
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="truncate text-sm font-medium tracking-tight">{data.title}</span>
          </div>
        </div>
        {/* The inner <button> is now valid because its parent is a <div> */}
        <button
          onClick={(e) => {
            e.stopPropagation()
            onTogglePin()
          }}
          title={data.pinned ? "Unpin" : "Pin"}
          className="rounded-md p-1 text-zinc-500 opacity-0 transition group-hover:opacity-100 hover:bg-zinc-200/50 dark:text-zinc-300 dark:hover:bg-zinc-700/60"
          aria-label={data.pinned ? "Unpin conversation" : "Pin conversation"}
        >
          {data.pinned ? (
            <Star className="h-4 w-4 fill-zinc-800 text-zinc-800 dark:fill-zinc-200 dark:text-zinc-200" />
          ) : (
            <Star className="h-4 w-4" />
          )}
        </button>
      </div>

      <div className="pointer-events-none absolute left-[calc(100%+6px)] top-1 hidden w-64 rounded-xl border border-zinc-200 bg-white p-3 text-xs text-zinc-700 shadow-lg dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-200 md:group-hover:block">
        <div className="line-clamp-6 whitespace-pre-wrap">{data.preview}</div>
      </div>
    </div>
  )
}
