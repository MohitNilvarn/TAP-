import * as React from "react"

import { cn } from "../../lib/utils"

// Note: I am not installing class-variance-authority or radix-ui yet, so I will implement a simpler version first
// or I should install them. The user asked for "ultra rich", so using standard libraries is better.
// I will install class-variance-authority and @radix-ui/react-slot now.
// Wait, I can't install inside this tool call. I'll write a simpler version for now or add a TODO to install.
// Actually, I'll just use standard props without cva for now to save time, or I'll install them in the next step.
// Let's stick to simple props for now to avoid dependency hell if I can't run commands easily.
// But "ultra rich" usually implies good component libraries.
// I'll implement a solid Button without extra deps for now.

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link" | "glass"
    size?: "default" | "sm" | "lg" | "icon"
    asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = "default", size = "default", asChild = false, ...props }, ref) => {
        const Comp = "button"

        const variants = {
            default: "bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg shadow-primary/20",
            destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
            outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
            secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
            ghost: "hover:bg-accent hover:text-accent-foreground",
            link: "text-primary underline-offset-4 hover:underline",
            glass: "bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 shadow-xl",
        }

        const sizes = {
            default: "h-10 px-4 py-2",
            sm: "h-9 rounded-md px-3",
            lg: "h-11 rounded-md px-8",
            icon: "h-10 w-10",
        }

        return (
            <Comp
                className={cn(
                    "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
                    variants[variant],
                    sizes[size],
                    className
                )}
                ref={ref}
                {...props}
            />
        )
    }
)
Button.displayName = "Button"

export { Button }
