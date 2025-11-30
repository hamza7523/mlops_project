"use client"
import { useState } from "react"
import { Paperclip } from "lucide-react"
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover"

export default function ComposerActionsPopover({ children, onUploadClick }) {
  const [open, setOpen] = useState(false)

  const mainActions = [
    {
      icon: Paperclip,
      label: "Upload your plant",
      action: () => onUploadClick?.(),
    },
  ]

  const handleAction = (action) => {
    action()
    setOpen(false)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>{children}</PopoverTrigger>
      <PopoverContent className="w-56 p-0" align="start" side="top">
        <div className="p-2">
          <div className="space-y-1">
            {mainActions.map((action, index) => (
              <button
                key={index}
                onClick={() => handleAction(action.action)}
                className="flex items-center justify-between w-full p-2 text-sm text-left hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg group"
              >
                <div className="flex items-center gap-3">
                  <action.icon className="h-4 w-4 text-zinc-500 group-hover:text-zinc-900 dark:text-zinc-400 dark:group-hover:text-zinc-100" />
                  <span>{action.label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  )
}
