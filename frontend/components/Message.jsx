import { cls } from "./utils"
import { Leaf, Activity } from "lucide-react"

export default function Message({ role, children, image, diagnosis, confidence }) {
  const isUser = role === "user"
  return (
    <div className={cls("flex gap-3", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="mt-0.5 grid h-7 w-7 place-items-center rounded-full border border-emerald-500 bg-zinc-950 text-[10px] font-bold text-emerald-500 shrink-0">
          FB
        </div>
      )}
      <div className="flex flex-col gap-2 max-w-[85%]">
        {image && (
          <div className={cls(
            "rounded-2xl overflow-hidden shadow-sm border border-zinc-200 dark:border-zinc-800",
            isUser ? "ml-auto" : "mr-auto"
          )}>
            <img src={image} alt="Uploaded content" className="max-w-full h-auto max-h-64 object-cover" />
          </div>
        )}

        {diagnosis ? (
          <div className="rounded-2xl overflow-hidden shadow-sm border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
            <div className="bg-emerald-50 dark:bg-emerald-950/30 px-4 py-3 border-b border-emerald-100 dark:border-emerald-900/30 flex justify-between items-center gap-4">
              <div className="flex items-center gap-2.5 min-w-0">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 dark:bg-emerald-900/50 dark:text-emerald-400">
                  <Leaf className="h-4 w-4" />
                </div>
                <div className="flex flex-col min-w-0">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600/80 dark:text-emerald-400/80">
                    Diagnosis
                  </span>
                  <span className="font-semibold text-emerald-950 dark:text-emerald-50 text-sm truncate">
                    {diagnosis.split('___').join(' ')}
                  </span>
                </div>
              </div>
              {confidence && (
                <div className="flex items-center gap-1.5 shrink-0 bg-white dark:bg-zinc-950 px-2 py-1 rounded-full border border-emerald-100 dark:border-emerald-900/30 shadow-sm">
                  <Activity className="h-3 w-3 text-emerald-500" />
                  <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300">
                    {confidence}
                  </span>
                </div>
              )}
            </div>
            <div className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
              {children}
            </div>
          </div>
        ) : (
          children && (
            <div
              className={cls(
                "rounded-2xl px-3 py-2 text-sm shadow-sm",
                isUser
                  ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                  : "bg-white text-zinc-900 dark:bg-zinc-900 dark:text-zinc-100 border border-zinc-200 dark:border-zinc-800",
              )}
            >
              {children}
            </div>
          )
        )}
      </div>
      {isUser && (
        <div className="mt-0.5 grid h-7 w-7 place-items-center rounded-full bg-zinc-900 text-[10px] font-bold text-white dark:bg-white dark:text-zinc-900 shrink-0">
          QR
        </div>
      )}
    </div>
  )
}
