/**
 * Select — minimal native `<select>` with shadcn-style chrome.
 *
 * The full shadcn Select uses Radix Popover + ListBox primitives; for
 * V3 MVP we use the native element (zero a11y surface to maintain) and
 * inherit form semantics for free. We can swap in the Radix variant
 * later without touching consumers.
 */
import * as React from "react";

import { cn } from "@/lib/utils";

export type SelectProps = React.SelectHTMLAttributes<HTMLSelectElement>;

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, children, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        "flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    >
      {children}
    </select>
  ),
);
Select.displayName = "Select";
