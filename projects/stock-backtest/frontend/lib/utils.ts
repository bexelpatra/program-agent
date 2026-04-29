import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Tailwind class merger.
 *
 * Combines `clsx` (conditional class composition) with `tailwind-merge`
 * (last-one-wins resolution for conflicting tailwind utilities).
 *
 * Standard shadcn/ui pattern.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
